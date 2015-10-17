__author__ = 'lamter'


from flowing import Flowing

def read(fileObj, securityTrader=None, _flowType=None):
    """
    读取 excel 文件，并返回
    :param fileObj: 已经打开的 file 文件实例，限制 file 实例是为了可以不依赖磁盘文件，直接使用内存
    :param securityTrader: 对应的券商
    :param _flowType:
    :return:
    """

    flowing = Flowing.open(fileObj, securityTrader)

    return flowing




