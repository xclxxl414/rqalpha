from rqalpha.api import *


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "000001.XSHE"
    context.s2 = "000002.XSHE"
    update_universe([context.s1,context.s2])
    # 是否已发送了order
    context.id = 1


def before_trading(context):
    pass


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单
    # TODO: 开始编写你的算法吧！
    # print("prev_trading_dt:",context.prev_trading_dt)
    if 1 == context.id:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_target_percent(context.s2, 0)
        order_target_percent(context.s1, 1)
        context.id = 2
    else:
        order_target_percent(context.s1, 0)
        order_target_percent(context.s2, 1)
        context.id = 1
