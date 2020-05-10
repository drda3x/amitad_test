#!/usr/bin/env python3

import dateutil
from dateutil import parser
from functools import partial
from flask import Flask, request
import argparse
import json


app = Flask(__name__)


def check_str(sub_str, in_str):
    """
    Syntax sugar

    @param sub_str<str>
    @param in_str<str>

    @return <bool>
    """

    return sub_str in in_str


def check_record(record1, record2):
    """
    Function to check if the record2 follows the record1

    @param record1<dict>
    @param record2<dict>

    @return <bool>
    """
    return record1['client_id'] == record2['client_id'] and \
                record1['User-Agent'] == record2["User-Agent"] and \
                record1['document.location'] == record2['document.referer']


def find_winners(data, seach_link, win_link):
    """
    Function to find winner links

    @param data<list(dict)>
    @param search_link<str>
    @param win_link<str>

    @return <list(dict)>
    """

    is_winner = partial(check_str, win_link)
    is_ours = partial(check_str, seach_link)
    winners = []

    for record in sorted(data, key=lambda x: parser.isoparse(x['date']), reverse=True):
        if is_winner(record['document.location']):
            winners.append(record)
            continue

        for winner_record in winners:
            if check_record(record, winner_record):
                winner_record['document.referer'] = record['document.referer']

    return [winner for winner in winners if is_ours(winner['document.referer'])]


@app.route("/")
def main():
    """
    The main function to process requests

    @return <str>
    """

    log = json.loads(request.args.get('log'))
    return json.dumps(find_winners(log, 'referal.ours.com', 'https://shop.com/checkout'))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-H", '--host', default='127.0.0.1', type=str, help="application host")
    arg_parser.add_argument("-P", '--port', default=5000, type=int, help="application port")
    args = arg_parser.parse_args()
    app.run(host=args.host, port=args.port)
