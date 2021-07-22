# _*_ coding:utf-8 _*_
import time
import hmac
import hashlib
import urllib.parse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Auth:
    """Create auth signed  """
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(Auth, "_instance"):
            Auth._instance = object.__new__(cls)
        return Auth._instance
    
    
    def __init__(self, apiKey, secretKey):
        self._apiKey:str = apiKey
        self._secretKey:str = secretKey

    @property
    def apiKey(self):
        return self._apiKey
    
    @apiKey.setter
    def apiKey(self, apiKey):
        self._apiKey = apiKey
        
    @property
    def secretKey(self):
        return self._secretKey
    
    @secretKey.setter
    def secretKey(self, secretKey):
        self._secretKey = secretKey
    
    def create_payload(self, payload:dict) -> dict:
        if not all([payload.get('accesskey'), payload.get('nonce')]):
            payload['accesskey'] = self._apiKey
            payload['nonce']  = str(int(time.time() * 1000))

            # Need sorted
            params = urllib.parse.urlencode(dict(sorted(payload.items(), key = lambda kv:(kv[0], kv[1]))))
            signature = self._create_signed(params)
            
            payload['signature'] = signature
        return payload
    
    def _create_signed(self, params:str) -> str:
        signature = hmac.new(self._secretKey.encode('utf-8'), params.encode('utf-8'), hashlib.sha256).hexdigest().upper()
        return signature
        


def get_auth_payload(param:dict) -> dict:
    """ return payload contains request params"""
    from xt_client_conf import AuthKey
    
    auth = Auth(AuthKey.PUBLIC_KEY, AuthKey.SECRET_KEY)
    return auth.create_payload(param)


