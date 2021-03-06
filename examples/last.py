#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymisp import PyMISP
from keys import url_priv, key_priv
# from keys import url_cert, key_cert
import argparse
import os
import json


# Usage for pipe masters: ./last.py -l 5h | jq .


def init(url, key):
    return PyMISP(url, key, True, 'json')


def download_last(m, last, out=None):
    result = m.download_last(last)
    if out is None:
        for e in result['response']:
            print(json.dumps(e) + '\n')
    else:
        with open(out, 'w') as f:
            for e in result['response']:
                f.write(json.dumps(e) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download latest events from a MISP instance.')
    parser.add_argument("-l", "--last", required=True, help="can be defined in days, hours, minutes (for example 5d or 12h or 30m).")
    parser.add_argument("-o", "--output", help="Output file")

    args = parser.parse_args()

    if args.output is not None and os.path.exists(args.output):
        print('Output file already exists, abord.')
        exit(0)

    misp = init(url_priv, key_priv)
    # misp = init(url_cert, key_cert)

    download_last(misp, args.last, args.output)
