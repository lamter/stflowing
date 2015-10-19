
__author__ = 'lamter'

import re
import json
import datetime
from collections import Counter

import xlrd
import openpyxl

from error import *
import iterm

# 表中至少要有几行数据
ITEM_NUM_MIN_SIZE = 1


''' 证券公司 '''
HUATAI = '华泰证券_交割流水'





class Flowing():
    """
    将一个 excel 文件解析并返回
    """
    with open('traders.json', 'r') as traders:
        TRADERS = json.load(traders)

    @classmethod
    def open(cls, fileObj, flowingType=None):
        """

        :param fileObj:
        :param flowingType:
        :return:
        """

        # TODO 尝试解析出原始数据
        originArray = cls.getOriginArray(fileObj)


        # TODO 解析表头

        # TODO 将数据逐条实例化为 Item() 导入到 Flowing() 实例中


    @classmethod
    def getOriginArray(cls, fileObj):
        """
        尝试解析出原始数据
        :param fileObj:
        :return:
        """
        try:
            if fileObj.name.endswith('.xls'):
                # 解析 *.xls 文件
                originArray = cls.open_xls(fileObj)
            elif fileObj.name.endswith('.xlsx'):
                # 解析 .xlsx 文件
                originArray = cls.open_xlsx(fileObj)
        except TypeError:
            # TODO ''' 非常规 excel 文件 '''
            originArray = cls.open_text(fileObj)

        # TODO 初步检查数据是否正常
        cls.checkOriginArray(originArray)

        return originArray



    @classmethod
    def open_xls(cls, fileObj):

        # TODO open_xls
        file_contents = fileObj.read()
        fileObj.seek(0, 0)  # 将指针移动到开头
        book = xlrd.open_workbook(file_contents=file_contents)


    @classmethod
    def open_xlsx(cls, fileObj):
        """
        解析  .xlsx 文件
        :param fileObj:
        :return:
        """
        # TODO  open_xlsx
        fileObj.seek(0, 0)  # 将指针移动到开头
        book = openpyxl.load_workbook(filename=fileObj)


    @classmethod
    def open_text(cls, fileObj):
        """
        使用  table 键构建的文本文件
        :param fileObj:
        :return:
        """

        # 解析表头, 根据表头判断解析类型
        # fileObj.seek(0, 0)  # 将指针移动到开头
        # titleStr = fileObj.readline().replace('\n', '')

        # 一系列用来分析表头的函数
        analyTitleFuncs = [
            cls._byTableKey,    # 尝试以 table key 来解析
        ]

        for func in analyTitleFuncs:
            # 逐个解析表头的函数，以此来确定券商的类型，可能会有多个解析函数符合，即可能多个券商符合
            try:
                # 直接返回 originArray
                return func(fileObj)
            except AnalyOriginArrayAsTextFaild:
                pass

        raise AnalyOriginArrayFaild('非常规文本解析失败!')

        # if not flowingTypes:
        #     raise UnknowTrader('title: titleStr')
        #
        # # 根据可能符合的券商，生成 Flowing() 实例返回
        # if flowingType is None:
        #     # TODO ''' 没有指定了流水类型 '''
        #     flowing = cls._getInstanceByFlowingType(flowingType, flowingTypes)
        # else:
        #     # TODO ''' 指定了流水类型 '''
        #     flowing = cls._getInstanceNotByFlowingType(flowingTypes)
        #
        # # 读取数据部分
        # flowing.readData(fileObj)



    # @classmethod
    # def _getInstanceByFlowingType(cls, flowingType, flowingTypes):
    #     """
    #     指定了流水类型的情况
    #     :param flowingType:
    #     :return:
    #     """
    #     if flowingType not in flowingTypes:
    #         raise UnknowTrader(flowingType)
    #
    #     return cls()


    # def _getInstanceNotByFlowingType(self, flowingTypes):
    #     """
    #     没指定流水类型时
    #     :return:
    #     """
    #
    #
    # @classmethod
    # def choseClassByTitles(cls, titles):
    #     """
    #     根据表头来找出券商
    #     :param titleStr:
    #     :return:
    #     """
    #     return [trader for trader, info in cls.TRADERS.iteritems() if titles == info.表头]


    @classmethod
    def _byTableKey(cls, fileObj):
        """
        分析是否为该格式 :
        ="成交日期"	="证券代码"	="证券名称"	="买卖标志"	="成交价格"	="成交数量"	="成交编号"	="委托编号"	="股东代码"
        如果格式为 ="123456"，说明其数据位为文本，如果单纯数字，则数据类型为数值
        :return:
        """
        # 将游标移动到初始位置
        fileObj.seek(0, 0)

        originArray = []
        try:
            for _ in range(10):
                dataStr = fileObj.readline()
                datas = dataStr.split('\t')
                originArray.append([cls._clearEqualQuto(t) for t in datas if t])
        except IOError:
            pass




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



    def checkOriginArray(self, originArray):
        """
        检查原始数据是否正常
        :param originArray:
        :return:
        """

        # 至少要有一行表头
        size = len(originArray)
        if size < ITEM_NUM_MIN_SIZE:
            raise AnalyOriginArrayFaild('表中没有数据')

        # 每行数据的长度要一致
        num = originArray[0]
        for i, data in enumerate(originArray[1:]):
            if len(data) != num:
                raise ValueError('第%s行数据长度不一致:%s' % (i, data))






