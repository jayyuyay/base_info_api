#! /usr/bin/python
# -*- coding:utf-8-*-

import pymongo
import sys
import codecs
reload(sys)
sys.setdefaultencoding('utf8')

cfg = {
    'host': '127.0.0.1',
    'port': 27017,
    'db': 'info',
    'code_c': 'code_info',
    'android_c': 'android_info',
}


def file_to_mongo():
    with open('country.csv', 'r') as f:
        for line in f:
            L = line.split(',')
            o = {
                'code': L[0],
                'en': L[1],
                'cn': L[2].strip()
            }
            code_c.save(o)
    with open('android_v.csv', 'r') as f:
        for line in f:
            L = line.split(',')
            o = {
                'api': L[0],
                'version': L[1],
                'name': L[2].strip()
            }
            android_c.save(o)


if __name__ == "__main__":
    conn = pymongo.Connection(
        host=cfg['host'],
        port=cfg['port']
    )
    db = conn[cfg['db']]
    code_c = db[cfg['code_c']]
    android_c = db[cfg['android_c']]
    file_to_mongo()
