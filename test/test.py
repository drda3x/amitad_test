#!/usr/bin/env python3

import unittest

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
        },
        {
            "client_id": "user8",
            "User-Agent": "Chrome 65",
            "document.location": "https://shop.com/checkout",
            "document.referer": "https://shop.com/cart",
            "date": "2018-05-23T19:05:59.224000Z"
        }
    ]

    def test_all(self):

