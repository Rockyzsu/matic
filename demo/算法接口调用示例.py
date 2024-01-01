# encoding: utf-8
"""
@project = HtStragetyRunEnv
@file = 算法接口调用示例
@author = 011048
@create_time = 2019/3/12 14:31
"""
from mquant_api import *
from mquant_struct import *
import datetime


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
        '撤单时间间隔': {'value': 10}
    }
    return dict_params


def timer_func(context, interval, msg_type):
    """
    定时处理函数
    :param interval:
    :return:
    """
    g.inst_list = AlgoTradeHandler.get_instance_id_list()

    
    for inst_id in g.inst_list:
        inst_info = AlgoTradeHandler.get_instance_info(inst_id)
        if inst_info is not None:

            
            if inst_info.status == AlgoInstanceStatus.RUNNING:
                print('查询实例信息返回：', inst_info.__dict__)
                if inst_info.symbol_info is not None:
                    for symbol_info in inst_info.symbol_info:
                        print('标的详情：', symbol_info.__dict__)
#                    AlgoTradeHandler.stop_instance(inst_info.inst_id)
#                    break


def initialize(context):
    """
    初始化
    :param context:
    :return:
    """
#    run_timely(timer_func, -1, (datetime.datetime.now() +datetime.timedelta(seconds=3)).strftime('%H:%M:%S'))  # 注册一个10s的定时函数，定时查询算法实例状态
    run_timely(timer_func, 10, (datetime.datetime.now() +datetime.timedelta(seconds=3)).strftime('%H:%M:%S'))
    g.inst_list = []  # 存储算法实例列表

    # submit_algo_instance(context.run_params['证券代码'].strip('/').split('/'))


def submit_algo_instance(security_list):
    """
    提交算法实例
    :param security_list:
    :return:
    """
    algo_params = SplitOrderAlgoParam()
    algo_params.algo_type = AlgoType.AITWAP
    algo_params.start_time = datetime.datetime.now()
    algo_params.end_time = datetime.datetime.strptime(datetime.datetime.now().date().strftime('%Y-%m-%d') + ' 14:57:00','%Y-%m-%d %H:%M:%S')
    algo_params.order_side = OrderSide.BUY
    algo_params.remark = '测试TWAP'
    
    ord_info = AlgoOrderInfo()
    ord_info.symbol='600000.SH'
    ord_info.amount = 100000
    ord_info.limit_price = 11
    algo_params.order_list.append(ord_info)
    
    ord_info1 = AlgoOrderInfo()
    ord_info1.symbol='000002.SZ'
    ord_info1.amount = 100000
    ord_info1.limit_price = 0
    algo_params.order_list.append(ord_info1)

    
    rsp = AlgoTradeHandler.start_split_order_algo_instance(AccountType.normal, algo_params)
    print(rsp.__dict__)
    
    
def handle_order_report(context, ord, msg_type):
    print('recv order:', ord.__dict__)
    