#!/usr/bin/env python
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

<<<<<<< HEAD
import inspect
import re



def get_code_block(func):
    lines = inspect.getsourcelines(func)[0][1:]
    return "".join([re.sub(r'^    ', '', line) for line in lines])


def test_get_order():
    from rqalpha.api import order_shares, get_order

=======
from rqalpha.api import *

from ..utils import make_test_strategy_decorator

test_strategies = []

as_test_strategy = make_test_strategy_decorator({
        "base": {
            "start_date": "2016-12-01",
            "end_date": "2016-12-31",
            "frequency": "1d",
            "accounts": {
                "stock": 1000000,
                "future": 1000000,
            }
        },
        "extra": {
            "log_level": "error",
        },
        "mod": {
            "sys_progress": {
                "enabled": True,
                "show": True,
            },
        },
    }, test_strategies)


@as_test_strategy()
def test_get_order():
>>>>>>> upstream/master
    def init(context):
        context.s1 = '000001.XSHE'
        context.amount = 100

<<<<<<< HEAD
    def handle_bar(context, bar_dict):
=======
    def handle_bar(context, _):
>>>>>>> upstream/master
        order_id = order_shares(context.s1, context.amount, style=LimitOrder(9.5))
        order = get_order(order_id)
        assert order.order_book_id == context.s1
        assert order.quantity == context.amount
        assert order.unfilled_quantity + order.filled_quantity == order.quantity
<<<<<<< HEAD
test_get_order_code_new = get_code_block(test_get_order)


def test_get_open_order():
    from rqalpha.api import order_shares, get_open_orders, get_order

=======
    return init, handle_bar


@as_test_strategy()
def test_get_open_order():
>>>>>>> upstream/master
    def init(context):
        context.s1 = '000001.XSHE'
        context.limitprice = 8.9
        context.amount = 100
        context.counter = 0
        context.order_id = None

<<<<<<< HEAD
    def handle_bar(context, bar_dict):
=======
    def handle_bar(context, _):
>>>>>>> upstream/master
        context.counter += 1

        order = order_shares(context.s1, context.amount, style=LimitOrder(context.limitprice))
        context.order_id = order.order_id
<<<<<<< HEAD
        print('cash: ', context.portfolio.cash)
        print('check_get_open_orders done')
        print(order.order_id)
        # print(get_open_orders())
        print(get_open_orders())
        print(get_order(order.order_id))
        if context.counter == 2:
            assert order.order_id in get_open_orders()
        context.counter = 0
test_get_open_order_code_new = get_code_block(test_get_open_order)


def test_cancel_order():
    from rqalpha.api import order_shares, cancel_order, get_order

    def init(context):
        context.s1 = '000001.XSHE'
        context.limitprice = 8.59
        context.amount = 100

    def handle_bar(context, bar_dict):
        order_id = order_shares(context.s1, context.amount, style=LimitOrder(context.limitprice))
        cancel_order(order_id)
        order = get_order(order_id)
        assert order.order_book_id == context.s1
        assert order.filled_quantity == 0
        return order_id
        assert order.price == context.limitprice
test_cancel_order_code_new = get_code_block(test_cancel_order)


def test_update_universe():
    from rqalpha.api import update_universe, history_bars

=======
        if context.counter == 2:
            assert order.order_id in get_open_orders()
        context.counter = 0
    return init, handle_bar


@as_test_strategy()
def test_submit_order():
    def init(context):
        context.s1 = '000001.XSHE'
        context.amount = 100
        context.fired = False

    def handle_bar(context, bar_dict):
        if not context.fired:
            submit_order(context.s1, context.amount, SIDE.BUY, bar_dict[context.s1].limit_up * 0.99)
            context.fired = True
        if context.fired:
            assert context.portfolio.positions[context.s1].quantity == context.amount
    return init, handle_bar


@as_test_strategy()
def test_cancel_order():
    def init(context):
        context.s1 = '000001.XSHE'
        context.amount = 100

    def handle_bar(context, bar_dict):
        order = order_shares(context.s1, context.amount, style=LimitOrder(bar_dict[context.s1].limit_down))
        cancel_order(order)
        assert order.order_book_id == context.s1
        assert order.filled_quantity == 0
        assert order.price == bar_dict[context.s1].limit_down
        assert order.status == ORDER_STATUS.CANCELLED
    return init, handle_bar


@as_test_strategy()
def test_update_universe():
>>>>>>> upstream/master
    def init(context):
        context.s1 = '000001.XSHE'
        context.s2 = '600340.XSHG'
        context.order_count = 0
        context.amount = 100

<<<<<<< HEAD
    def handle_bar(context, bar_dict):
=======
    def handle_bar(context, _):
>>>>>>> upstream/master
        context.order_count += 1
        if context.order_count == 1:
            update_universe(context.s2)
            his = history_bars(context.s2, 5, '1d', 'close')
<<<<<<< HEAD
            print(sorted(his.tolist()))
            print(sorted([24.1, 23.71, 23.82, 23.93, 23.66]))
            assert sorted(his.tolist()) == sorted([26.06, 26.13, 26.54, 26.6, 26.86])
test_update_universe_code_new = get_code_block(test_update_universe)


def test_subscribe():
    from rqalpha.api import subscribe

=======
            assert sorted(his.tolist()) == sorted([26.06, 26.13, 26.54, 26.6, 26.86])
    return init, handle_bar


@as_test_strategy()
def test_subscribe():
>>>>>>> upstream/master
    def init(context):
        context.f1 = 'AU88'
        context.amount = 1
        subscribe(context.f1)

<<<<<<< HEAD
    def handle_bar(context, bar_dict):
        assert context.f1 in context.universe
test_subscribe_code_new = get_code_block(test_subscribe)


def test_unsubscribe():
    from rqalpha.api import subscribe, unsubscribe

=======
    def handle_bar(context, _):
        assert context.f1 in context.universe
    return init, handle_bar


@as_test_strategy()
def test_unsubscribe():
>>>>>>> upstream/master
    def init(context):
        context.f1 = 'AU88'
        context.amount = 1
        subscribe(context.f1)
        unsubscribe(context.f1)

<<<<<<< HEAD
    def handle_bar(context, bar_dict):
        assert context.f1 not in context.universe
test_unsubscribe_code_new = get_code_block(test_unsubscribe)


def test_get_yield_curve():
    from rqalpha.api import get_yield_curve

    def init(context):
        pass

    def handle_bar(context, bar_dict):
        df = get_yield_curve('20161101')
        assert df.iloc[0, 0] == 0.019923
        assert df.iloc[0, 6] == 0.021741
test_get_yield_curve_code_new = get_code_block(test_get_yield_curve)


def test_history_bars():
    from rqalpha.api import history_bars

    def init(context):
        context.s1 = '000001.XSHE'
        pass

    def handle_bar(context, bar_dict):
        return_list = history_bars(context.s1, 5, '1d', 'close')
        if str(context.now.date()) == '2016-12-29':
            assert return_list.tolist() == [9.08, 9.12, 9.08, 9.06, 9.08]
test_history_bars_code_new = get_code_block(test_history_bars)


def test_all_instruments():
    from rqalpha.api import all_instruments

    def init(context):
        pass

    def handle_bar(context, bar_dict):
=======
    def handle_bar(context, _):
        assert context.f1 not in context.universe
    return init, handle_bar


@as_test_strategy
def test_get_yield_curve():
    def handle_bar(_, __):
        df = get_yield_curve('20161101')
        assert df.iloc[0, 0] == 0.019923
        assert df.iloc[0, 6] == 0.021741
    return handle_bar


def test_history_bars():
    def handle_bar(context, _):
        return_list = history_bars(context.s1, 5, '1d', 'close')
        if str(context.now.date()) == '2016-12-29':
            assert return_list.tolist() == [9.08, 9.12, 9.08, 9.06, 9.08]
    return handle_bar


@as_test_strategy()
def test_all_instruments():
    def handle_bar(context, _):
>>>>>>> upstream/master
        date = context.now.replace(hour=0, minute=0, second=0)
        df = all_instruments('CS')
        assert (df['listed_date'] <= date).all()
        assert (df['de_listed_date'] >= date).all()
<<<<<<< HEAD
        assert all(not is_suspended(o) for o in df['order_book_id'])
=======
        # assert all(not is_suspended(o) for o in df['order_book_id'])
>>>>>>> upstream/master
        assert (df['type'] == 'CS').all()

        df1 = all_instruments('Stock')
        assert sorted(df['order_book_id']) == sorted(df1['order_book_id'])

        df2 = all_instruments('Future')

        assert (df2['type'] == 'Future').all()
        assert (df2['listed_date'] <= date).all()
        assert (df2['de_listed_date'] >= date).all()

        df3 = all_instruments(['Future', 'Stock'])
        assert sorted(list(df['order_book_id']) + list(df2['order_book_id'])) == sorted(df3['order_book_id'])
<<<<<<< HEAD

test_all_instruments_code_new = get_code_block(test_all_instruments)


def test_instruments_code():
    from rqalpha.api import instruments

    def init(context):
        context.s1 = '000001.XSHE'
        pass

    def handle_bar(context, bar_dict):
=======
    return handle_bar


@as_test_strategy()
def test_instruments_code():
    def init(context):
        context.s1 = '000001.XSHE'

    def handle_bar(context, _):
>>>>>>> upstream/master
        ins = instruments(context.s1)
        assert ins.sector_code_name == '金融'
        assert ins.symbol == '平安银行'
        assert ins.order_book_id == context.s1
        assert ins.type == 'CS'
<<<<<<< HEAD
test_instruments_code_new = get_code_block(test_instruments_code)


def test_sector():
    from rqalpha.api import sector

    def init(context):
        pass

    def handle_bar(context, bar_dict):
        assert len(sector('金融')) >= 180
test_sector_code_new = get_code_block(test_sector)


def test_industry():
    from rqalpha.api import industry, instruments

=======
    return init, handle_bar


@as_test_strategy()
def test_sector():
    def handle_bar(_, __):
        assert len(sector('金融')) >= 80, "sector('金融') 返回结果少于 80 个"
    return handle_bar


@as_test_strategy()
def test_industry():
>>>>>>> upstream/master
    def init(context):
        context.s1 = '000001.XSHE'
        context.s2 = '600340.XSHG'

<<<<<<< HEAD
    def handle_bar(context, bar_dict):
=======
    def handle_bar(context, _):
>>>>>>> upstream/master
        ins_1 = instruments(context.s1)
        ins_2 = instruments(context.s2)
        industry_list_1 = industry(ins_1.industry_name)
        industry_list_2 = industry(ins_2.industry_name)
        assert context.s1 in industry_list_1
        assert context.s2 in industry_list_2
<<<<<<< HEAD
test_industry_code_new = get_code_block(test_industry)


def test_get_trading_dates():
    from rqalpha.api import get_trading_dates
    import datetime

    def init(context):
=======
    return init, handle_bar


@as_test_strategy()
def test_get_trading_dates():
    import datetime

    def init(_):
>>>>>>> upstream/master
        trading_dates_list = get_trading_dates('2016-12-15', '2017-01-03')
        correct_dates_list = [datetime.date(2016, 12, 15), datetime.date(2016, 12, 16), datetime.date(2016, 12, 19),
                              datetime.date(2016, 12, 20), datetime.date(2016, 12, 21), datetime.date(2016, 12, 22),
                              datetime.date(2016, 12, 23), datetime.date(2016, 12, 26), datetime.date(2016, 12, 27),
                              datetime.date(2016, 12, 28), datetime.date(2016, 12, 29), datetime.date(2016, 12, 30),
                              datetime.date(2017, 1, 3)]
        assert sorted([item.strftime("%Y%m%d") for item in correct_dates_list]) == sorted(
            [item.strftime("%Y%m%d") for item
             in trading_dates_list])
<<<<<<< HEAD

    def handle_bar(context, bar_dict):
        pass
test_get_trading_dates_code_new = get_code_block(test_get_trading_dates)


def test_get_previous_trading_date():
    from rqalpha.api import get_previous_trading_date

    def init(context):
=======
    return init


@as_test_strategy()
def test_get_previous_trading_date():
    def init(_):
>>>>>>> upstream/master
        assert str(get_previous_trading_date('2017-01-03').date()) == '2016-12-30'
        assert str(get_previous_trading_date('2016-01-03').date()) == '2015-12-31'
        assert str(get_previous_trading_date('2015-01-03').date()) == '2014-12-31'
        assert str(get_previous_trading_date('2014-01-03').date()) == '2014-01-02'
        assert str(get_previous_trading_date('2010-01-03').date()) == '2009-12-31'
        assert str(get_previous_trading_date('2009-01-03').date()) == '2008-12-31'
        assert str(get_previous_trading_date('2005-01-05').date()) == '2005-01-04'
<<<<<<< HEAD

    def handle_bar(context, bar_dict):
        pass
test_get_previous_trading_date_code_new = get_code_block(test_get_previous_trading_date)


def test_get_next_trading_date():
    from rqalpha.api import get_next_trading_date

    def init(context):
        assert str(get_next_trading_date('2017-01-03').date()) == '2017-01-04'
        assert str(get_next_trading_date('2007-01-03').date()) == '2007-01-04'

    def handle_bar(context, bar_dict):
        pass
test_get_next_trading_date_code_new = get_code_block(test_get_next_trading_date)


def test_get_dividend():
    from rqalpha.api import get_dividend

    def init(context):
        pass

    def handle_bar(context, bar_dict):
=======
    return init


@as_test_strategy()
def test_get_next_trading_date():
    def init(_):
        assert str(get_next_trading_date('2017-01-03').date()) == '2017-01-04'
        assert str(get_next_trading_date('2007-01-03').date()) == '2007-01-04'
    return init


@as_test_strategy()
def test_get_dividend():
    def handle_bar(_, __):
>>>>>>> upstream/master
        df = get_dividend('000001.XSHE', start_date='20130104')
        df_to_assert = df[df['book_closure_date'] == 20130619]
        assert len(df) >= 4
        assert df_to_assert[0]['dividend_cash_before_tax'] == 1.7
        assert df_to_assert[0]['payable_date'] == 20130620
<<<<<<< HEAD
test_get_dividend_code_new = get_code_block(test_get_dividend)

# =================== 以下把代码写为纯字符串 ===================

test_get_order_code = '''
from rqalpha.api import order_shares, get_order
def init(context):
    context.s1 = '000001.XSHE'
    context.amount = 100

def handle_bar(context, bar_dict):
    assert 1 == 2
    order_id = order_shares(context.s1, context.amount, style=LimitOrder(9.5))
    order = get_order(order_id)
    assert order.order_book_id == context.s1
    assert order.quantity == context.amount
    assert order.unfilled_quantity + order.filled_quantity == order.quantity

'''

test_get_open_order_code = '''
from rqalpha.api import order_shares, get_open_orders
def init(context):
    context.s1 = '000001.XSHE'
    context.limitprice = 8.9
    context.amount = 100
    context.counter = 0
    context.order_id = None

def handle_bar(context, bar_dict):
    context.counter += 1

    order = order_shares(context.s1, context.amount, style=LimitOrder(context.limitprice))
    context.order_id = order.order_id
    print('cash: ', context.portfolio.cash)
    print('check_get_open_orders done')
    print(order.order_id)
    # print(get_open_orders())
    print(get_open_orders())
    print(get_order(order.order_id))
    if context.counter == 2:
        assert order.order_id in get_open_orders()
    context.counter = 0
'''

test_cancel_order_code = '''
from rqalpha.api import order_shares, cancel_order, get_order
def init(context):
    context.s1 = '000001.XSHE'
    context.limitprice = 8.59
    context.amount = 100

def handle_bar(context, bar_dict):
    order_id = order_shares(context.s1, context.amount, style=LimitOrder(context.limitprice))
    cancel_order(order_id)
    order = get_order(order_id)
    assert order.order_book_id == context.s1
    assert order.filled_quantity == 0
    return order_id
    assert order.price == context.limitprice
'''

test_update_universe_code = '''
from rqalpha.api import update_universe, history_bars
def init(context):
    context.s1 = '000001.XSHE'
    context.s2 = '600340.XSHG'
    context.order_count = 0
    context.amount = 100

def handle_bar(context, bar_dict):
    context.order_count += 1
    if context.order_count == 1:
        update_universe(context.s2)
        his = history_bars(context.s2, 5, '1d', 'close')
        print(sorted(his.tolist()))
        print(sorted([24.1, 23.71, 23.82, 23.93, 23.66]))
        assert sorted(his.tolist()) == sorted([26.06, 26.13, 26.54, 26.6, 26.86])
'''

test_subscribe_code = '''
from rqalpha.api import subscribe
def init(context):
    context.f1 = 'AU88'
    context.amount = 1
    subscribe(context.f1)

def handle_bar(context, bar_dict):
    assert context.f1 in context.universe
'''

test_unsubscribe_code = '''
from rqalpha.api import subscribe, unsubscribe
def init(context):
    context.f1 = 'AU88'
    context.amount = 1
    subscribe(context.f1)
    unsubscribe(context.f1)

def handle_bar(context, bar_dict):
    assert context.f1 not in context.universe
'''

test_get_yield_curve_code = '''
from rqalpha.api import get_yield_curve
def init(context):
    pass

def handle_bar(context, bar_dict):
    df = get_yield_curve('20161101')
    assert df.iloc[0, 0] == 0.019923
    assert df.iloc[0, 6] == 0.021741
'''

test_history_bars_code = '''
from rqalpha.api import history_bars
def init(context):
    context.s1 = '000001.XSHE'
    pass

def handle_bar(context, bar_dict):
    return_list = history_bars(context.s1, 5, '1d', 'close')
    if str(context.now.date()) == '2016-12-29':
        assert return_list.tolist() == [9.08, 9.1199, 9.08, 9.06, 9.08]
'''

test_all_instruments_code = '''
from rqalpha.api import all_instruments
def init(context):
    pass

def handle_bar(context, bar_dict):
    df = all_instruments('FenjiA')
    df_to_assert = df.loc[df['order_book_id'] == '150247.XSHE']
    assert df_to_assert.iloc[0, 0] == 'CMAJ'
    assert df_to_assert.iloc[0, 7] == '工银中证传媒A'
    assert all_instruments().shape >= (8000, 4)
    assert all_instruments('CS').shape >= (3000, 16)
    assert all_instruments('ETF').shape >= (120, 9)
    assert all_instruments('LOF').shape >= (130, 9)
    assert all_instruments('FenjiMu').shape >= (10, 9)
    assert all_instruments('FenjiA').shape >= (120, 9)
    assert all_instruments('FenjiB').shape >= (140, 9)
    assert all_instruments('INDX').shape >= (500, 8)
    assert all_instruments('Future').shape >= (3500, 16)
'''

test_instruments_code = '''
from rqalpha.api import instruments
def init(context):
    context.s1 = '000001.XSHE'
    pass

def handle_bar(context, bar_dict):
    print('hello')
    ins = instruments(context.s1)
    assert ins.sector_code_name == '金融'
    assert ins.symbol == '平安银行'
    assert ins.order_book_id == context.s1
    assert ins.type == 'CS'
    print('world')
'''

test_sector_code = '''
from rqalpha.api import sector
def init(context):
    pass

def handle_bar(context, bar_dict):
    assert len(sector('金融')) >= 180
'''

test_industry_code = '''
from rqalpha.api import industry, instruments
def init(context):
    context.s1 = '000001.XSHE'
    context.s2 = '600340.XSHG'

def handle_bar(context, bar_dict):
    ins_1 = instruments(context.s1)
    ins_2 = instruments(context.s2)
    industry_list_1 = industry(ins_1.industry_name)
    industry_list_2 = industry(ins_2.industry_name)
    assert context.s1 in industry_list_1
    assert context.s2 in industry_list_2
'''

test_get_trading_dates_code = '''
from rqalpha.api import get_trading_dates
import datetime
def init(context):
    pass

def handle_bar(context, bar_dict):
    trading_dates_list = get_trading_dates('2016-12-15', '2017-01-03')
    correct_dates_list = [datetime.date(2016, 12, 15), datetime.date(2016, 12, 16), datetime.date(2016, 12, 19),
                          datetime.date(2016, 12, 20), datetime.date(2016, 12, 21), datetime.date(2016, 12, 22),
                          datetime.date(2016, 12, 23), datetime.date(2016, 12, 26), datetime.date(2016, 12, 27),
                          datetime.date(2016, 12, 28), datetime.date(2016, 12, 29), datetime.date(2016, 12, 30),
                          datetime.date(2017, 1, 3)]
    assert sorted([item.strftime("%Y%m%d") for item in correct_dates_list]) == sorted([item.strftime("%Y%m%d") for item
                                                                                       in trading_dates_list])
'''

test_get_previous_trading_date_code = '''
from rqalpha.api import get_previous_trading_date
def init(context):
    pass

def handle_bar(context, bar_dict):
    assert str(get_previous_trading_date('2017-01-03').date()) == '2016-12-30'
    assert str(get_previous_trading_date('2016-01-03').date()) == '2015-12-31'
    assert str(get_previous_trading_date('2015-01-03').date()) == '2014-12-31'
    assert str(get_previous_trading_date('2014-01-03').date()) == '2014-01-02'
    assert str(get_previous_trading_date('2010-01-03').date()) == '2009-12-31'
    assert str(get_previous_trading_date('2009-01-03').date()) == '2008-12-31'
    assert str(get_previous_trading_date('2005-01-05').date()) == '2005-01-04'
'''

test_get_next_trading_date_code = '''

from rqalpha.api import get_next_trading_date
def init(context):
    pass

def handle_bar(context, bar_dict):
    assert str(get_next_trading_date('2017-01-03').date()) == '2017-01-04'
    assert str(get_next_trading_date('2007-01-03').date()) == '2007-01-04'

'''

test_get_dividend_code = '''
from rqalpha.api import get_dividend
import pandas
def init(context):
    pass

def handle_bar(context, bar_dict):
    df = get_dividend('000001.XSHE', start_date='20130104')
    df_to_assert = df.loc[df['book_closure_date'] == '	2013-06-19']
    assert df.shape >= (4, 5)
    assert df_to_assert.iloc[0, 1] == 0.9838
    assert df_to_assert.iloc[0, 3] == pandas.tslib.Timestamp('2013-06-20 00:00:00')
'''
=======
    return handle_bar


@as_test_strategy()
def test_current_snapshot():
    def handle_bar(_, bar_dict):
        snapshot = current_snapshot('000001.XSHE')
        bar = bar_dict['000001.XSHE']

        assert snapshot.last == bar.close
        for field in (
            "open", "high", "low", "prev_close", "volume", "total_turnover", "order_book_id", "datetime",
            "limit_up", "limit_down"
        ):
            assert getattr(bar, field) == getattr(snapshot, field), "snapshot.{} = {}, bar.{} = {}".format(
                field, getattr(snapshot, field), field, getattr(bar, field)
            )
    return handle_bar


@as_test_strategy()
def test_get_position():

    def assert_position(pos, obid, dir, today_quantity, old_quantity, avg_price):
        assert pos.order_book_id == obid
        assert pos.direction == dir, "Direction of {} is expected to be {} instead of {}".format(
            pos.order_book_id, dir, pos.direction
        )
        assert pos.today_quantity == today_quantity
        assert pos.old_quantity == old_quantity
        assert pos.quantity == (today_quantity + old_quantity)
        assert pos.avg_price == avg_price

    def init(context):
        context.counter = 0
        context.expected_avg_price = None

    def handle_bar(context, bar_dict):
        context.counter += 1

        if context.counter == 1:
            order_shares("000001.XSHE", 300)
            context.expected_avg_price = bar_dict["000001.XSHE"].close
        elif context.counter == 5:
            order_shares("000001.XSHE", -100)
        elif context.counter == 10:
            sell_open("RB1701", 5)
            context.expected_avg_price = bar_dict["RB1701"].close
        elif context.counter == 15:
            buy_close("RB1701", 2)

        if context.counter == 1:
            pos = get_positions()[0]
            assert_position(pos, "000001.XSHE", POSITION_DIRECTION.LONG, 300, 0, context.expected_avg_price)
        elif 1 < context.counter < 5:
            pos = get_positions()[0]
            assert_position(pos, "000001.XSHE", POSITION_DIRECTION.LONG, 0, 300, context.expected_avg_price)
        elif 5 <= context.counter < 10:
            pos = get_position("000001.XSHE", POSITION_DIRECTION.LONG)
            assert_position(pos, "000001.XSHE", POSITION_DIRECTION.LONG, 0, 200, context.expected_avg_price)
        elif context.counter == 10:
            pos = get_position("RB1701", POSITION_DIRECTION.SHORT)
            assert_position(pos, "RB1701", POSITION_DIRECTION.SHORT, 5, 0, context.expected_avg_price)
        elif 10 < context.counter < 15:
            pos = get_position("RB1701", POSITION_DIRECTION.SHORT)
            assert_position(pos, "RB1701", POSITION_DIRECTION.SHORT, 0, 5, context.expected_avg_price)
        elif context.counter >= 15:
            pos = get_position("RB1701", POSITION_DIRECTION.SHORT)
            assert_position(pos, "RB1701", POSITION_DIRECTION.SHORT, 0, 3, context.expected_avg_price)

    return init, handle_bar
>>>>>>> upstream/master
