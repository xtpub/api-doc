#coding=utf-8
"""
author:kidd
"""

# python 3.6

from python.restful import UbiexSDK

def main():
    sdk = UbiexSDK("accessKey", "secretKey")
    print("balance: ", sdk.getBalance())
    print("market config: ", sdk.getMarketConfig())
    print("funds: ", sdk.getFunds())
    print("getDepth: ", sdk.getDepth("btc_usdt"))

if __name__ == '__main__':
    main()
