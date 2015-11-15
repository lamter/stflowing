__author__ = 'lamter'

import logging
import json
import datetime
from collections import OrderedDict

import xlrd
import openpyxl

from error import *
from item import Item

# 表中至少要有几行数据
ITEM_NUM_MIN_SIZE = 1


''' 证券公司 '''
HUATAI = '华泰证券_交割流水'





class Flowing():
    """
    将一个 excel 文件解析并返回
    """
    with open('heads.json', 'r') as traders:
        # TRADERS = json.load(traders)
        HEADS_MAP = json.load(traders)

    @classmethod
    def open(cls, fileObj, flowingType=None):
        """

        :param fileObj:
        :param flowingType:
        :return:
        """

        # 尝试解析出原始数据
        originArray = cls.getOriginArray(fileObj)

        # TODO 解析表头
        return cls(flowingType, originArray)



    @classmethod
    def getOriginArray(cls, fileObj):
        """
        尝试解析出原始数据
        :param fileObj:
        :return:
        """

        originArray = []
        try:
            if fileObj.name.endswith('.xls'):
                # 解析 *.xls 文件
                originArray = cls.open_xls(fileObj)
            elif fileObj.name.endswith('.xlsx'):
                # 解析 .xlsx 文件
                originArray = cls.open_xlsx(fileObj)
        except TypeError:
            # ''' 非常规 excel 文件 '''
            originArray = cls.open_text(fileObj)

        # 初步检查数据是否正常
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

        # 一系列用来分析 数据格式 的函数
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
            while 1:
                # 读一行
                dataStr = fileObj.readline()
                # 空字符，结束
                if dataStr == '':break

                # 去掉末尾的 \n
                dataStr = dataStr.strip()
                # 按照 table 符来切割单元格  'unit1\tunit2
                datas = dataStr.split('\t')
                originArray.append([cls._clearEqualQuto(t) for t in datas])
        except IOError:
            logging.info('%s done ...' % fileObj.name)
            pass

        return originArray


    @classmethod
    def _clearEqualQuto(cls, s):
        """
        清洗 ="成交日期" 这种格式
        :param s:
        :return:
        """
        if s == '':
            return None

        if '=' in s:
            ''' 有字符 '''
            return s.replace('=', '').replace('"', '').replace("'", '')
        else:
            return float(s)


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


    @classmethod
    def checkOriginArray(cls, originArray):
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
        num = len(originArray[0])
        for i, data in enumerate(originArray[1:]):
            if len(data) != num:
                raise ValueError('第%s行数据长度: %s 与表头长度: %s 不一致:%s' % (i, len(data), num, data))


    def __init__(self, flowingType, originArray):
        """
        :param flowingType: 指定的流水的名字
        :param originArray:
        :return:
        """
        self.type = flowingType
        self.originArray = originArray
        self._heads = OrderedDict()          # 表头 {"price": "价格"}

        # TODO 将数据逐条实例化为 Item() 导入到 Flowing() 实例中
        self._identyfy()


    def getOriginHeads(self):
        """
        获取原始数据中的表头
        :return:
        """
        return self.originArray[0]


    def getOriginData(self):
        """

        :return:
        """
        return self.originArray[1:]


    def _identyfy(self):
        """
        识别原始数据
        :return:
        """
        for head in self.getOriginHeads():
            proName = self.getProNameByHead(head)
            if proName is None:
                raise IdentifyTitleFaild('表头:%s找不到对应的属性' % head)
            self._heads[proName] = head

        # 生成数据列
        for datas in self.getOriginData():
            item = Item.read(self._heads, datas)


    @classmethod
    def getProNameByHead(cls, head):
        """

        :param head:
        :return:
        """
        for proName, heads in cls.HEADS_MAP.items():
            if head in heads:
                return proName


