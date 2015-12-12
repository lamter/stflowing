__author__ = 'lamter'

from error import *

from orm import Model, StringField, IntegerField

''' 表头最小列数 '''
HEADS_MIN_SIZE = 2



class Shares(Model):
    """
    股票交易流水表
    """
    __table__ = 'shares'

    id = IntegerField(primary_key=True)
    # name = StringField()




    # def __init__(self, heads):
    #     """
    #     一个通用的流水实例应该有的属性
    #     "流水号", "发生日期", "业务名称", "发生金额", "剩余金额", "币种", "股东代码", "证券代码", "证券名称",
    #     "买卖标志", "成交价格", "成交数量", "备注", "佣金", "印花税", "过户费", "其他费"
    #     :return:
    #     """
    #     self.heads = heads    # OrderedDict
    #
    #     self.id = ''                                # 流水号
    #     self.date = None                            # 发生日期 datetime.date
    #     self.business = ''                          # 业务名称
    #     self.amount = 0.                            # 发生金额
    #     self.rest = 0.                              # 剩余金额
    #     self.currency = ''                          # 币种
    #     self.shareholdersCode = ''                  # 股东代码
    #     self.securityCode = ''                      # 证券代码
    #     self.securityName = ''                      # 证券名称
    #     self.tradingSymbol = ''                     # 买卖标志
    #     self.price = ''                             # 成交价格
    #     self.number = ''                            # 成交数量
    #     self.remark = ''                            # 备注
    #     self.commissions = 0.                       # 佣金
    #     self.stampDuty = 0.                         # 印花税
    #     self.transferFee = 0.                       # 过户费
    #     self.otherFee = 0.                          # 其他费


    # def _load(self, datas):
    #     """
    #     :return:
    #     """
    #     for i, proName in enumerate(self.heads.keys()):
    #         setattr(self, proName, datas[i])
    #
