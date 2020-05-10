#!/usr/bin/env python3

import sys
import unittest
import random
import time
from winner_app.main import find_winners
from copy import deepcopy


class TestWinnerService(unittest.TestCase):

    def setUp(self):
        self.data = [
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
                "date": "2018-05-23T18:59:13.286000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-05-23T18:59:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=25",
                "document.referer": "https://shop.com/products/id?=10",
                "date": "2018-05-23T19:04:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/cart",
                "document.referer": "https://shop.com/products/id?=25",
                "date": "2018-05-23T19:05:13.123000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/cart",
                "date": "2018-05-23T19:05:59.224000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
                "date": "2018-05-23T18:59:13.286000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-05-23T18:59:20.119000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=25",
                "document.referer": "https://shop.com/products/id?=10",
                "date": "2018-05-23T19:04:20.119000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/cart",
                "document.referer": "https://shop.com/products/id?=25",
                "date": "2018-05-23T19:05:13.123000Z"
            },
            {
                "client_id": "user8",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/cart",
                "date": "2018-05-23T19:05:59.224000Z"
            }
        ]

    def test_basic(self):
        # Базовый тест. У нас два пользователя параллельно использующие сайт
        ref_data = [
            ("user8", "Chrome 65", "https://shop.com/checkout", "https://referal.ours.com/?ref=0xc0ffee"),
            ("user7", "Chrome 65", "https://shop.com/checkout", "https://referal.ours.com/?ref=0xc0ffee"),
        ]

        winners = [(winner['client_id'],
                    winner['User-Agent'],
                    winner['document.location'],
                    winner['document.referer'])
                   for winner in find_winners(self.data, 'referal.ours.com', 'https://shop.com/checkout')]

        assert len(winners) == 2
        assert all((w in ref_data for w in winners))

    def test_order(self):
        # Смотрим что будет если перемешать лог
        random.shuffle(self.data)
        self.test_basic()

    def test_surround(self):
        # в базовом варианте два пользователя параллельно проходят по ссылкам
        # посмотрим что будет если один из них прошел по ссылке, забыл
        # об этом, снова прошел по ссылке, купил, а потом вспомнил что уже
        # открывал сайт. Он нашел ранее открытую вкладку, и купил товар
        self.data += [
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
                "date": "2018-01-23T18:59:13.286000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-03-23T18:59:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=25",
                "document.referer": "https://shop.com/products/id?=10",
                "date": "2018-08-23T19:04:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/cart",
                "document.referer": "https://shop.com/products/id?=25",
                "date": "2018-09-23T19:05:13.123000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/cart",
                "date": "2018-11-23T19:05:59.224000Z"
            }
        ]

        winners = [(winner['client_id'],
                    winner['User-Agent'],
                    winner['document.location'],
                    winner['document.referer'])
                   for winner in find_winners(self.data, 'referal.ours.com', 'https://shop.com/checkout')]

        assert len(winners) == 3

    def test_not_buy(self):
        # Прверяем, что не купившие не попали в итоговый список
        self.data += [
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://referal.ours.com/?ref=0xc0ffee",
                "date": "2018-01-23T18:59:13.286000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-03-23T18:59:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=25",
                "document.referer": "https://shop.com/products/id?=10",
                "date": "2018-08-23T19:04:20.119000Z"
            },
            {
                "client_id": "user7",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/cart",
                "document.referer": "https://shop.com/products/id?=25",
                "date": "2018-09-23T19:05:13.123000Z"
            }
        ]

        winners = [(winner['client_id'],
                    winner['User-Agent'],
                    winner['document.location'],
                    winner['document.referer'])
                   for winner in find_winners(self.data, 'referal.ours.com', 'https://shop.com/checkout')]

        assert len(winners) == 2

    def test_filter_others(self):
        # Проверяем, что купившие не через нашу ссылку не попали в список
        self.data += [
            {
                "client_id": "user69",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/",
                "document.referer": "https://referal.not_ours.com/?ref=0xc0ffee",
                "date": "2018-01-23T18:59:13.286000Z"
            },
            {
                "client_id": "user69",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=10",
                "document.referer": "https://shop.com/",
                "date": "2018-03-23T18:59:20.119000Z"
            },
            {
                "client_id": "user69",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/products/id?=25",
                "document.referer": "https://shop.com/products/id?=10",
                "date": "2018-08-23T19:04:20.119000Z"
            },
            {
                "client_id": "user69",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/cart",
                "document.referer": "https://shop.com/products/id?=25",
                "date": "2018-09-23T19:05:13.123000Z"
            },
            {
                "client_id": "user69",
                "User-Agent": "Chrome 65",
                "document.location": "https://shop.com/checkout",
                "document.referer": "https://shop.com/cart",
                "date": "2018-11-23T19:05:59.224000Z"
            }

        ]

        winners = [(winner['client_id'],
                    winner['User-Agent'],
                    winner['document.location'],
                    winner['document.referer'])
                   for winner in find_winners(self.data, 'referal.ours.com', 'https://shop.com/checkout')]

        not_our_winners = [(winner['client_id'],
                    winner['User-Agent'],
                    winner['document.location'],
                    winner['document.referer'])
                   for winner in find_winners(self.data, 'referal.not_ours.com', 'https://shop.com/checkout')]

        assert len(winners) == 2
        assert len(not_our_winners) == 1

    def test_alot_of_users(self):
        # Посмотрим насколько быстро обработается 1к пользователей
        users = []
        for i in range(1000):
            _users = deepcopy(self.data[:6])
            user_id = "user{}".format(i)
            for user in _users:
                user["client_id"] = user_id

            users += _users

        t = time.time()

        winners = [(winner['client_id'],
                    winner['User-Agent'],
                    winner['document.location'],
                    winner['document.referer'])
                   for winner in find_winners(users, 'referal.ours.com', 'https://shop.com/checkout')]

        assert time.time() - t < 3
        assert len(winners) == 1000

if __name__ == "__main__":
    unittest.main()
