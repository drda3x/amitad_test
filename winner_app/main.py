#!/usr/bin/env python3

import dateutil
from dateutil import parser
from functools import partial
from flask import Flask, request
import json


app = Flask(__name__)


def check_str(sub_str, in_str):
    return sub_str in in_str


def check_record(record1, record2):
    return record1['client_id'] == record2['client_id'] and \
                record1['User-Agent'] == record2["User-Agent"] and \
                record1['document.location'] == record2['document.referer']


def find_winners(data, seach_link, win_link):
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
    log = json.loads(request.args.get('log'))
    return json.dumps(find_winners(log, 'referal.ours.com', 'https://shop.com/checkout'))


if __name__ == "__main__":
    app.run()
