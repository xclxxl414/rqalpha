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

import six
import datetime
from collections import defaultdict

from rqalpha.model.base_account import BaseAccount
from rqalpha.events import EVENT
from rqalpha.environment import Environment
from rqalpha.utils.logger import user_system_log
from rqalpha.utils.i18n import gettext as _
from rqalpha.const import SIDE, DEFAULT_ACCOUNT_TYPE

from decimal import Decimal, getcontext

import six
import numpy as np

from rqalpha.api.api_base import decorate_api_exc, instruments, cal_style, register_api
from rqalpha.const import DEFAULT_ACCOUNT_TYPE, EXECUTION_PHASE, SIDE, ORDER_TYPE
from rqalpha.environment import Environment
from rqalpha.execution_context import ExecutionContext
from rqalpha.model.instrument import Instrument
from rqalpha.model.order import Order, OrderStyle, MarketOrder, LimitOrder
from rqalpha.utils.arg_checker import apply_rules, verify_that
# noinspection PyUnresolvedReferences
from rqalpha.utils.exception import patch_user_exc, RQInvalidArgument
from rqalpha.utils.i18n import gettext as _
from rqalpha.utils.logger import user_system_log
# noinspection PyUnresolvedReferences
from rqalpha.utils.scheduler import market_close, market_open
# noinspection PyUnresolvedReferences
from rqalpha.utils import scheduler
from ..api.api_stock import assure_stock_order_book_id,downsize_amount
# 使用Decimal 解决浮点数运算精度问题
getcontext().prec = 10



class StockAccount(BaseAccount):

    __abandon_properties__ = []

    def __init__(self,name, total_cash, positions, backward_trade_set=set(), dividend_receivable=None, register_event=True):
        super(StockAccount, self).__init__(name,total_cash, positions, backward_trade_set, register_event)
        self._dividend_receivable = dividend_receivable if dividend_receivable else {}

    def register_event(self):
        event_bus = Environment.get_instance().event_bus
        event_bus.add_listener(EVENT.TRADE, self._on_trade)
        event_bus.add_listener(EVENT.ORDER_PENDING_NEW, self._on_order_pending_new)
        event_bus.add_listener(EVENT.ORDER_CREATION_REJECT, self._on_order_unsolicited_update)
        event_bus.add_listener(EVENT.ORDER_UNSOLICITED_UPDATE, self._on_order_unsolicited_update)
        event_bus.add_listener(EVENT.ORDER_CANCELLATION_PASS, self._on_order_unsolicited_update)
        event_bus.add_listener(EVENT.PRE_BEFORE_TRADING, self._before_trading)
        event_bus.add_listener(EVENT.SETTLEMENT, self._on_settlement)
        if self.AGGRESSIVE_UPDATE_LAST_PRICE:
            event_bus.add_listener(EVENT.BAR, self._update_last_price)
            event_bus.add_listener(EVENT.TICK, self._update_last_price)

    def get_state(self):
        return {
            'positions': {
                order_book_id: position.get_state()
                for order_book_id, position in six.iteritems(self._positions)
            },
            'frozen_cash': self._frozen_cash,
            'total_cash': self._total_cash,
            'backward_trade_set': list(self._backward_trade_set),
            'dividend_receivable': self._dividend_receivable,
            'transaction_cost': self._transaction_cost,
        }

    def set_state(self, state):
        self._frozen_cash = state['frozen_cash']
        self._total_cash = state['total_cash']
        self._backward_trade_set = set(state['backward_trade_set'])
        self._dividend_receivable = state['dividend_receivable']
        self._transaction_cost = state['transaction_cost']
        self._positions.clear()
        for order_book_id, v in six.iteritems(state['positions']):
            position = self._positions.get_or_create(order_book_id)
            position.set_state(v)

    def fast_forward(self, orders, trades=list()):
        # 计算 Positions
        for trade in trades:
            if trade.exec_id in self._backward_trade_set:
                continue
            self._apply_trade(trade)
        # 计算 Frozen Cash
        self._frozen_cash = 0
        frozen_quantity = defaultdict(int)
        for o in orders:
            if o.is_final():
                continue
            if o.side == SIDE.BUY:
                self._frozen_cash += o.frozen_price * o.unfilled_quantity
            else:
                frozen_quantity[o.order_book_id] += o.unfilled_quantity
        for order_book_id, position in six.iteritems(self._positions):
            position.reset_frozen(frozen_quantity[order_book_id])

    def _on_trade(self, event):
        if event.account != self:
            return
        self._apply_trade(event.trade)

    def _apply_trade(self, trade):
        if trade.exec_id in self._backward_trade_set:
            return

        position = self._positions.get_or_create(trade.order_book_id)
        position.apply_trade(trade)
        self._transaction_cost += trade.transaction_cost
        self._total_cash -= trade.transaction_cost
        if trade.side == SIDE.BUY:
            self._total_cash -= trade.last_quantity * trade.last_price
            self._frozen_cash -= trade.frozen_price * trade.last_quantity
        else:
            self._total_cash += trade.last_price * trade.last_quantity
        self._backward_trade_set.add(trade.exec_id)

    def _on_order_pending_new(self, event):
        if event.account != self:
            return
        order = event.order
        position = self._positions.get(order.order_book_id, None)
        if position is not None:
            position.on_order_pending_new_(order)
        if order.side == SIDE.BUY:
            order_value = order.frozen_price * order.quantity
            self._frozen_cash += order_value

    def _on_order_unsolicited_update(self, event):
        if event.account != self:
            return

        order = event.order
        position = self._positions.get_or_create(order.order_book_id)
        position.on_order_cancel_(order)
        if order.side == SIDE.BUY:
            unfilled_value = order.unfilled_quantity * order.frozen_price
            self._frozen_cash -= unfilled_value

    def _before_trading(self, event):
        trading_date = Environment.get_instance().trading_dt.date()
        last_date = Environment.get_instance().data_proxy.get_previous_trading_date(trading_date)
        self._handle_dividend_book_closure(last_date)
        self._handle_dividend_payable(trading_date)
        self._handle_split(trading_date)

    def _on_settlement(self, event):
        env = Environment.get_instance()
        for position in list(self._positions.values()):
            order_book_id = position.order_book_id
            if position.is_de_listed() and position.quantity != 0:
                if env.config.validator.cash_return_by_stock_delisted:
                    self._total_cash += position.market_value
                user_system_log.warn(
                    _(u"{order_book_id} is expired, close all positions by system").format(order_book_id=order_book_id)
                )
                self._positions.pop(order_book_id, None)
            elif position.quantity == 0:
                self._positions.pop(order_book_id, None)
            else:
                position.apply_settlement()

        self._transaction_cost = 0
        self._backward_trade_set.clear()

    def _update_last_price(self, event):
        for position in self._positions.values():
            position.update_last_price()

    @property
    def type(self):
        return DEFAULT_ACCOUNT_TYPE.STOCK.name

    def _handle_dividend_payable(self, trading_date):
        to_be_removed = []
        for order_book_id, dividend in six.iteritems(self._dividend_receivable):
            if dividend['payable_date'] == trading_date:
                to_be_removed.append(order_book_id)
                self._total_cash += dividend['quantity'] * dividend['dividend_per_share']
        for order_book_id in to_be_removed:
            del self._dividend_receivable[order_book_id]

    @staticmethod
    def _int_to_date(d):
        r, d = divmod(d, 100)
        y, m = divmod(r, 100)
        return datetime.date(year=y, month=m, day=d)

    def _handle_dividend_book_closure(self, trading_date):
        for order_book_id, position in six.iteritems(self._positions):
            if position.quantity == 0:
                continue

            dividend = Environment.get_instance().data_proxy.get_dividend_by_book_date(order_book_id, trading_date)
            if dividend is None:
                continue

            dividend_per_share = dividend['dividend_cash_before_tax'] / dividend['round_lot']
            position.dividend_(dividend_per_share)

            config = Environment.get_instance().config
            if config.extra.dividend_reinvestment:
                last_price = Environment.get_instance().data_proxy.get_bar(order_book_id, trading_date).close
                shares = position.quantity * dividend_per_share / last_price
                position._quantity += shares
            else:
                self._dividend_receivable[order_book_id] = {
                    'quantity': position.quantity,
                    'dividend_per_share': dividend_per_share,
                    'payable_date': self._int_to_date(dividend['payable_date']),
                }

    def _handle_split(self, trading_date):
        data_proxy = Environment.get_instance().data_proxy
        for order_book_id, position in six.iteritems(self._positions):
            ratio = data_proxy.get_split_by_ex_date(order_book_id, trading_date)
            if ratio is None:
                continue
            position.split_(ratio)

    @property
    def total_value(self):
        return self.market_value + self._total_cash + self.dividend_receivable

    @property
    def dividend_receivable(self):
        """
        [float] 投资组合在分红现金收到账面之前的应收分红部分。具体细节在分红部分
        """
        return sum(d['quantity'] * d['dividend_per_share'] for d in six.itervalues(self._dividend_receivable))

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
        orders = self.order_shares(order_book_id, quantity, style=style)

        if isinstance(orders, Order):
            return [orders]
        return orders

    # @apply_rules(verify_that('order_book_id').is_valid_stock(),
    #              verify_that('quantity').is_number(),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order_to(self,order_book_id, quantity, price=None, style=None):
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
        quantity = quantity - position.quantity
        orders = self.order_shares(order_book_id, quantity, style=style)

        if isinstance(orders, Order):
            return [orders]
        return orders

    # @apply_rules(verify_that('id_or_ins').is_valid_stock(),
    #              verify_that('percent').is_number().is_greater_or_equal_than(-1).is_less_or_equal_than(1),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order_pct(self, id_or_ins, percent, price=None, style=None):
        """
        发送一个等于目前投资组合价值（市场价值和目前现金的总和）一定百分比的买/卖单，正数代表买，负数代表卖。股票的股数总是会被调整成对应的一手的股票数的倍数（1手是100股）。百分比是一个小数，并且小于或等于1（<=100%），0.5表示的是50%.需要注意，如果资金不足，该API将不会创建发送订单。

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str`

        :param float percent: 占有现有的投资组合价值的百分比。正数表示买入，负数表示卖出。

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object

        :example:

        .. code-block:: python

            #买入等于现有投资组合50%价值的平安银行股票。如果现在平安银行的股价是￥10/股并且现在的投资组合总价值是￥2000，那么将会买入200股的平安银行股票。（不包含交易成本和滑点的损失）：
            order_percent('000001.XSHG', 0.5)
        """
        if percent < -1 or percent > 1:
            raise RQInvalidArgument(_(u"percent should between -1 and 1"))
        style = cal_style(price, style)
        return self.order_value(id_or_ins, self.total_value * percent, style=style)

    # @apply_rules(verify_that('id_or_ins').is_valid_stock(),
    #              verify_that('percent').is_number().is_greater_or_equal_than(0).is_less_or_equal_than(1),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order_pct_to(self, id_or_ins, percent, price=None, style=None):
        """
        买入/卖出证券以自动调整该证券的仓位到占有一个指定的投资组合的目标百分比。

        *   如果投资组合中没有任何该证券的仓位，那么会买入等于现在投资组合总价值的目标百分比的数目的证券。
        *   如果投资组合中已经拥有该证券的仓位，那么会买入/卖出目标百分比和现有百分比的差额数目的证券，最终调整该证券的仓位占据投资组合的比例至目标百分比。

        其实我们需要计算一个position_to_adjust (即应该调整的仓位)

        `position_to_adjust = target_position - current_position`

        投资组合价值等于所有已有仓位的价值和剩余现金的总和。买/卖单会被下舍入一手股数（A股是100的倍数）的倍数。目标百分比应该是一个小数，并且最大值应该<=1，比如0.5表示50%。

        如果position_to_adjust 计算之后是正的，那么会买入该证券，否则会卖出该证券。 需要注意，如果资金不足，该API将不会创建发送订单。

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str` | List[:class:`~Instrument`] | List[`str`]

        :param float percent: 仓位最终所占投资组合总价值的目标百分比。

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object

        :example:

        .. code-block:: python

            #如果投资组合中已经有了平安银行股票的仓位，并且占据目前投资组合的10%的价值，那么以下代码会买入平安银行股票最终使其占据投资组合价值的15%：
            order_target_percent('000001.XSHE', 0.15)
        """
        if percent < 0 or percent > 1:
            raise RQInvalidArgument(_(u"percent should between 0 and 1"))
        order_book_id = assure_stock_order_book_id(id_or_ins)
        style = cal_style(price, style)
        position = self.positions[order_book_id]
        if percent == 0:
            return self._sell_all_stock(order_book_id, position.sellable, style)
        return self.order_value(order_book_id, self.total_value * percent - position.market_value, style=style)

    # @apply_rules(verify_that('id_or_ins').is_valid_stock(),
    #              verify_that('quantity').is_number(),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order_lots(self, id_or_ins, quantity, price=None, style=None):
        """
        指定手数发送买/卖单。如有需要落单类型当做一个参量传入，如果忽略掉落单类型，那么默认是市价单（market order）。

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str`

        :param int quantity: 下单量, 正数代表买入，负数代表卖出。将会根据一手xx股来向下调整到一手的倍数，比如中国A股就是调整成100股的倍数。

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object

        :example:

        .. code-block:: python

            #买入20手的平安银行股票，并且发送市价单：
            order_lots('000001.XSHE', 20)
            #买入10手平安银行股票，并且发送限价单，价格为￥10：
            order_lots('000001.XSHE', 10, style=LimitOrder(10))

        """
        order_book_id = assure_stock_order_book_id(id_or_ins)

        round_lot = int(Environment.get_instance().get_instrument(order_book_id).round_lot)

        style = cal_style(price, style)

        return self.order_shares(id_or_ins, quantity * round_lot, style=style)

    # @apply_rules(verify_that('id_or_ins').is_valid_stock(),
    #              verify_that('cash_amount').is_number(),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order_value(self, id_or_ins, cash_amount, price=None, style=None):
        """
        使用想要花费的金钱买入/卖出股票，而不是买入/卖出想要的股数，正数代表买入，负数代表卖出。股票的股数总是会被调整成对应的100的倍数（在A中国A股市场1手是100股）。当您提交一个卖单时，该方法代表的意义是您希望通过卖出该股票套现的金额。如果金额超出了您所持有股票的价值，那么您将卖出所有股票。需要注意，如果资金不足，该API将不会创建发送订单。

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str`

        :param float cash_amount: 需要花费现金购买/卖出证券的数目。正数代表买入，负数代表卖出。

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object

        :example:

        .. code-block:: python

            #买入价值￥10000的平安银行股票，并以市价单发送。如果现在平安银行股票的价格是￥7.5，那么下面的代码会买入1300股的平安银行，因为少于100股的数目将会被自动删除掉：
            order_value('000001.XSHE', 10000)
            #卖出价值￥10000的现在持有的平安银行：
            order_value('000001.XSHE', -10000)

        """

        style = cal_style(price, style)

        if isinstance(style, LimitOrder):
            if style.get_limit_price() <= 0:
                raise RQInvalidArgument(_(u"Limit order price should be positive"))

        order_book_id = assure_stock_order_book_id(id_or_ins)
        env = Environment.get_instance()

        price = env.get_last_price(order_book_id)
        if np.isnan(price):
            user_system_log.warn(
                _(u"Order Creation Failed: [{order_book_id}] No market data").format(order_book_id=order_book_id))
            return

        if price == 0:
            return self.order_shares(order_book_id, 0, style)

        round_lot = int(env.get_instrument(order_book_id).round_lot)

        if cash_amount > 0:
            cash_amount = min(cash_amount, self.cash)

        if isinstance(style, MarketOrder):
            amount = int(Decimal(cash_amount) / Decimal(price) / Decimal(round_lot)) * round_lot
        else:
            amount = int(Decimal(cash_amount) / Decimal(style.get_limit_price()) / Decimal(round_lot)) * round_lot

        # if the cash_amount is larger than you current security’s position,
        # then it will sell all shares of this security.

        position = self.positions[order_book_id]
        amount = downsize_amount(amount, position)

        return self.order_shares(order_book_id, amount, style=style)

    # @apply_rules(verify_that('id_or_ins').is_valid_stock(),
    #              verify_that('cash_amount').is_number(),
    #              verify_that('style').is_instance_of((MarketOrder, LimitOrder, type(None))))
    def order_value_to(self, id_or_ins, cash_amount, price=None, style=None):
        """
        买入/卖出并且自动调整该证券的仓位到一个目标价值。如果还没有任何该证券的仓位，那么会买入全部目标价值的证券。如果已经有了该证券的仓位，则会买入/卖出调整该证券的现在仓位和目标仓位的价值差值的数目的证券。需要注意，如果资金不足，该API将不会创建发送订单。

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str` | List[:class:`~Instrument`] | List[`str`]

        :param float cash_amount: 最终的该证券的仓位目标价值。

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object

        :example:

        .. code-block:: python

            #如果现在的投资组合中持有价值￥3000的平安银行股票的仓位并且设置其目标价值为￥10000，以下代码范例会发送价值￥7000的平安银行的买单到市场。（向下调整到最接近每手股数即100的倍数的股数）：
            order_target_value('000001.XSHE', 10000)
        """
        order_book_id = assure_stock_order_book_id(id_or_ins)
        position = self.positions[order_book_id]

        style = cal_style(price, style)
        if cash_amount == 0:
            return self._sell_all_stock(order_book_id, position.sellable, style)

        return self.order_value(order_book_id, cash_amount - position.market_value, style=style)

    def order_shares(self, id_or_ins, quantity, price=None, style=None):
        """
        落指定股数的买/卖单，最常见的落单方式之一。如有需要落单类型当做一个参量传入，如果忽略掉落单类型，那么默认是市价单（market order）。

        :param id_or_ins: 下单标的物
        :type id_or_ins: :class:`~Instrument` object | `str`

        :param int quantity: 下单量, 正数代表买入，负数代表卖出。将会根据一手xx股来向下调整到一手的倍数，比如中国A股就是调整成100股的倍数。

        :param float price: 下单价格，默认为None，表示 :class:`~MarketOrder`, 此参数主要用于简化 `style` 参数。

        :param style: 下单类型, 默认是市价单。目前支持的订单类型有 :class:`~LimitOrder` 和 :class:`~MarketOrder`
        :type style: `OrderStyle` object

        :return: :class:`~Order` object

        :example:

        .. code-block:: python

            #购买Buy 2000 股的平安银行股票，并以市价单发送：
            order_shares('000001.XSHE', 2000)
            #卖出2000股的平安银行股票，并以市价单发送：
            order_shares('000001.XSHE', -2000)
            #购买1000股的平安银行股票，并以限价单发送，价格为￥10：
            order_shares('000001.XSHG', 1000, style=LimitOrder(10))
        """
        if quantity == 0:
            # 如果下单量为0，则认为其并没有发单，则直接返回None
            return None
        style = cal_style(price, style)
        if isinstance(style, LimitOrder):
            if style.get_limit_price() <= 0:
                raise RQInvalidArgument(_(u"Limit order price should be positive"))
        order_book_id = assure_stock_order_book_id(id_or_ins)
        env = Environment.get_instance()

        price = env.get_last_price(order_book_id)
        if np.isnan(price):
            user_system_log.warn(
                _(u"Order Creation Failed: [{order_book_id}] No market data").format(order_book_id=order_book_id))
            return

        if quantity > 0:
            side = SIDE.BUY
        else:
            quantity = abs(quantity)
            side = SIDE.SELL

        round_lot = int(env.get_instrument(order_book_id).round_lot)

        try:
            quantity = int(Decimal(quantity) / Decimal(round_lot)) * round_lot
        except ValueError:
            quantity = 0

        r_order = Order.__from_create__(order_book_id, quantity, side, style, None)

        if price == 0:
            user_system_log.warn(
                _(u"Order Creation Failed: [{order_book_id}] No market data").format(order_book_id=order_book_id))
            r_order.mark_rejected(
                _(u"Order Creation Failed: [{order_book_id}] No market data").format(order_book_id=order_book_id))
            return r_order

        if quantity == 0:
            # 如果计算出来的下单量为0, 则不生成Order, 直接返回None
            # 因为很多策略会直接在handle_bar里面执行order_target_percent之类的函数，经常会出现下一个量为0的订单，如果这些订单都生成是没有意义的。
            r_order.mark_rejected(_(u"Order Creation Failed: 0 order quantity"))
            return r_order
        if r_order.type == ORDER_TYPE.MARKET:
            r_order.set_frozen_price(price)
        if env.can_submit_order(self,r_order):
            env.broker.submit_order(self,r_order)
        return r_order

    def _sell_all_stock(self, order_book_id, quantity, style):
        env = Environment.get_instance()
        order = Order.__from_create__(order_book_id, quantity, SIDE.SELL, style, None)
        if quantity == 0:
            order.mark_rejected(_(u"Order Creation Failed: 0 order quantity"))
            return order

        if env.can_submit_order(self,order):
            env.broker.submit_order(self,order)
        return order