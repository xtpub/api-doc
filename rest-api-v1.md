## 接入说明

### REST API

``
https://api.xt.com
``

鉴于延迟高和稳定性差等原因，不建议通过代理的方式访问Ubiex API。

请求头信息请设置为：`Content-Type=application/x-www-form-urlencoded`

<br/>

### 限频规则

获取资产每秒3次，其他方法单个用户每秒10次，单个IP每分钟1000次，超出锁定账户10分钟。

<br/>

### 签名说明


使用API请求在通过 internet 传输的过程中极有可能被篡改，为了确保请求未被更改，除公共接口（基础信息，行情数据）外的私有接口均必须使用您的 API Key 做签名认证，以校验参数或参数值在传输途中是否发生了更改。每一个API Key需要有适当的权限才能访问相应的接口。每个新创建的API Key都需要分配权限。权限类型分为：读取，交易，提币。在使用接口前，请查看每个接口的权限类型，并确认你的API Key有相应的权限。


一个合法的请求由以下几部分组成：

方法请求地址：即访问服务器地址 `api.xt.com`，比如 `api.xt.com/trade/api/v1/order`。

API 访问密钥（accesskey）：您申请的 API Key 中的 Access Key。

时间戳（nonce）：您应用程序发出请求的时间戳，13位毫秒数，Ubiex将根据这个时间戳检验您API请求的有效性。

签名(signature)：签名计算得出的值，用于确保签名有效和未被篡改，Ubiex使用 `HmacSHA256`。

<br/>

### 签名步骤

规范要计算签名的请求 因为使用 HMAC 进行签名计算时，使用不同内容计算得到的结果会完全不同。所以在进行签名计算前，请先对请求进行规范化处理。下面以查询某订单详情请求为例进行说明：


`https://api.xt.com/trade/api/v1/getOrder?accesskey={AccessKey}&market={Market}&nonce={Timestamp}&id={OrderId}&signature={Signature}`

按照ASCII码的顺序对参数名进行排序,将各参数使用字符 “&” 连接，例如下面就是排序之后结果：

`accesskey=myAccessKey&id=123&market=btc_usdt&nonce=1562919832183`

需要注意的是nonce的值为13位毫秒数时间戳

使用网站申请得到的Secret Key对上面生成的参数串进行 `HmacSHA256` 签名。例如上述参数进行签名的结果：

`97b7b71741ca0aec6e0404a5b1c7cb2a78e7bd6c2a8088dbd84a20129dee4fe7`

最后把签名赋值到参数名signature并提交到服务器。

<br/>

### 返回格式

所有的接口返回都是JSON格式。

<br/>

### 错误代码

状态码 | 错误信息
-|:-
101 | 委托失败，未知的委托类型
102 | 委托失败，参数错误
103 | 委托失败，没有足够的资金
104 | 委托失败，未知异常请稍后再试
105 | 委托失败，委托数量不能低于系统设置最小委托数量
106 | 委托失败，委托频繁
107 | 操作失败，暂未开放交易
108 | 委托失败，触发价格不正确
109 | 委托失败，不支持市价单委托
110 | 委托失败，不支持止盈止损单委托
111 | 委托失败，超出系统保护价格
121 | 撤单失败，订单不存在或已取消
122 | 撤单失败，订单已取消或已完成
123 | 撤单失败，未知异常请稍后再试
124 | 撤单失败，操过频繁
404 | 其他错误提示

<br/>

### 行情数据

**交易市场配置**

``
    GET /data/api/v1/getMarketConfig
``

>请求参数

`None`

>响应数据
```js
{
  "ltc_usdt": {
    "minAmount": 0.00010,       // 最小下单数量
    "pricePoint": 2,            // 价格小数点
    "coinPoint": 4,             // 数量小数点
    "maker": 0.00100000,        // 主动单交易手续费
    "taker": 0.00100000         // 被动单交易手续费
  }
  "eth_usdt": {
    "minAmount": 0.00010,
    "pricePoint": 2,
    "coinPoint": 4,
    "maker": 0.00100000,
    "taker": 0.00100000
  },
  "btc_usdt": {
    "minAmount": 0.0000010,
    "pricePoint": 2,
    "coinPoint": 6,
    "maker": 0.00100000,
    "taker": 0.00100000
  }
}
```

<br/>

**K线数据**

``
    GET /data/api/v1/getKLine
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
type | string | true | N/A | K线类型 | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | 时间条件，控制增量 | 第一次为0,之后为响应的since的值即可

>响应数据
```js
// [时间戳，开盘价，最高价，最低价，收盘价，成交量，成交额]
{
  "datas": [
    [
      1562923200,
      11634.64,  
      11637.22,
      11627.58,
      11631.43,
      1.144578,
      13314.16264138
    ]
  ],
  "since": 1562923200
}
```

<br/>

**聚合行情（Ticker）**

``
    GET /data/api/v1/getTicker
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...

>响应数据
```js
{
  "high": 11776.93,
  "moneyVol": 33765013.61761934,    //成交额
  "rate": 1.3900,                   //24涨跌幅
  "low": 11012.17,
  "price": 11609.92,
  "ask": 11618.25,
  "bid": 11604.08,
  "coinVol": 2944.208780            //成交量
}
```

<br/>

**所有市场的最新 Ticker**

``
    GET /data/api/v1/getTickers
``

>请求参数

`None`

>响应数据
```js
{
  "ltc_usdt": {
    "high": 106.99,
    "moneyVol": 1589953.528784,
    "rate": 4.3400,
    "low": 97.51,
    "price": 105.52,
    "ask": 105.61,
    "bid": 105.46,
    "coinVol": 15507.7052
  },
  "btc_usdt": {
    "high": 11776.93,
    "moneyVol": 33765013.61761934,
    "rate": 1.3900,                 
    "low": 11012.17,
    "price": 11609.92,
    "ask": 11618.25,
    "bid": 11604.08,
    "coinVol": 2944.208780
  }
}
```

<br/>

**市场深度数据**

``
    GET /data/api/v1/getDepth
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...

>响应数据
```js
{
  "last": 11591.26,     //最新成交价
  "asks": [
    [
      11594.80,
      0.049472
    ],
    [
      11594.86,
      0.048462
    ]
  ],
  "bids": [
       [
         11590.06,
         0.188749
       ],
       [
         11588.42,
         0.030403
       ]
   ]
}
```

<br/>

**最近市场成交记录**

``
    GET /data/api/v1/getTrades
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...

>响应数据
```js
// [时间戳，成交价，成交数量，交易类型，记录ID]
[
  [
    1562924059762,
    11613.18,
    0.044448,
    "bid",
    156292405956105
  ],
  [
    1562924059006,
    11613.22,
    0.000086,
    "bid",
    156292405956104
  ]
]
```

<br/>
<br/>

### 交易 API

**获取服务器时间(不需要签名)**

``
    GET /trade/api/v1/getServerTime
``

>请求参数

`None`

>响应数据
```js
{
  "code": 200,
  "data": {
      "serverTime": 1562924059006
  },
  "info": "success"
}
```
<br/>

**获取交易(现货)账户资产**

``
    GET /trade/api/v1/getBalance
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 

>响应数据
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // 冻结
      "available": "0.00"   // 可用
    },
    "eth": {
      "freeze": "0.00",
      "available": "0.00"
    },
    "usdt": {
      "freeze": "3062.17437341",
      "available": "3867.43650012"
    },
    "ltc": {
      "freeze": "0.00",
      "available": "0.00"
    }
  },
  "info": "success"
}
```

<br/>

**获取账户类型(不需要签名)**

``
    GET /trade/api/v1/getAccounts
``

>请求参数

`None`

>响应数据
```js
// 固定的系统账户，可直接写死在程序中，不必动态获取
{
  "code":200,
  "data":[
  	{"name":"钱包账户","id":1},
  	{"name":"交易账户","id":2},
  	{"name":"法币账户","id":3}
  ],
  "info":"success"
}
```


<br/>

**获取指定账户资产**

``
    GET /trade/api/v1/getFunds
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
account | integer | true | N/A | 账户ID | 参考getAccounts接口
nonce | integer | true | N/A | 13位毫秒数 | 

>响应数据
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // 冻结
      "available": "0.00"   // 可用
    },
    "eth": {
      "freeze": "0.00",
      "available": "0.00"
    },
    "usdt": {
      "freeze": "3062.17437341",
      "available": "3867.43650012"
    },
    "ltc": {
      "freeze": "0.00",
      "available": "0.00"
    }
  },
  "info": "success"
}
```

<br/>

**账户间资金划转**

``
    POST /trade/api/v1/transfer
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
from | integer | true | N/A | 账户ID | 参考getAccounts接口
to | integer | true | N/A | 账户ID | 参考getAccounts接口
amount | float | true | N/A | 金额 | 
coin | string | true | N/A | 币种 |btc,eth,usdt... 
safePwd | string | true | N/A | 安全资金密码 | 

>响应数据
```js
{
	"code":200,
	"info":"Succeeded"
}
```

<br/>

**委托**

``
    POST /trade/api/v1/order
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
price | float | true | N/A | 委托价格 | 
number | float | true | N/A | 委托数量 | 
type | integer | true | N/A | 交易类型 | 1、买 0、卖
entrustType | integer | true | N/A | 委托类型 | 0、限价，1、市价

>响应数据
```js
{
  "code": 200,
  "data": {
    "id": 156292794190713
  },
  "info": "An order has been placed successfully"
}
```

<br/>

**批量委托**

``
    POST /trade/api/v1/batchOrder
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
data | string | true | N/A | 订单数据 | 

```
只支持限价委托，一次事务，要么都成功，要么都失败

data 是一个JSON数组，数组长度最大只支持100个，超出100的会被忽略100个以外的元素，数组元素格式为：

{
  "price": 1000,
  "amount": 1,
  "type" : 1    // 1、买 0、卖
}

组装完成之后，把JSON数组转为STRING，再进行Base64.encode()才是最终要提交的数据

请注意，data参与签名的不是JSON数据本身，而是Base64.decode()之后的STRING
```

>响应数据
```js
{
  "code": 200,
  "data": [
    {
      "amount": 0.0010,
      "price": 5000.0000,
      "id": 156292972664756,
      "type": 1
    },
    {
      "amount": 0.0020,
      "price": 5000.0000,
      "id": 156292972664757,
      "type": 1
    }
  ],
  "info": "An order has been placed successfully"
}
```

<br/>

**撤单**

``
    POST /trade/api/v1/cancel
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
id | integer | true | N/A | 订单ID |

>响应数据
```js
{
  "code": 200,
  "info": "The order has been canceled successfully"
}
```

<br/>

**批量撤单**

``
    POST /trade/api/v1/batchCancel
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
data | string | true | N/A | 订单数据 | 

```
data 是一个JSON数组，数组长度最大只支持100个，超出100的会被忽略100个以外的元素，数组元素格式为订单ID，如：

[123, 456, 789]

组装完成之后，把JSON数组转为STRING，再进行Base64.encode()才是最终要提交的数据

请注意，data参与签名的不是JSON数据本身，而是Base64.decode()之后的STRING
```

>响应数据
```js
{
  "code": 200,
  "data": [
    {
      "msg": "The order has been canceled successfully",
      "code": 120,
      "id": 156293034776986
    },
    {
      "msg": "The order has been canceled successfully",
      "code": 120,
      "id": 156293034776987
    },
    {
      "msg": "Failed to cancel the order since it does not exist or has been canceled",
      "code": 121,
      "id": 156293034776988
    }
  ],
  "info": "The order has been canceled successfully"
}
```

<br/>

**订单信息**

``
    GET /trade/api/v1/getOrder
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
id | integer | true | N/A | 订单ID |

>响应数据
```js
{
  "code": 200,
  "data": {
    "number": "0.002000",           // 委托数量
    "price": "5000.00",             // 委托价格
    "avgPrice": "0.00",             // 成交均价
    "id": 156293034776987,          // 订单ID
    "time": 1562930348000,          // 委托时间
    "type": 1,                      // 交易类型：1、买 0、卖
    "status": 3,                    // 状态  (0、提交未撮合，1、未成交或部份成交，2、已完成，3、已取消，4、撮合完成结算中)
    "completeNumber": "0.000000",   // 完成数量
    "completeMoney": "0.000000",    // 完成金额
    "entrustType": 0,               // 订单类型：1、市价 0、限价
    "fee": "0.000000"               // 交易手续费
  },
  "info": "success"
}
```

<br/>

**获取未完成订单**

``
    GET /trade/api/v1/getOpenOrders
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
page | integer | false | 1 | 页码 | 
pageSize | integer | false | 10 | 订单数量 | [10-1000]

>响应数据
```js
{
  "code": 200,
  "data": [
    {
      "number": "0.002000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074105,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    },
    {
      "number": "0.001000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074104,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    }
  ],
  "info": "success"
}
```

<br/>

**获取多个订单信息**

``
    GET /trade/api/v1/getBatchOrders
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
data | string | true | N/A | 订单数据 | 

```
data 是一个JSON数组，数组长度最大只支持100个，超出100的会被忽略100个以外的元素，数组元素格式为订单ID，如：

[123, 456, 789]

组装完成之后，把JSON数组转为STRING，再进行Base64.encode()才是最终要提交的数据

请注意，data参与签名的不是JSON数据本身，而是Base64.decode()之后的STRING
```

>响应数据
```js
{
  "code": 200,
  "data": [
    {
      "number": "0.002000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074105,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    },
    {
      "number": "0.001000",
      "price": "5000.00",
      "avgPrice": "0.00",
      "id": 156293034074104,
      "time": 1562930340271,
      "type": 1,
      "status": 1,
      "completeNumber": "0.000000",
      "completeMoney": "0.000000",
      "entrustType": 0,              
      "fee": "0.000000"
    }
  ],
  "info": "success"
}
```

<br/>

**获取充值地址**

``
    GET /trade/api/v1/getPayInAddress
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
coin | string | true | N/A | 币种名称 | btc,eth,ltc...

>响应数据
```js
{
	"code": 200,
	"data": {
		"record": [{
			"chainName": "omni",    //链类型
			"chain": "btc",         //主链币种
			"address": "1EAEoYaXx93tKgvrfgpna19GPqC4J2Xcp7",  //充值地址
			"coin": "USDT",         //当前币种
			"memo": ""				//EOS等币种可能会存在memo
		}, 
		{
			"chainName": "usdt-erc20",
			"chain": "eth",
			"address": "0x8390b456fe03139ba402f45be9110a5fadf7e862",
			"coin": "USDT",
			"memo": ""
		}]
	},
	"info": "success"
}
```

<br/>

**获取提现地址**

``
    GET /trade/api/v1/getPayOutAddress
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
coin | string | true | N/A | 币种名称 | btc,eth,ltc...
page | integer | true | 1 | 分页页码 | 
pageSize | integer | true | 10 | 每页数量 | 


>响应数据
```js
{
	"code": 200,
	"data": {
		"record": [{
			"chainName": "ERC-20",      //主链名称
			"chain": "eth",             //主链币种
			"address": "0x8390b456fe03139ba402f45be9110a5fadf7e862", //提现地址
			"memo": "",    				//EOS等币种可能会存在memo             
			"coin": "usdt"              //当前币种
		}, {
			"chainName": "omni",
			"chain": "btc",
			"address": "1EAEoYaXx93tKgvrfgpna19GPqC4J2Xcp7",
			"memo": "",
			"coin": "usdt"
		}]
	},
	"info": "success"
}
```

<br/>

**获取充值记录**

``
    GET /trade/api/v1/getPayInRecord
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
coin | string | true | N/A | 币种名称 | btc,eth,ltc...
page | integer | true | 1 | 分页页码 | 
pageSize | integer | true | 10 | 每页数量 | 


>响应数据
```js
{
 	"code": 200,
 	"data": {
 		"total": 1,
 		"pageIndex": 1,
 		"record": [{
 			"chainName": "ERC-20",      //主链名称
 			"amount": 0.001000000,      //币种数量
 			"chain": "eth",             //主链币种
 			"address": "0x145e96ff8388e474df8c799fb433f103f42d9462",		//EOS等币种存在memo时用'_'隔开
 			"depth": 12,                //确认数
 			"creatTime": 1563465915000,
 			"manageTime": 1563466260000,
 			"txHash": "0x4bcd1207e57dc96737d20198c8792c3340386e7f247571458d17671b7834ddd6", //交易哈希
 			"status": 2,       			//0、初始 1、失败 2、成功 5、待确认
 			"coin": "usdt",             //当前币种
 			"innerTransfer": 0			//是否是内账地址转账的记录
 		}],
 		"pageSize": 100
 	},
 	"info": "success"
 }
```

<br/>

**获取提现记录**

``
    GET /trade/api/v1/getPayOutRecord
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
coin | string | true | N/A | 币种名称 | btc,eth,ltc...
page | integer | true | 1 | 分页页码 | 
pageSize | integer | true | 10 | 每页数量 | 


>响应数据
```js
{
	"code": 200,
	"data": {
		"record": [{
			"chainName": "ERC-20",      //主链名称
			"amount": 0.002000000,      //币种数量
			"chain": "eth",             //主链币种
			"address": "0x8390b456fe03139ba402f45be9110a5fadf7e862",    //EOS等币种存在memo时用'_'隔开
			"creatTime": 1563513678000, //提币时间
			"fee": 0.001000000,         //手续费
			"manageTime": 1563513698000,//处理时间
			"status": 4,				    //0、初始 1、失败/取消 2、成功 4、审核中 5、待确认
			"coin": "usdt",				//当前币种
			"innerTransfer": 0			//是否是内账地址转账的记录
		}]
	},
	"info": "success"
}
```

<br/>

**提现配置**

``
    GET /trade/api/v1/getWithdrawConfig
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 


>响应数据
```js
{
  "code": 200,
  "data": {
      "btc": {
          "minAmount": 0.01,    // 单次最小提现数量
          "maxAmount": 10      // 日提币额度
      },
      "eth": {
          "minAmount": 0.1,
          "maxAmount": 100
      }
  },
  "info": "success"
}
```

<br/>

**提现**

``
    GET /trade/api/v1/withdraw
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
accesskey | string | true | N/A | 访问密钥 | 
nonce | integer | true | N/A | 13位毫秒数 | 
coin | string | true | N/A | 币种名称 | btc,eth,ltc...
address | string | true | N/A | 提现地址 | 仅支持您在Ubiex的认证地址
memo | string | false | N/A | memo | 提现地址memo，如EOS等
amount | float | true | N/A | 提现数量 | 不能低于当前币种最低提现额度
innerTransfer | integer | false | 0 | 是否内部地址转账，享受0手续费 | 0、否 1、是
safePwd | string | true | N/A | 安全密码 | 


>响应数据
```js
{
  "code": 200,
  "data": {
  	  "fees":0.001000000,
  	  "amount":1,
  	  "address":"0xb1878d51e4a951e566a8c1bd206264077d959169",
  	  "id":1001,
  	  "subTime":1565717647769
  },
  "info": "success"
}
```
