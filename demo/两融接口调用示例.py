# encoding: utf-8
"""
@project = HtStragetyRunEnv
@file = mq_strategy_apitest
@author = 011048
@create_time = 2018/5/23 16:28
"""
from mquant_api import *
from mquant_struct import *

def timer_func(conetxt, interval, msg_type):
    """
    示例定时函数
    :param conetxt:
    :return:
    :remark:用户函数
    """
    print('enter timer func,inerval:%d' % interval)
    if interval == 7:
#         print('开始融资买入')
#         MarginTradeHandler.margincash_open('600060.SH',1000, LimitOrderStyle(9.57))
#         print('结束融资买入')
#         print('开始融资买入(市价)')
#         MarginTradeHandler.margincash_open('600060.SH',1000)
#         print('结束融资买入（市价）')
#         print('开始卖券还款')
#         MarginTradeHandler.margincash_close('600000.SH',1000, style=LimitOrderStyle(9.57))
#         print('结束卖券还款')
#         print('开始卖券还款(市价)')
#         MarginTradeHandler.margincash_close('600000.SH',1000)
#         print('结束卖券还款(市价)')
#
#         print('开始融券卖出')
#         MarginTradeHandler.marginsec_open('600000.SH',1000,style=LimitOrderStyle(10.57))
#         print('结束融券卖出')
#         print('开始融券卖出(市价)')
#         MarginTradeHandler.marginsec_open('600000.SH',1000)
#         print('结束融券卖出（市价）')
# #
# #
#         print('开始买券还券')
#         MarginTradeHandler.marginsec_open('600036.SH',100,style=LimitOrderStyle(10.57))
#         print('结束买券还券')
#         print('开始买券还券(市价)')
#         MarginTradeHandler.marginsec_open('600036.SH',100)
#         print('结束买券还券（市价）')
#         print('开始直接还券')
#         MarginTradeHandler.marginsec_direct_refund('000895.SZ',100)
#         print('结束直接还券')
#
#         print('开始直接还款')
#         MarginTradeHandler.margincash_direct_refund(1000.5)
#         print('结束直接还款')
#         print('开始担保品买入')
#         MarginTradeHandler.margin_trade(['600036.SH','000895.SZ'],[1000,-1000])
#         print('结束担保品买入')
        
        print('开始查询融资标的')
        print(MarginTradeHandler.get_margincash_stocks())
        print('结束查询融资标的')
        print('开始查询融券标的')
        print(MarginTradeHandler.get_marginsec_stocks())
        print('结束查询融券标的')

        print('开始查询担保券列表')
        print(MarginTradeHandler.get_assure_security_list())
        print('查询担保券列表结束')
        
        print('开始查询信用资产')
        margin_assert = MarginTradeHandler.get_margin_assert()
        if margin_assert:
            print(margin_assert.cash_asset,margin_assert.security_market_value,margin_assert.assure_asset,margin_assert.available_margin)
            
        print('开始查询信用合约')
        contract_list = MarginTradeHandler.get_margin_contract()
        if contract_list and len(contract_list) > 0:
            print('查询返回信用合约数量：', len(contract_list), '合约编号列表：', contract_list.keys())
            
    elif interval == 10:
        print('开始查询全部成交')
        trade_deals = get_trades(only_this_inst=False)
        print('查询获取到%d条成交数据' % len(trade_deals))
        order_list = get_orders(only_this_inst=False)
        print('查询所有订单返回%d条数据' % len(order_list))


def strategy_params():
    """
    策略可自定义运行参数，启动策略时会写入到context对象的run_params字段内
    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现
    """
    # 示例如下：
    dict_params = {
        '证券代码': {'value': '601688.SH/000002.SZ', 'desc': '交易标的'},  # 'desc'字段可填写，也可不填写
        '买入价格': {'value': '17.50/27.50'},
        '卖出价格': {'value': '18.50/28.00'},
        '撤单时间间隔':{'value': 10}
    }
    return dict_params


def initialize(context):
    """
    策略初始化，启动策略时调用，用户可在初始化函数中订阅行情、设置标的、设置定时处理函数等
    该函数中允许读取文件，除此之外的其他函数禁止读取文件
    :param context:
    :return:
    :remark:必须实现
    """
    run_timely(timer_func, 7)  # 注册一个3s的定时函数，用于下单
    

def handle_tick(context, tick, msg_type):
    """
    实时行情接收函数
    :param context:
    :param tick: Tick对象
    :return:
    :remark:可选实现
    """

#    print('recv tick msg', tick.current, tick.code, tick.datetime, datetime.datetime.now())    
    #判断如果当前价超过卖出价，则卖出，如果低于买入价则买入
    symbol = normalize_code_jq_to_mquant(tick.code)
    # if symbol in g.security_list:
    #     if float(g.buy_dict[symbol]) > tick.current:
    #         log.debug('开始买入证券：%s' % symbol)
    #         order(symbol, 1000)
    #     elif float(g.sell_dict[symbol]) < tick.current:
    #         log.debug('开始卖出证券：%s' % symbol)
    #         order(symbol, -1000)


def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:
    :return:
    :remark:可选实现
    """
    print('on_strategy_end')
