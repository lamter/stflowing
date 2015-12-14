__author__ = 'lamter'

import logging
logging.basicConfig(level=logging.INFO)
# import unittest
import asyncio
import time

import orm
import shares

# 获取EventLoop: EventLoop 并发池
loop = asyncio.get_event_loop()

def createPool():
    # 执行coroutine
    yield from orm.create_pool(
        loop,
        user='root',
        password='qqqqqq',
        db='stflowing',
    )

def test():
    yield from orm.create_pool(loop,
                               user='root',
                               password='qqqqqq',
                               db='stflowing',
                               )

    share = shares.Shares(id=2, name='新能车A')

    yield from share.save()

def read():
    yield from orm.create_pool(loop,
                               user='root',
                               password='qqqqqq',
                               db='stflowing',
                               )
    share = yield from shares.Shares.find(1)
    logging.info(share.name)


def findNum():
    yield from orm.create_pool(loop,
                               user='root',
                               password='qqqqqq',
                               db='stflowing',
                               )
    # num = yield from shares.Shares.findNumber(shares.Shares.id)
    num = yield from shares.Shares.findNumber('id', where='id>? AND name="%车%"', args=(0,))
    logging.info('findNumber %s' % num)

# loop.run_until_complete(test())
# loop.run_until_complete(read())
loop.run_until_complete(findNum())
loop.close()


# class TestORM(unittest.TestCase):
#     '''
#     测试 http server
#     '''
#     def setUp(self):
#         logging.debug('setUp ...')
#
#
#     def tearDown(self):
#         # self.loop.close()
#         logging.info('tear down ...')
#         return
#
#
#     def test_shares(self):
#         """
#
#         :return:
#         """
#         logging.info('run the test shares ...')
#
#         share = shares.Shares(
#             id=1,
#         )
#         logging.info('share id %s' % share.id)
#         yield from share.save()
#
#         logging.info('save over ..')
#
#
#
#
