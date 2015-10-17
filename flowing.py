
__author__ = 'lamter'

import re
import json
import datetime

import xlrd
import openpyxl

from error import *
import iterm


''' 证券公司 '''
HUATAI = u'华泰证券_交割流水'




class Flowing():
    """
    将一个 excel 文件解析并返回
    """
    with open('traders.json', 'r') as traders:
        TRADERS = json.load(traders)

    @classmethod
    def open(cls, fileObj, flowingType=None):
        try:
            ''' 读物流水文件 '''
            if fileObj.name.endswith('.xls'):
                return cls.open_xls(fileObj)
            elif fileObj.name.endswith('.xlsx'):
                return cls.open_xlsx(fileObj)
        except TypeError:
            # TODO ''' 非常规 excel 文件 '''
            return cls.open_text(fileObj, flowingType)

        raise UnknowTrader(fileObj.name)



    @classmethod
    def open_xls(cls, fileObj):

        # TODO open_xls
        file_contents = fileObj.read()
        book = xlrd.open_workbook(file_contents=file_contents)


    @classmethod
    def open_xlsx(cls, fileObj):
        """
        解析  .xlsx 文件
        :param fileObj:
        :return:
        """
        # TODO  open_xlsx
        book = openpyxl.load_workbook(filename=fileObj)


    @classmethod
    def open_text(cls, fileObj, flowingType):
        """
        使用  table 键构建的文本文件
        :param fileObj:
        :return:
        """

        # 解析表头, 根据表头判断解析类型
        fileObj.seek(0, 0)  # 将指针移动到开头
        titleStr = fileObj.readline().replace('\n', '')

        # 一系列用来分析表头的函数
        analyTitleFuncs = [
            cls._byTableKey,    #
        ]

        flowingTypes = []
        for func in analyTitleFuncs:
            # 逐个解析表头的函数，以此来确定券商的类型，可能会有多个解析函数符合，即可能多个券商符合
            try:
                flowingTypes = func(titleStr)
            except AnalyTitleFaild:
                pass

        if not flowingTypes:
            raise UnknowTrader('title: titleStr')

        # 根据可能符合的券商，生成 Flowing() 实例返回
        if flowingType is None:
            # TODO ''' 没有指定了流水类型 '''
            flowing = cls._getInstanceByFlowingType(flowingType, flowingTypes)
        else:
            # TODO ''' 指定了流水类型 '''
            flowing = cls._getInstanceNotByFlowingType(flowingTypes)

        # 读取数据部分
        flowing.readData(fileObj)



    @classmethod
    def _getInstanceByFlowingType(cls, flowingType, flowingTypes):
        """
        指定了流水类型的情况
        :param flowingType:
        :return:
        """
        if flowingType not in flowingTypes:
            raise UnknowTrader(flowingType)

        return cls()


    def _getInstanceNotByFlowingType(self, flowingTypes):
        """
        没指定流水类型时
        :return:
        """


    @classmethod
    def choseClassByTitles(cls, titles):
        """
        根据表头来找出券商
        :param titleStr:
        :return:
        """
        return [trader for trader, info in cls.TRADERS.iteritems() if titles == info.表头]


    @classmethod
    def _byTableKey(cls, titleStr):
        """
        分析是否为该格式 :
        ="成交日期"	="证券代码"	="证券名称"	="买卖标志"	="成交价格"	="成交数量"	="成交编号"	="委托编号"	="股东代码"
        :return:
        """
        ''' table="表头" 的解析方式 '''
        titles = titleStr.split('\t')
        if len(titles) < iterm.HEADS_MIN_SIZE:
            raise AnalyTitleFaild(titleStr)

        ''' 解析出表头数组 '''
        titles = [cls._clearEqualQuto(t) for t in titles if t]

        ''' 据此找到匹配的券商 '''
        return cls.choseClassByTitles(titles)


    @classmethod
    def _clearEqualQuto(cls, s):
        """
        清洗 ="成交日期" 这种格式
        :param s:
        :return:
        """
        return s.replace('=', '').replace('"', '').replace("'", '')


    def readData(self, fileObj):
        """
        读取数据部分
        :param fileObj:
        :return:
        """

        try:
            while 1:
                self.saveToItem(fileObj.readline())
        except IOError:
            pass
        except:


    def saveToItem(self, record):
        """

        :param record:
        :return:
        """