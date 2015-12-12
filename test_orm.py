__author__ = 'lamter'

import logging
logging.basicConfig(level=logging.NOTSET)
import unittest
import asyncio
import time

import orm
import shares

def suite():
    testSuit = unittest.makeSuite(TestORM)
    alltestCase = unittest.TestSuite([testSuit, ])
    return alltestCase


class TestORM(unittest.TestCase):
    '''
    测试 http server
    '''
    def setUp(self):
        # 获取EventLoop:
        self.loop = asyncio.get_event_loop()
        # 执行coroutine

        orm.create_pool(
            self.loop,
            user='root',
            password='qqqqqq',
            db='stflowing',
        )

    def tearDown(self):
        # self.loop.close()
        return

    def test_shares(self):
        """

        :return:
        """

        share = shares.Shares(
            id=1,
        )
        logging.info('share id %s' % share.id)
        yield from share.save()

        logging.info('save over ..')
