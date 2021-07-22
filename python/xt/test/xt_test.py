    
    def test_init(self):
        
        pb = PublicRequestAPI()
        res = pb.get_server_time()
        print(type(res[1]))
        
        self.assertTrue(isinstance(res[0], bool))
        self.assertEqual(res[1].get('code'), 200)
        
        self.assertTrue(isinstance(res[1], dict))
        self.assertTrue(res[1].__contains__("data"))
        self.assertTrue(res[1].__contains__("info"))
        print("test init >>>", res)

    
    def test_depth(self):
        
        params = {
            "market":"btc_usdt"
        }
        
        pb = PublicRequestAPI()
        status, data, _ =  pb.get_depth(params)
        
        self.assertTrue(isinstance(data, dict))
        self.assertTrue(data.__contains__("asks"))
        self.assertTrue(data.__contains__("bids"))
        self.assertTrue(isinstance(data['asks'], list))
        self.assertTrue(isinstance(data['bids'], list))
        self.assertTrue(status)
        # print("test depth >>>", data)
    
    
    def test_ticker(self):
        
        params = {
            "market":"btc_usdt"
        }
        
        pb = PublicRequestAPI()
        status, data, _ = pb.get_ticker(params)
        
        self.assertTrue(status)
        self.assertTrue(isinstance(data, dict))
        
        assert data.get('pricd') is None
        # print("test ticker >>> ", data)
    
    
    def test_kline(self):
        
        param = {'market':'btc_usdt','type':'1min','since':0}
        
        pb = PublicRequestAPI()
        status, data, _ = pb.get_klines(param)
        
        self.assertTrue(status)
        self.assertTrue(isinstance(data, dict))
        
        # print("test kline >>> ", data)
    
    
    def test_balance(self):
        
        accesskey = 'xxxxxxxxxxxxxxxxxxxx'
        secretkey = 'xxxxxxxxxxxxxxxxxxxx'
        sra = SignedRequestAPI(accesskey, secretkey)
        
        status, data, _ = sra.get_balance()
        self.assertTrue(status)
        self.assertTrue(isinstance(data, dict))
        
        assert data.get('info') == "Success"
        assert len(data.get('data')) > 0
        """ ¡®Forth¡¯ is my test account, if not ¡®Forth¡¯ account please switch   """
        assert data['data'].get('forth') and data['data'].get('usdt')
        
        print("test balance >>> ", data)

    def test_order(self):
        
        accesskey = 'xxxxxxxxxxxxxxxxxxxx'
        secretkey = 'xxxxxxxxxxxxxxxxxxxx'
        sra = SignedRequestAPI(accesskey, secretkey)  
        
        params = {
            'market': "forth_usdt",
            'price': 4.44,
            'type': 0,
            'number':6,
            'entrustType':0,
            }
        
        status, data, _ = sra.palce_order(params)
        
        assert data.get('code') == 200
        self.assertTrue(status)
        self.assertTrue(isinstance(data, dict))
        
                
        print("test order >>> ", data)
    
    
    def test_camcel(self):
        
        accesskey = 'xxxxxxxxxxxxxxxxxxxx'
        secretkey = 'xxxxxxxxxxxxxxxxxxxx'
        sra = SignedRequestAPI(accesskey, secretkey)  
        
        params = {
                'market':'forth_usdt',
                'id':'6823168236830742528'
        }
        
        status, data, _ = sra.palce_order(params)
        
        assert  data.get('code') == 200
        assert data.get('data') is not None
        self.assertTrue(status)
        self.assertTrue(isinstance(data, dict))
        
        print('test cancel >>> ', data)
    
    
    def test_opens(self):
        
        accesskey = 'xxxxxxxxxxxxxxxxxxxx'
        secretkey = 'xxxxxxxxxxxxxxxxxxxx'
        sra = SignedRequestAPI(accesskey, secretkey)  
        
        params = {
                'market':'forth_usdt',
        }
        
        status, data, _ = sra.get_unfinished_order(params)
        
        assert  data.get('code') == 200
        assert data.get('data') is not None
        self.assertTrue(status)
        self.assertTrue(isinstance(data, dict))
        
        print('test opens >>> ', data)
        pass
    
