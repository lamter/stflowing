__author__ = 'lamter'

class FlowingException(Exception):
    """
    解析流水时错误的基类
    """



class UnknowTrader(FlowingException):
    """
    无法识别的券商
    """



class AnalyTitleFaild(FlowingException):
    """
    解析表头失败
    """