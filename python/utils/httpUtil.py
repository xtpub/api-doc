# coding=utf-8
"""
author:kidd
"""

import requests
import hmac
import hashlib



class HttpUtil:
    KWARGS = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
            "content-type": "application/json; charset=utf8",
        },
        "timeout": 5,
    }

    def __init__(self) -> None:
        return

    def get(self, url, data=None):
        resp = requests.get(url, data, **self.KWARGS)
        return resp.json()

    def post(self, url, data=None):
        resp = requests.post(url, data, **self.KWARGS)
        return resp.json()
