# _*_ coding:utf-8 _*_
import requests
import base64
import json
import random
import time
from functools import wraps
from abc import abstractmethod

# Append sys path
import json

from xt_client_conf import Api
from xt_utils import *
from logging import Logger
logger = Logger(__file__)


class RequestAPI:
    """ 
    Base request 
    
    @Mehtod :: request method
    @url :: request url
    @params :: request data
    @return :: Auto
    
    
    The easiest way to register is to pass in the callback function as a parameter, 
    otherwise you need to refactor the schema involved

    ::param INTERVAL run period 
    ::parma TIMEOUT  run timeout 
    ::parma TRY      error retry times
    
    ::Return (status, data , response)
        ::parma status Request status is bool
        ::parma data   Response data is json 
        ::parma response  Origin Response
    """
    INTERVAL = 0.3
    TIMEOUT = 1 << 3 
    TRY = 3
    
    def __init__(self):
        self.timer_active = True
        self.__t = None
    
    def _request(self,method, url, parmas:dict):
        i = 0 
        response = ''
        if not self.timer_active:
            return
        
        if method.upper() == "GET":
            # get
            while i < self.TRY:
                try:
                    response = requests.get(url=url,params=parmas, timeout = self.TIMEOUT)
                    response.raise_for_status()
                    
                except requests.exceptions.RequestException as e:
                    logger.info(f'Request timeout, retry operation::[{e}]........')
                else:
                    if response.status_code == 200 and response:
                        # self.timer_active = False
                        res = response.json()
                        return True, res, response
                finally:
                    time.sleep(random.randint(1,3))
                    i += 1
                    print(f"Please wait a moment...retry now... times is {i}")
            else:
                logger.error(f'error Request timeout, retry operation failed::{url}::{parmas}')

            
        elif method.upper() == 'POST':
            # post
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'

            }

            while i < self.TRY:
                try:
                    
                    response = requests.post(url=url, headers=headers, data=parmas, timeout = self.TIMEOUT )
                    response.raise_for_status()
                    i += 1
                    
                    if response.status_code == 200 and response:
                        # self.timer_active = False
                        res = response.json()
                        return True, res, response
                except requests.exceptions.RequestException as e:
                    logger.info(f'Request timeout, retry operation::[{e}]........')
                    
                finally:
                    time.sleep(random.randint(1,3))
                    i += 1
                    print(f"Please wait a moment...retry now... times is {i}")
                    
            else:
                logger.error(f'error Request timeout, retry operation failed::{url}::{parmas}')
        else:
            raise TypeError(" Request method error , Please use post or get ....")

        logger.info(f'request info:>>{parmas}\n {response.text if response else response}')
        return False, parmas, response
    
        # self.__t = Timer(self.INTERVAL, self._request(method, url, parmas))
        # self.__t.start()
        
    def request(self,method, url, parmas:dict):
        self.timer_active = True
        
        try:
            response = self._request(method, url, parmas)
        except (requests.exceptions.HTTPError,requests.exceptions.ConnectTimeout) as err:
            #handel logging 
            logger.error(f"request error :{err}")
            response = False,None,None
        return response
    
    
    def response_to_format(self, data):
        return json.dumps(data, ensure_ascii=False)
    
    def get_server_time(self, method:str, url:str, kwargs:dict) -> str:
        """ Get server time now """
        return self.request(method, url, kwargs)
    
    def get_account(self,method,url,kwargs):
        """ Get account info """
        return self.request(method,url,kwargs)
    
    def get_all_market_config(self,method,url,kwargs):
        """ Access all market config """
        return self.request(method,url,kwargs)
    
    def get_klines(self, method,url,kwargs):
        """ Get Klines """
        return self.request(method,url,kwargs)

    def get_ticker(self, method,url,kwargs):
        """ Aggregate market """
        return self.request(method,url,kwargs)

    def get_tickers(self,method,url,kwargs):
        """ All aggregate market """
        return self.request(method,url,kwargs)

    def get_depth(self, method,url,kwargs):
        """ Gain market depth """
        return self.request(method,url,kwargs)

    def get_trades(self, method,url,kwargs):
        """ Get trade history """
        return self.request(method,url,kwargs)
    
# ---------------------------------------------------------------------------
    def get_balance(self, method,url,kwargs):
        """ Get account balance """
        return self.request(method,url,kwargs)

    def get_fund(self, method,url,kwargs):
        """ Gets the corresponding information for an account """
        return self.request(method,url,kwargs)

    def palce_order(self, method,url,kwargs):
        """ Order """
        return self.request(method,url,kwargs)

    def palce_orders(self, method,url,kwargs):
        """ Orders """
        return self.request(method,url,kwargs)
    
    def cancel_order(self, method,url,kwargs):
        """ Cancel order """
        return self.request(method,url,kwargs)
    
    def cancel_orders(self, method,url,kwargs):
        """ Cancel orders """
        return self.request(method,url,kwargs)
    
    def get_order(self, method,url,kwargs):
        """ Get order """
        return self.request(method,url,kwargs)
        
    def get_unfinished_order(self, method,url,kwargs):
        """ Obtain outstanding orders """
        return self.request(method,url,kwargs)
    
    def get_orders(self, method,url,kwargs):
        """ Obtain all orders information"""
        return self.request(method,url,kwargs)
    


class PublicRequestAPI(RequestAPI):
    """ Public request """
    
    def get_server_time(self):
        """
        @Method : GET
        @Return : josn
        """
        return super(PublicRequestAPI, self).get_server_time('GET', Api.get_server,  {})
    
    def get_account(self):
        """ Get account info """
        return super(PublicRequestAPI, self).get_account('GET', Api.get_account, {})
    
    def get_all_market_config(self):
        """ Access all market config """
        return super(PublicRequestAPI, self).get_all_market_config('GET',Api.get_market_config, {})
    
    def get_klines(self, kwargs:dict):
        """ 
        Get Klines 
        @Example:
            @Kwargs : {'market':'btc_usdt','type':'1min','since':0}
            @Return : {"datas":
            [[1607370060, 18935.99, 18964.13, 18926.58, 18950.02, 1.3156, 24932.181068],
             [1607370180, 18961.49, 18963.05, 18953.89, 18959.17, 0.963, 18257.544006]]}
        """
        return super(PublicRequestAPI, self).get_klines('GET',Api.get_kline, kwargs)

    def get_ticker(self, kwargs):
        """ 
        Aggregate market 
        
        @Example:
            @kwargs: dict(market=btc_usdt)
            @Retrun: 
            {   "high": 11776.93, 
                "moneyVol": 33765013.61761934, //成交额 
                "rate": 1.3900, //24涨跌幅 
                "low": 11012.17, 
                "price": 11609.92, 
                "ask": 11618.25, 
                "bid": 11604.08, 
                "coinVol": 2944.208780 //成交量 
            }
        """
        return super(PublicRequestAPI, self).get_ticker('GET',Api.get_ticker,kwargs)

    def get_tickers(self):
        """ 
        All aggregate market
        @Example:
            @kwargs: None
            @Return: ... 
        """
        return super(PublicRequestAPI, self).get_tickers('GET',Api.get_tickers, {})

    def get_depth(self, kwargs):
        """ 
        Gain market depth
        @Example:
            @Kwargs:  dict(market=btc_usdt)
            @Return: ...
        """
        return super(PublicRequestAPI, self).get_depth('GET',Api.get_depth,kwargs)

    def get_trades(self, kwargs):
        """ 
        Get trade history 
        @Example:
            @Kwargs: dict(market=btc_usdt)
            @Return: ...
        """
        return super(PublicRequestAPI, self).get_trades('GET',Api.get_trades,kwargs)
    

class SignedRequestAPI(RequestAPI):
    """
    
    Singed request 
    
    """
    def __init__(self, accesskey, secretkey):
        super().__init__()
        self.user = None
        self._accesskey = accesskey
        self._secretkey = secretkey
        self._api = self.signe_api()
    
    def signe_api(self):
        return Auth(self._accesskey,  self._secretkey)
    
    
    def request(self, method, url, kwrags):
        params = self._api.create_payload(kwrags)
        self.timer_active = True
        try:
            response = self._request(method, url, params)
        except requests.exceptions.HTTPError as err:
            #handel logging 
            logger.error(err)
            response = False, None, None
            
        return response
    
    def get_balance(self):
        
        """ 
        Get account balance 
            @Example:
                @Kwargs: dict(accesskey=82e8fb09-71a2-4954-b74e-1a86ff370e8f&
                nonce=1607326707452&
                signature=14C11ABF80A1CB1EECB3AA1AEC8C50447195121FEE12A5B2F10F639F8A43E9C3)
            @Return: ...
        """
        
        return self.request('GET',Api.get_balance, {})

    def get_fund(self,kwargs):
        
        """ 
        Gets the corresponding information for an account 
            @Example:
                @Kwargs: dict(accesskey=82e8fb09-71a2-4954-b74e-1a86ff370e8f&
                nonce=1607329670621
                &signature=40F87CDE1C99BD8ECCA8F4E30BCBE76B55DEF852B31605DFF5F12FA8C1B094D3)
            @Return: ...
        """
        
        return self.request('GET',Api.get_funds,kwargs)

    def palce_order(self, kwargs):
        
        """ 
        Order 
        @Example:
            @Kwargs: dict(market=btc_usdt&
            price=19243.84&
            number=0.0001&
            type=1&
            entrustType=0&
            accesskey=82e8fb09-71a2-4954-b74e-1a86ff370e8f&
            nonce=1607330801850&
            signature=80795D28D0EB231800503B4880C71D94B1E7803FB865A48007E1692BAF7BB71B)
            @Return :...
        """
        
        return self.request('POST',Api.place_order,kwargs)

    def palce_orders(self, kwargs):
        
        """ 
        Orders 
        @Example:
            @Kwargs: {
                'market':'btc_usdt',  # kinds
                'data':[{ 
                    'price':'19243.84', 
                    'amount':'0.0001', 
                    "type":0,
                    }]
                }
            @Return：...
        """
        
        order_lines = json.dumps(kwargs['data'])
        order_lines = base64.b64encode(order_lines.encode('utf-8'))
        kwargs['data'] = str(order_lines, 'utf-8')
        
        return self.request('POST',Api.batch_order,kwargs)
    
    def cancel_order(self, kwargs):
        
        """ 
        Cancel order 
        @Example:
            @Kwargs: {
                'market':'btc_usdt',
                'id':'160739901250175'
                }
            @Return:
        """
        
        return self.request('POST',Api.cancel_order,kwargs)
    
    def cancel_orders(self, kwargs): 
        
        """ 
        Cancel orders 
        @Example:
            @Kwargs: {
                'market':'btc_usdt',
                'data':['160739901250175']
                } 
            @Return:
        """
        order_lines = json.dumps(kwargs['data'])
        order_lines = base64.b64encode(order_lines.encode('utf-8'))
        kwargs['data'] = str(order_lines, 'utf-8')
        
        return self.request('POST', Api.batch_cancel,kwargs)
    
    def get_order(self, kwargs):
        
        """ 
        Get order 
        @Example:
            @Kwargs: 
            @Return:
        """
        
        return self.request('GET', Api.get_order, kwargs)
        
    def get_unfinished_order(self, kwargs):
        
        """ 
        Obtain outstanding orders 
        @Example:
            @Kwargs: {
                'market':'btc_usdt',
                'page':'1',
                'pageSize':10
                }
            @Return:
        """
        kwargs.setdefault('page', 1)
        kwargs.setdefault('pageSize', 10)
        
        
        return self.request('GET', Api.get_open_orders ,kwargs)
    
    def get_orders(self, kwargs):
        
        """ 
        Obtain all orders information
        @Example:
            @Kwargs: {
                'market':'btc_usdt',
                'data':['160739901250175']
                }
            @Return:
        """
        order_lines = json.dumps(kwargs['data'])
        order_lines = base64.b64encode(order_lines.encode('utf-8'))
        kwargs['data'] = str(order_lines, 'utf-8')
        
        return self.request('GET', Api.get_batch_orders,kwargs)





class XTClientSDK:
    
    """
    ::parma isauth 
    ::parma args ---- > (accesskey, secrectkey)
    ::parma kwargs ---> {'accesskey': xxxx, 'secrectkey' : xxxxx}
    """
    def __init__(self, isauth :bool =False):
        self.isauth = isauth
        if not self.isauth:
            self._api = PublicRequestAPI
        else:
            self._api = SignedRequestAPI
    
    def __call__(self, *args, **kwargs):
        
        if not args and not kwargs and not self.isauth:
            return self._api()
        
        if args and self.isauth:
            
            ak, sk = self.__check_args__(*args)
            return self._api(ak, sk)
            
        if kwargs and self.isauth:
            ak, sk = self.__check_kwargs__(*args)
            return self._api(ak, sk)
        
        return self._api()
    
    def __check_args__(self, *args):
        return args
    
    def __check_kwargs__(self, **kwargs):
        ak, sk = kwargs.get('accesskey'), kwargs.get('secrectkey')
        return ak, sk
