#!/usr/bin/env python3

import dateutil
from dateutil import parser
from functools import partial
from flask import Flask, request
import json

app = Flask(__name__)

def load_data():
    data = [
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

    for record in data:
        record['date'] = parser.isoparse(record['date'])

    return data


def check_str(sub_str, in_str):
    return sub_str in in_str


def check_record(record1, record2):
    return record1['client_id'] == record2['client_id'] and \
                record1['User-Agent'] == record2["User-Agent"] and \
                record1['document.location'] == record2['document.referer']


@app.route("/")
def main():
    log = json.loads(request.args.get('log'))
    is_winner = partial(check_str, 'shop.com/checkout')
    is_ours = partial(check_str, 'referal.ours.com')
    winners = []

    for record in sorted(log, key=lambda x: x['date'], reverse=True):
        if is_winner(record['document.location']):
            winners.append(record)
            continue

        for winner_record in winners:
            if check_record(record, winner_record):
                winner_record['document.referer'] = record['document.referer']

    result = [winner for winner in winners if is_ours(winner['document.referer'])]

    return json.dumps(result)


if __name__ == "__main__":
    app.run()
