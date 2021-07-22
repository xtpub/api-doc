# _*_ coding:utf-8 _*_
# BASE_URL = "http://xtapi.testdev.fun"
BASE_URL = "http://api.xt.pub"


class APIConfig(type):
    """ API handle """
    
    exclude_funcs = ('__new__', '__init__')
    def __new__(cls, name, bases, attrs:dict):
        
        [attrs.update({key: BASE_URL + api}) for key, api in attrs.items() if key.islower() and isinstance(key, str)]
        
        return type.__new__(cls, name, bases, attrs)


class Api(object, metaclass=APIConfig):
    """ All interfaces requested """
    
    # Get timestamp from server 
    get_server = '/trade/api/v1/getServerTime'
    
    # Get trade account type
    get_account = '/trade/api/v1/getAccounts'
    
    # Get trade config from market
    get_market_config = '/data/api/v1/getMarketConfig'
    
    # Get Kline
    get_kline = '/data/api/v1/getKLine'
    
    # Access to 24 hours of trading
    get_ticker = '/data/api/v1/getTicker'
    
    # Obtain all trading quotations within 24 hours
    get_tickers = '/data/api/v1/getTickers'
    
    # Get the latest trading depth
    get_depth = '/data/api/v1/getDepth'
    
    # Get the latest transaction data
    get_trades = '/data/api/v1/getTrades'
    
    # Get balance of account
    get_balance = '/trade/api/v1/getBalance'
    
    # Gets the specified account assets
    get_funds = '/trade/api/v1/getFunds'
    
    # Place a order and Commissioned order
    place_order = '/trade/api/v1/order'
    
    # Batch order
    batch_order = '/trade/api/v1/batchOrder'
    
    # Cancel order
    cancel_order = '/trade/api/v1/cancel'
    
    # Batch cancel
    batch_cancel = '/trade/api/v1/batchCancel'
    
    # OrderLine
    get_order = '/trade/api/v1/getOrder'
    
    # Obtain outstanding orders
    get_open_orders = '/trade/api/v1/getOpenOrders'
    
    # Get multiple order information
    get_batch_orders = '/trade/api/v1/getBatchOrders'
    
    
api = Api()    


class AuthKey:
    
    PUBLIC_KEY = 'xxxxxxxxxxxxxxxxxx'
    SECRET_KEY = 'xxxxxxxxxxxxxxxxxx'


if __name__ == "__main___":
    api  = Api()
    print(api.get_account)
