# coding=utf-8
"""
author:kidd
"""

from python.utils.httpUtil import HttpUtil
import hashlib
import hmac
import time

def getTimestamp() -> int:
    return int(round(time.time()*1000))

def getSignature(kwargs: dict, secretKey: str) -> str:
    out = []
    for k, v in kwargs.items():
        out.append("{}={}".format(str(k).strip(), str(v).strip()))
    out.sort()
    s = "&".join(out)
    return hmac.new(secretKey.encode(), s.encode(), digestmod=hashlib.sha256).hexdigest().upper()


class UbiexSDK():
    URL = "https://api.ubiex.co"

    def __init__(self, accessKey: str, secretKey: str):
        super().__init__()
        self.accessKey = accessKey
        self.secretKey = secretKey
        return

    '''
    交易市场配置
    '''

    def getMarketConfig(self):
        return HttpUtil().get(self.URL + "/data/api/v1/getMarketConfig")

    '''
    聚合行情（Ticker）
    '''

    def getKLine(self, market: str):
        return HttpUtil().get(self.URL + "/data/api/v1/getTicker?market=" + market)

    '''
    所有市场的最新 All Tickers
    '''

    def getTickers(self):
        return HttpUtil().get(self.URL + "/data/api/v1/getTickers")

    '''
    市场深度数据 Depth
    '''

    def getDepth(self, market: str):
        return HttpUtil().get(self.URL + "/data/api/v1/getDepth?market=" + market)

    '''
    最近市场成交记录
    '''

    def getTrades(self, market: str):
        return HttpUtil().get(self.URL + "/data/api/v1/getTrades?market=" + market)

    '''
    获取交易账户资产
    '''

    def getBalance(self) -> object:
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getBalance", dit)

    '''
    获取账户类型
    '''

    def getAccounts(self):
        return HttpUtil().get(self.URL + "/trade/api/v1/getAccounts")

    '''
    获取指定账户资金
    '''

    def getFunds(self):
        dit = {
            "accesskey": self.accessKey,
            "account": 1,
            "nonce": getTimestamp(),
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getFunds", dit)

    '''
    划账
        map.put("accesskey", accessKey);
		map.put("from", 1);
		map.put("to", 2);
		map.put("amount", 0.1);
		map.put("coin", "btc");
		map.put("safePwd", "123456");
    '''

    def transfer(self, _from, to, amount: float, coin: str, safePwd: str, ):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "from": _from,
            "to": to,
            "amount": amount,
            "coin": coin,
            "safePwd": safePwd,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().post(self.URL + "/trade/api/v1/transfer", dit)

    '''
    委托
        map.put("market", "btc_usdt");
		map.put("price", "10000.12");
		map.put("number", "1.23");
		map.put("type", 1);		// 0.sell 1.buy
		map.put("entrustType", 0);	// 0.Limited price  1.Market price matching
    '''

    def order(self, market: str, price: float, number: float, type, entrustType: float):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "market": market,
            "price": price,
            "number": number,
            "type": type,
            "entrustType": entrustType,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().post(self.URL + "/trade/api/v1/order", dit)

    '''
    批量委托
        map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		map.put("price", "10000.12");
		map.put("number", "1.23");
		map.put("type", 1);		// 0.sell 1.buy
		map.put("entrustType", 0);	// 0.Limited price  1.Market price matching    
    '''

    def batchOrder(self, market: str, jsonData: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "market": market,
            "data": jsonData,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().post(self.URL + "/trade/api/v1/batchOrder", dit)

    '''
    撤单
    '''

    def cancel(self, market: str, id: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "market": market,
            "id": id,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().post(self.URL + "/trade/api/v1/cancel", dit)

    '''
    批量撤单
    '''

    def batchCancel(self, market: str, *ids: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "market": market,
            "data": ids,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().post(self.URL + "/trade/api/v1/batchCancel", dit)

    '''
    获取订单
    '''

    def getOrder(self, market: str, id: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "market": market,
            "id": id,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getOrder", dit)

    '''
    获取未完成的订单
    '''

    def getOpenOrders(self, market: str, page, pageSize):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "market": market,
            "page": page,
            "pageSize": pageSize,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getOpenOrders", dit)

    '''
    批量获取订单
    '''

    def getBatchOrders(self, market: str, *ids: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "market": market,
            "data": ids,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getBatchOrders", dit)

    '''
    获取充值记录
    '''

    def getPayInRecord(self, coin: str, page, pageSize):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "coin": coin,
            "page": page,
            "pageSize": pageSize,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getPayInRecord", dit)

    '''
    获取提现记录
    '''

    def getPayOutRecord(self, coin: str, page, pageSize):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "coin": coin,
            "page": page,
            "pageSize": pageSize,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getPayOutRecord", dit)

    '''
    获取充值地址
    '''

    def getPayInAddress(self, coin: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "coin": coin,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getPayInAddress", dit)

    '''
    获取提现地址
    '''

    def getPayOutAddress(self, coin: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "coin": coin,
        }
        dit["signature"] = getSignature(dit, self.secretKey)
        return HttpUtil().get(self.URL + "/trade/api/v1/getPayOutAddress", dit)

    '''
    提现
    '''

    def withdraw(self, coin: str, safePwd: str, amount: float, address: str):
        dit = {
            "accesskey": self.accessKey,
            "nonce": getTimestamp(),
            "coin": coin,
            "safePwd": safePwd,
            "amount": amount,
            "address": address,
        }
        dit["signature"] = getSignature(dit, self.secretKey)

        return HttpUtil().get(self.URL + "/trade/api/v1/withdraw", dit)
