=======
SecuritiesTransactionFlowing
=======
将各个 excel 格式的券商的交易流水文件转为 json 或者 csv 格式

Description
-----------
开发遵循以下规范：
- python 3.4
- 同时支持 .xls 文件和 .xlsx 文件。但是优先支持 .xls 文件。
- 自动识别改交易流水所属的券商，以及流水类型。

How to use
-----------
::

    with open('20150615_20150813_ht_currency.xls', 'r', encoding='gbk') as f:
        flowing = opertaion.read(f)
        print(flowing.originArray)
        print(flowing.getOriginHeads())
        print(flowing.getOriginData())
