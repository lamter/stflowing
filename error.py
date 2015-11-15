__author__ = 'lamter'

class FlowingException(Exception):
    """
    解析流水时错误的基类
    """

class UnknowTrader(FlowingException):
    """
    无法识别的券商
    """

class IdentifyTitleFaild(FlowingException):
    """
    识别表头失败
    """


class AnalyOriginArrayAsTextFaild(FlowingException):
    """
    解析初始数据失败
    """

class AnalyOriginArrayFaild(FlowingException):
    """
    解析初始数据失败
    """


class InitItemFaild(FlowingException):
    """
    生成 item 失败
    """