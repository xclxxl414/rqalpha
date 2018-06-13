# -*- coding: utf-8 -*-
#
# Copyright 2017 Ricequant, Inc
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division
import six
import numpy as np
from rqalpha.model.base_account import BaseAccount
from rqalpha.environment import Environment
from rqalpha.events import EVENT
from rqalpha.const import DEFAULT_ACCOUNT_TYPE, POSITION_EFFECT, SIDE
from rqalpha.utils.i18n import gettext as _
from rqalpha.utils.logger import user_system_log

from rqalpha.api.api_base import decorate_api_exc, instruments, cal_style
from rqalpha.execution_context import ExecutionContext
from rqalpha.environment import Environment
from rqalpha.model.order import Order, MarketOrder, LimitOrder, OrderStyle
from rqalpha.const import EXECUTION_PHASE, SIDE, POSITION_EFFECT, ORDER_TYPE, RUN_TYPE
from rqalpha.model.instrument import Instrument
from rqalpha.utils.exception import RQInvalidArgument
from rqalpha.utils.logger import user_system_log
from rqalpha.utils.i18n import gettext as _
from rqalpha.utils.arg_checker import apply_rules, verify_that


def margin_of(order_book_id, quantity, price):
    env = Environment.get_instance()
    margin_info = env.data_proxy.get_margin_info(order_book_id)
    margin_multiplier = env.config.base.margin_multiplier
    margin_rate = margin_info['long_margin_ratio'] * margin_multiplier
    contract_multiplier = env.get_instrument(order_book_id).contract_multiplier
    return quantity * contract_multiplier * price * margin_rate


class FutureAccount(BaseAccount):

    __abandon_properties__ = [
        "daily_holding_pnl",
        "daily_realized_pnl"
    ]

    def register_event(self):
        event_bus = Environment.get_instance().event_bus
        event_bus.add_listener(EVENT.SETTLEMENT, self._settlement)
        event_bus.add_listener(EVENT.ORDER_PENDING_NEW, self._on_order_pending_new)
        event_bus.add_listener(EVENT.ORDER_CREATION_REJECT, self._on_order_creation_reject)
        event_bus.add_listener(EVENT.ORDER_CANCELLATION_PASS, self._on_order_unsolicited_update)
        event_bus.add_listener(EVENT.ORDER_UNSOLICITED_UPDATE, self._on_order_unsolicited_update)
        event_bus.add_listener(EVENT.TRADE, self._on_trade)
        if self.AGGRESSIVE_UPDATE_LAST_PRICE:
            event_bus.add_listener(EVENT.BAR, self._on_bar)
            event_bus.add_listener(EVENT.TICK, self._on_tick)

    def fast_forward(self, orders, trades=list()):
        # 计算 Positions
        for trade in trades:
            if trade.exec_id in self._backward_trade_set:
                continue
            self._apply_trade(trade)
        # 计算 Frozen Cash
        self._frozen_cash = sum(self._frozen_cash_of_order(order) for order in orders if order.is_active())

    def get_state(self):
        return {
            'positions': {
                order_book_id: position.get_state()
                for order_book_id, position in six.iteritems(self._positions)
            },
            'frozen_cash': self._frozen_cash,
            'total_cash': self._total_cash,
            'backward_trade_set': list(self._backward_trade_set),
            'transaction_cost': self._transaction_cost,
        }

    def set_state(self, state):
        self._frozen_cash = state['frozen_cash']
        self._backward_trade_set = set(state['backward_trade_set'])
        self._transaction_cost = state['transaction_cost']

        margin_changed = 0
        self._positions.clear()
        for order_book_id, v in six.iteritems(state['positions']):
            position = self._positions.get_or_create(order_book_id)
            position.set_state(v)
            if 'margin_rate' in v and abs(v['margin_rate'] - position.margin_rate) > 1e-6:
                 margin_changed += position.margin * (v['margin_rate'] - position.margin_rate) / position.margin_rate

        self._total_cash = state['total_cash'] + margin_changed


    @property
    def type(self):
        return DEFAULT_ACCOUNT_TYPE.FUTURE.name

    @staticmethod
    def _frozen_cash_of_order(order):
        if order.position_effect == POSITION_EFFECT.OPEN:
            return margin_of(order.order_book_id, order.unfilled_quantity, order.frozen_price)
        else:
            return 0

    @staticmethod
    def _frozen_cash_of_trade(trade):
        if trade.position_effect == POSITION_EFFECT.OPEN:
            return margin_of(trade.order_book_id, trade.last_quantity, trade.frozen_price)
        else:
            return 0

    @property
    def total_value(self):
        return self._total_cash + self.margin + self.holding_pnl

    # -- Margin 相关
    @property
    def margin(self):
        """
        [float] 总保证金
        """
        return sum(position.margin for position in six.itervalues(self._positions))

    @property
    def buy_margin(self):
        """
        [float] 买方向保证金
        """
        return sum(position.buy_margin for position in six.itervalues(self._positions))

    @property
    def sell_margin(self):
        """
        [float] 卖方向保证金
        """
        return sum(position.sell_margin for position in six.itervalues(self._positions))

    # -- PNL 相关
    @property
    def daily_pnl(self):
        """
        [float] 当日盈亏
        """
        return self.realized_pnl + self.holding_pnl - self.transaction_cost

    @property
    def holding_pnl(self):
        """
        [float] 浮动盈亏
        """
        return sum(position.holding_pnl for position in six.itervalues(self._positions))

    @property
    def realized_pnl(self):
        """
        [float] 平仓盈亏
        """
        return sum(position.realized_pnl for position in six.itervalues(self._positions))

    def _settlement(self, event):
        total_value = self.total_value

        for position in list(self._positions.values()):
            order_book_id = position.order_book_id
            if position.is_de_listed() and position.buy_quantity + position.sell_quantity != 0:
                user_system_log.warn(
                    _(u"{order_book_id} is expired, close all positions by system").format(order_book_id=order_book_id))
                del self._positions[order_book_id]
            elif position.buy_quantity == 0 and position.sell_quantity == 0:
                del self._positions[order_book_id]
            else:
                position.apply_settlement()
        self._total_cash = total_value - self.margin - self.holding_pnl

        # 如果 total_value <= 0 则认为已爆仓，清空仓位，资金归0
        if total_value <= 0:
            self._positions.clear()
            self._total_cash = 0

        self._backward_trade_set.clear()

    def _on_bar(self, event):
        for position in self._positions.values():
            position.update_last_price()

    def _on_tick(self, event):
        for position in self._positions.values():
            position.update_last_price()

    def _on_order_pending_new(self, event):
        if self != event.account:
            return
        self._frozen_cash += self._frozen_cash_of_order(event.order)

    def _on_order_creation_reject(self, event):
        if self != event.account:
            return
        self._frozen_cash -= self._frozen_cash_of_order(event.order)

    def _on_order_unsolicited_update(self, event):
        if self != event.account:
            return
        self._frozen_cash -= self._frozen_cash_of_order(event.order)

    def _on_trade(self, event):
        if self != event.account:
            return
        self._apply_trade(event.trade)

    def _apply_trade(self, trade):
        if trade.exec_id in self._backward_trade_set:
            return
        order_book_id = trade.order_book_id
        position = self._positions.get_or_create(order_book_id)
        delta_cash = position.apply_trade(trade)

        self._transaction_cost += trade.transaction_cost
        self._total_cash -= trade.transaction_cost
        self._total_cash += delta_cash
        self._frozen_cash -= self._frozen_cash_of_trade(trade)
        self._backward_trade_set.add(trade.exec_id)

    # @apply_rules(verify_that('order_book_id').is_valid_stock(),
    #              verify_that('quantity').is_number(),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order(self,order_book_id, quantity, price=None, style=None):
        """
        全品种通用智能调仓函数

        如果不指定 price, 则相当于下 MarketOrder

        如果 order_book_id 是股票，等同于调用 order_shares

        如果 order_book_id 是期货，则进行智能下单:

            *   quantity 表示调仓量
            *   如果 quantity 为正数，则先平 Sell 方向仓位，再开 Buy 方向仓位
            *   如果 quantity 为负数，则先平 Buy 反向仓位，再开 Sell 方向仓位

        :param order_book_id: 下单标的物
        :type order_book_id: :class:`~Instrument` object | `str`

        :param int quantity: 调仓量

        :param float price: 下单价格

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: list[:class:`~Order`]

        :example:

        ..  code-block:: python3
            :linenos:

            # 当前仓位为0
            # RB1710 多方向调仓2手：调整后变为 BUY 2手
            order('RB1710'， 2)

            # RB1710 空方向调仓3手：先平多方向2手 在开空方向1手，调整后变为 SELL 1手
            order('RB1710', -3)

        """
        style = cal_style(price, style)
        orders = self._order_general(order_book_id, quantity, style)

        if isinstance(orders, Order):
            return [orders]
        return orders

    # @apply_rules(verify_that('order_book_id').is_valid_stock(),
    #              verify_that('quantity').is_number(),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order_to(self, order_book_id, quantity, price=None, style=None):
        """
        如果不指定 price, 则相当于 MarketOrder

        如果 order_book_id 是股票，则表示仓位调整到多少股

        如果 order_book_id 是期货，则进行智能调仓:

            *   quantity 表示调整至某个仓位
            *   quantity 如果为正数，则先平 SELL 方向仓位，再 BUY 方向开仓 quantity 手
            *   quantity 如果为负数，则先平 BUY 方向仓位，再 SELL 方向开仓 -quantity 手

        :param order_book_id: 下单标的物
        :type order_book_id: :class:`~Instrument` object | `str`

        :param int quantity: 调仓量

        :param float price: 下单价格

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: list[:class:`~Order`]

        :example:

        ..  code-block:: python3
            :linenos:

            # 当前仓位为0
            # RB1710 调仓至 BUY 2手
            order_to('RB1710', 2)

            # RB1710 调仓至 SELL 1手
            order_to('RB1710'， -1)

        """
        style = cal_style(price, style)
        position = self.positions[order_book_id]
        quantity = quantity - position.buy_quantity + position.sell_quantity
        orders = self._order_general(order_book_id, quantity, style=style)

        if isinstance(orders, Order):
            return [orders]
        return orders

    def buy_open(self,id_or_ins, amount, price=None, style=None):
        """
        买入开仓。

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str` | List[:class:`~Instrument`] | List[`str`]

        :param int amount: 下单手数

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object

        :example:

        .. code-block:: python

            #以价格为3500的限价单开仓买入2张上期所AG1607合约：
            buy_open('AG1607', amount=2, price=3500))
        """
        return self._order(id_or_ins, amount, SIDE.BUY, POSITION_EFFECT.OPEN, cal_style(price, style))

    def buy_close(self,id_or_ins, amount, price=None, style=None, close_today=False):
        """
        平卖仓

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str` | List[:class:`~Instrument`] | List[`str`]

        :param int amount: 下单手数

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :param bool close_today: 是否指定发平进仓单，默认为False，发送平仓单

        :return: :class:`~Order` object | list[:class:`~Order`]

        :example:

        .. code-block:: python

            #市价单将现有IF1603空仓买入平仓2张：
            buy_close('IF1603', 2)
        """
        position_effect = POSITION_EFFECT.CLOSE_TODAY if close_today else POSITION_EFFECT.CLOSE
        return self._order(id_or_ins, amount, SIDE.BUY, position_effect, cal_style(price, style))


    def sell_open(self,id_or_ins, amount, price=None, style=None):
        """
        卖出开仓

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str` | List[:class:`~Instrument`] | List[`str`]

        :param int amount: 下单手数

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object
        """
        return self._order(id_or_ins, amount, SIDE.SELL, POSITION_EFFECT.OPEN, cal_style(price, style))


    def sell_close(self,id_or_ins, amount, price=None, style=None, close_today=False):
        """
        平买仓

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str` | List[:class:`~Instrument`] | List[`str`]

        :param int amount: 下单手数

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :param bool close_today: 是否指定发平进仓单，默认为False，发送平仓单

        :return: :class:`~Order` object | list[:class:`~Order`]
        """
        position_effect = POSITION_EFFECT.CLOSE_TODAY if close_today else POSITION_EFFECT.CLOSE
        return self._order(id_or_ins, amount, SIDE.SELL, position_effect, cal_style(price, style))

    def assure_future_order_book_id(self,id_or_symbols):
        if isinstance(id_or_symbols, Instrument):
            if id_or_symbols.type != "Future":
                raise RQInvalidArgument(
                    _(u"{order_book_id} is not supported in current strategy type").format(
                        order_book_id=id_or_symbols.order_book_id))
            else:
                return id_or_symbols.order_book_id
        elif isinstance(id_or_symbols, six.string_types):
            return self.assure_future_order_book_id(Environment.get_instance().data_proxy.instruments(id_or_symbols))
        else:
            raise RQInvalidArgument(_(u"unsupported order_book_id type"))

    def _order_general(self, order_book_id, quantity, style):
        position = self.positions[order_book_id]
        orders = []
        if quantity > 0:
            # 平昨仓
            if position.sell_old_quantity > 0:
                orders.append(self._order(
                    order_book_id,
                    min(quantity, position.sell_old_quantity),
                    SIDE.BUY,
                    POSITION_EFFECT.CLOSE,
                    style
                ))
                quantity -= position.sell_old_quantity
            if quantity <= 0:
                return orders
            # 平今仓
            if position.sell_today_quantity > 0:
                orders.append(self._order(
                    order_book_id,
                    min(quantity, position.sell_today_quantity),
                    SIDE.BUY,
                    POSITION_EFFECT.CLOSE_TODAY,
                    style
                ))
                quantity -= position.sell_today_quantity
            if quantity <= 0:
                return orders
            # 开多仓
            orders.append(self._order(
                order_book_id,
                quantity,
                SIDE.BUY,
                POSITION_EFFECT.OPEN,
                style
            ))
            return orders
        else:
            # 平昨仓
            quantity *= -1
            if position.buy_old_quantity > 0:
                orders.append(self._order(
                    order_book_id,
                    min(quantity, position.buy_old_quantity),
                    SIDE.SELL,
                    POSITION_EFFECT.CLOSE,
                    style
                ))
                quantity -= position.buy_old_quantity
            if quantity <= 0:
                return orders
            # 平今仓
            if position.buy_today_quantity > 0:
                orders.append(self._order(
                    order_book_id,
                    min(quantity, position.buy_today_quantity),
                    SIDE.SELL,
                    POSITION_EFFECT.CLOSE_TODAY,
                    style
                ))
                quantity -= position.buy_today_quantity
            if quantity <= 0:
                return orders
            # 开空仓
            orders.append(self._order(
                order_book_id,
                quantity,
                SIDE.SELL,
                POSITION_EFFECT.OPEN,
                style
            ))
            return orders

    # @apply_rules(verify_that('id_or_ins').is_valid_future(),
    #              verify_that('quantity').is_number().is_greater_or_equal_than(0),
    #              verify_that('side').is_in([SIDE.BUY, SIDE.SELL]),
    #              verify_that('position_effect').is_in([POSITION_EFFECT.OPEN, POSITION_EFFECT.CLOSE]),
    #              verify_that('style').is_instance_of((LimitOrder, MarketOrder, type(None))))
    def _order(self, id_or_ins, quantity, side, position_effect, style):
        if not isinstance(style, OrderStyle):
            raise RuntimeError
        if quantity < 0:
            raise RuntimeError
        if quantity == 0:
            user_system_log.warn(_(u"Order Creation Failed: Order amount is 0."))
            return None
        if isinstance(style, LimitOrder) and style.get_limit_price() <= 0:
            raise RQInvalidArgument(_(u"Limit order price should be positive"))

        order_book_id = self.assure_future_order_book_id(id_or_ins)
        env = Environment.get_instance()
        if env.config.base.run_type != RUN_TYPE.BACKTEST:
            if "88" in order_book_id:
                raise RQInvalidArgument(_(u"Main Future contracts[88] are not supported in paper trading."))
            if "99" in order_book_id:
                raise RQInvalidArgument(_(u"Index Future contracts[99] are not supported in paper trading."))

        price = env.get_last_price(order_book_id)
        if np.isnan(price):
            user_system_log.warn(
                _(u"Order Creation Failed: [{order_book_id}] No market data").format(order_book_id=order_book_id)
            )
            return

        quantity = int(quantity)

        position = self.positions[order_book_id]

        orders = []
        if position_effect == POSITION_EFFECT.CLOSE:
            if side == SIDE.BUY:
                # 如果平仓量大于持仓量，则 Warning 并 取消订单创建
                if quantity > position.sell_quantity:
                    user_system_log.warn(
                        _(u"Order Creation Failed: close amount {amount} is larger than position "
                          u"quantity {quantity}").format(amount=quantity, quantity=position.sell_quantity)
                    )
                    return []
                sell_old_quantity = position.sell_old_quantity
                if quantity > sell_old_quantity:
                    if sell_old_quantity != 0:
                        # 如果有昨仓，则创建一个 POSITION_EFFECT.CLOSE 的平仓单
                        orders.append(Order.__from_create__(
                            order_book_id,
                            sell_old_quantity,
                            side,
                            style,
                            POSITION_EFFECT.CLOSE
                        ))
                    # 剩下还有仓位，则创建一个 POSITION_EFFECT.CLOSE_TODAY 的平今单
                    orders.append(Order.__from_create__(
                        order_book_id,
                        quantity - sell_old_quantity,
                        side,
                        style,
                        POSITION_EFFECT.CLOSE_TODAY
                    ))
                else:
                    # 创建 POSITION_EFFECT.CLOSE 的平仓单
                    orders.append(Order.__from_create__(
                        order_book_id,
                        quantity,
                        side,
                        style,
                        POSITION_EFFECT.CLOSE
                    ))
            else:
                if quantity > position.buy_quantity:
                    user_system_log.warn(
                        _(u"Order Creation Failed: close amount {amount} is larger than position "
                          u"quantity {quantity}").format(amount=quantity, quantity=position.sell_quantity)
                    )
                    return []
                buy_old_quantity = position.buy_old_quantity
                if quantity > buy_old_quantity:
                    if buy_old_quantity != 0:
                        orders.append(Order.__from_create__(
                            order_book_id,
                            buy_old_quantity,
                            side,
                            style,
                            POSITION_EFFECT.CLOSE
                        ))
                    orders.append(Order.__from_create__(
                        order_book_id,
                        quantity - buy_old_quantity,
                        side,
                        style,
                        POSITION_EFFECT.CLOSE_TODAY
                    ))
                else:
                    orders.append(Order.__from_create__(
                        order_book_id,
                        quantity,
                        side,
                        style,
                        POSITION_EFFECT.CLOSE
                    ))
        else:
            orders.append(Order.__from_create__(
                order_book_id,
                quantity,
                side,
                style,
                position_effect
            ))

        if np.isnan(price) or price == 0:
            user_system_log.warn(
                _(u"Order Creation Failed: [{order_book_id}] No market data").format(order_book_id=order_book_id))
            for o in orders:
                o.mark_rejected(
                    _(u"Order Creation Failed: [{order_book_id}] No market data").format(
                        order_book_id=order_book_id))
            return orders

        for o in orders:
            if o.type == ORDER_TYPE.MARKET:
                o.set_frozen_price(price)
            if env.can_submit_order(self,o):
                env.broker.submit_order(self,o)

        # 向前兼容，如果创建的order_list 只包含一个订单的话，直接返回对应的订单，否则返回列表
        if len(orders) == 1:
            return orders[0]
        else:
            return orders

    # ------------------------------------ Abandon Property ------------------------------------

    @property
    def daily_holding_pnl(self):
        """
        [已弃用] 请使用 holding_pnl
        """
        user_system_log.warn(_(u"[abandon] {} is no longer used.").format('future_account.daily_holding_pnl'))
        return self.holding_pnl

    @property
    def daily_realized_pnl(self):
        """
        [已弃用] 请使用 realized_pnl
        """
        user_system_log.warn(_(u"[abandon] {} is no longer used.").format('future_account.daily_realized_pnl'))
        return self.realized_pnl
