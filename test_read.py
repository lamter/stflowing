
__author__ = 'lamter'

import unittest

import opertaion


def suite():
    testSuit = unittest.makeSuite(TestRead, "test")
    alltestCase = unittest.TestSuite([testSuit, ])
    return alltestCase


class TestRead(unittest.TestCase):
    '''
    测试 http server
    '''
    def setUp(self):
        pass


    def test_read(self):
        """

        :return:
        """
        with open('20150615_20150813_ht_currency.xls', 'r', encoding='gbk') as f:
            flowing = opertaion.read(f)
            print(flowing)


    def test_open(self):
        import xlrd
        book = xlrd.open_workbook(filename='.xls')


    def test_file(self):
        with open('item.py', 'r') as f:
            while 1:print(17171, f.readline())

            # f.seek(0, 2)
            # print(181818, f.read())
            # print(f.fileno())



    def test_re(self):
        import re
        source = "s2f程序员杂志一2d3程序员杂志二2d3程序员杂志三2d3程序员杂志四2d3"

        xx=u"([/u4e00-/u9fa5]+)"
        pattern = re.compile(xx)
        results =  pattern.findall(source)

        for result in results :
            print(result)


    def test_json(self):
        """

        :return:
        """
        import json
        with open('traders.json', 'r') as f:
            print(json.load(f))


    def test_table_key(self):
        a = '		'

        print(a.split('\t'))