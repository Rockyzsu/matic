# encoding: utf-8
"""
@project = HtStragetyRunEnv
@file = mq_strategy_apitest
@author = 011048
@create_time = 2018/5/23 16:28
"""
from mquant_api import *
from mquant_struct import *

def TestSqlite():
    conn = get_sqlite_connection()
    conn.excutesql('''CREATE TABLE `ma_5` (
                       `index` BIGINT(20) NULL DEFAULT NULL,
                       `code` VARCHAR(16) NULL DEFAULT NULL,
                       `date` VARCHAR(50) NULL DEFAULT NULL,
                       `ma` DOUBLE NULL DEFAULT NULL
                       )''')
    conn.excutesql('insert into ma_5 values(0,?1,?2,19.50)', ['601688', '2018-01-29'])
    conn.excutesql('insert into ma_5 values(1,\'000002\',\'2018-01-28\',23.50)')

    conn.transaction()
    conn.excutesql('insert into ma_5 values(2,?1,?2,19.50)', ['000001', '2018-01-29'])
    conn.excutesql('insert into ma_5 values(3,?1,?2,19.50)', ['000100', '2018-01-29'])
    conn.excutesql('insert into ma_5 values(4,?1,?2,19.50)', ['601600', '2018-01-29'])
    conn.rollback()

    conn.transaction()
    conn.excutesql('insert into ma_5 values(5,?1,?2,19.50)', ['000001', '2018-01-29'])
    conn.excutesql('insert into ma_5 values(6,?1,?2,19.50)', ['000100', '2018-01-29'])
    conn.excutesql('insert into ma_5 values(7,?1,?2,19.50)', ['601600', '2018-01-29'])
    conn.commit()

    conn.excutesql('select * from ma_5')
    print(conn.fetchall())

def TestReadCsv():
    csv_reader = open_csv_file('./configFile/testCsv.csv')
    count = 0
    for row in csv_reader:
        print(row)
        count = count + 1
        
        if count > 10:
            break



    csv_reader.reset()
    print('第5行：', csv_reader.getRow(5))
    csv_reader.close()

def timer_func(context, interval, msg_type):
    """
    示例定时函数
    :param conetxt:
    :return:
    :remark:用户函数
    """
#    print('enter timer func,inerval:%d' % interval)
#    print('111')
#    log.debug('recv timer signal:%d' % interval)

    if interval == 3:
        log.debug('开始查询资金账号下所有成交数据')
        trade_deals = get_trades(only_this_inst=False)
        log.debug('查询获取到%d条成交数据' % len(trade_deals))
        log.debug('开始查询所有订单数据')
        order_list = get_orders(only_this_inst=False)
        log.debug('查询所有订单返回%d条数据' % len(order_list))
        print('账户可用资金', context.portfolio.available_cash)
        if not context.portfolio.positions['601688.SH'] is None:
            log.debug('华泰证券持仓 : %d' % context.portfolio.positions['601688.SH'].total_amount)
#        
        cancel_order_list = []
        log.debug('开始查询资金账号下所有未成订单')
        open_orders = get_open_orders(only_this_inst=False)
        log.debug('查询获得当前资金账号下所有未完成订单,%s' % len(open_orders))
        
        # log.debug('开始下单：%s' % '601688.SH')
        # order('601688.SH', 3000, LimitOrderStyle(18.0))
        # log.debug('结束下单：%s' % '601688.SZ')
        # log.debug('开始下单：%s' % '000002.SZ')
        # order('000002.SZ', 3000, MarketOrderStyle('a'))
        # log.debug('结束下单：%s' % '000002.SZ')

def strategy_params():
    """
    策略可自定义运行参数，启动策略时会写入到context对象的run_params字段内
    :return:dict对象，key为参数名，value为一个包含参数默认值、参数描述（选填）的字典
    :remark:可选实现
    """
    # 示例如下：
    dict_params = {
        '证券代码': {'value': '000001.SZ/000002.SZ', 'desc': '交易标的'},  # 'desc'字段可填写，也可不填写
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
    run_timely(timer_func, 3)  # 注册一个3s的定时函数，用于下单
#    run_timely(timer_func, 10)  # 注册一个3s的定时函数，用于下单
#    run_timely(timer_func, 20, '13:20')  # 注册20s的定时函数，用于查询成交
#    run_timely(timer_func, 30, '13:20')  # 注册30s的定时函数，查询所有订单
    #    log.debug('enter initialize')
#    print('证券代码',context.run_params['证券代码'])
    subscribe(context.run_params['证券代码'].strip('/').split('/'))
    subscribe(context.run_params['证券代码'].strip('/').split('/'),'record_order')
    subscribe(context.run_params['证券代码'].strip('/').split('/'),'record_transaction')
    g.security_list=context.run_params['证券代码'].strip('/').split('/')
    lst_buy_price = context.run_params['买入价格'].strip('/').split('/')
    lst_sell_price = context.run_params['卖出价格'].strip('/').split('/')
    g.buy_dict = dict(zip(g.security_list,lst_buy_price))
    g.sell_dict = dict(zip(g.security_list,lst_sell_price))
#    
    print('开始读取配置文件：./configFile/usrCfg.ini')
    configValue = read_ini_config('./configFile/usrCfg.ini', 'TEST', 'key1')
    print('读取配置文件完成：key:%s,value:%s' % ('key1', configValue))
#
    print('开始读取csv配置文件')
    TestReadCsv()
    print('结束读取csv配置文件')

    print('开始测试sqlite数据库')
    TestSqlite()
    print('结束测试sqlite数据库')
    
    print('fund account',context.get_fund_account_by_type('stock'))
    
    print('开始查询A股账户的全部持仓')
    positions = get_positions()
    if positions:
        print('查询A股账户全部持仓返回', positions.keys())

    print('开始查询信用账户的全部持仓')
    positions = get_positions(AccountType.margin)
    if positions:
        print('查询信用账户全部持仓返回', positions.keys())



def handle_tick(context, tick, msg_type):
    """
    实时行情接收函数
    :param context:
    :param tick: Tick对象
    :return:
    :remark:可选实现
    """
    print('recv tick msg', tick.code, tick.datetime, datetime.datetime.now())
            
            
def handle_order_report(context, ord, msg_type):
    """
    订单回报处理函数，非必填
    :param ord:Order对象
    :return:
    """
    print('recv order report', ord.symbol, ord.status, ord.order_id)


def on_strategy_end(context):
    """
    策略结束时调用，用户可以在此函数中进行一些汇总分析、环境清理等工作
    :param context:Context对象
    :return:
    :remark:可选实现
    """
    print('on_strategy_end')
    
def handle_order_record(context, order_record, msg_type):
    """
    处理逐笔委托，深市代码有逐笔委托，沪市没有
    :param context: Context对象
    :param order_record: 逐笔委托数据，RecordOrder对象
    :param msg_type:
    :return:
    """
    print('recv order record',order_record.code)

    
def handle_record_transaction(context, record_transaction, msg_type):
    """
    处理逐笔成交
    :param context: Context对象
    :param record_transaction: 逐笔成交数据，RecordTransaction对象
    :param msg_type: 保留
    :return:
    """
    print('recv record transaction',record_transaction.code)