## Access Description

### REST API


```
Official:
https://api.xt.com
```
```
Spare:
https://api.xt.pub
```

### Basic information of the interface

Due to the reasons of high latency and poor stability, it is not recommend to access the XT API through a proxy.

GET request parameters are put in query Params, POST request parameters are put in request body, please do not put parameters in query Params and request body at the same time

The request header information is set to: `Content-Type=application/x-www-form-urlencoded`

In addition to the parameters required by the interface itself, signature, which is the signature parameter, needs to be passed in the query Params or request body. The interface that does not need to pass the signature parameter will be additionally explained.
<br/>

### Frequency limiting rules

Get assets 3 times per second, other methods 10 times per second for each single user, 1000 times per minute for each single IP, exceeding the requested times, account will be locked for 10 minutes.
<br/>

### Signature Statement:

The request of API is likely to be tampered during the transmission through the Internet. In order to ensure that the request has not been changed, private interfaces other than public interfaces (basic information, market data) must use your API Key for signature verification to verify and check whether the parameter or parameter value has changed during the transmission. Each API Key needs proper permissions to access the corresponding interface. Every newly created API Key needs to be assigned permissions. Permission types are divided into: read, transaction and withdrawal. Before using the interface, please check the permission type of each interface and confirm that your API Key has the corresponding permission.


A legitimate request consists of the following parts:

Way to request an address: Accessing the server address `api.xt.com` such as `api.xt.com/trade/api/v1/order`.

API accesskey: There is the Access Key in the API Key you applied for.

Timestamp (nonce): The timestamp of your application's request, 13-bit milliseconds. XT will verify the validity of your API request based on this timestamp.

Signature: A value calculated by the signature to ensure the signature is valid and has not been tampered. XT uses HmacSHA256.

### Signing steps

Standardize the request to calculate signature. When HMAC is used for signature calculation, the calculation result using different content will be completely different. Therefore, before performing signature calculation, please standardize the request. The following takes the query of an order details request as an example:

`https://api.xt.com/trade/api/v1/getOrder?accesskey={AccessKey}&market={Market}&nonce={Timestamp}&id={OrderId}&signature={Signature}`

Sort the parameter names according to the order of ASCII codes, and concatenate each parameter with the character "&".

`accesskey = myAccessKey & id = 123 & market = btc_usdt & nonce = 1562919832183`

Note that the value of nonce is a 13-bit millisecond number.

Use the Secret Key obtained from the website to sign the HmacSHA256 parameter string generated above.

For example, the signature of the above parameters results:

`97b7b71741ca0aec6e0404a5b1c7cb2a78e7bd6c2a8088dbd84a20129dee4fe7`

Finally, the signature is assigned to the parameter name signature and submitted to the server.
<br/>

### Return format
All interfaces’ returns are in JSON format.
<br/>

### Error code
Status code	| error information
-|:-
101	| Order failed, unknown order type
102	| Order failed, Parameter error
103	| Order failed, not enough funds
104	| Order failed, unknown exceptions, please try again later.
105	| Order failed, the number of orders cannot be lower than the minimum number set by the system
106	| Order failed, Operate too frequently
107	| Operation failed, not open for trading
108	| Order failed, incorrect triggered price
109	| Order failed, unsupported market price order
110	| Order failed, unsupported stop-limited order
111	| Order failed, exceed the protected price set by system
121	| Cancellation failed, order does not exist or has been cancelled
122	| Cancellation failed, order cancelled or completed
123	| Cancellation failed, Unknown error, please try again later.
124	| Cancellation failed, Operate too frequently
200 | Success
307 | AccessKey error
308 | Sign error
400 | Request error, Check whether the parameters are standardized
404	| Others error warning
<br/>

### Market data （No signature required）

**Trading market configuration**

``
GET /data/api/v1/getMarketConfig
``

>Request Parameter

`None`

>Response data

```js

{
  "ltc_usdt": {
    "minAmount": 0.00010,       // minimum order quantity
    "minMoney": 0,		// minimum order money
    "pricePoint": 2,            // price decimal point
    "coinPoint": 4,             // number decimal point
    "maker": 0.00100000,        // Active transaction fee
    "taker": 0.00100000         // Passive transaction fee
  }
  "eth_usdt": {
    "minAmount": 0.00010,
    "minMoney": 0,
    "pricePoint": 2,
    "coinPoint": 4,
    "maker": 0.00100000,
    "taker": 0.00100000
  },
  "btc_usdt": {
    "minAmount": 0.0000010,
    "minMoney": 0,
    "pricePoint": 2,
    "coinPoint": 6,
    "maker": 0.00100000,
    "taker": 0.00100000
  }
}
```
<br/>

**Kline/Candlestick data**

``
GET /data/api/v1/getKLine
``

>Request Parameter

Parameter | Type | True or false | Default Value | Description | Ranges
-|-|-|-|-|-
market | string	 | true | N/A | Market pair | btc_usdt, eth_usdt...
type | string | true | N/A | Kline type | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | Time condition. Control increment | The first time is 0, after that follow the value of the since

>Response data

```js
// [Timestamp, Open price, Highest price, Lowest price, Close price, Volume, Turnover]
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

**Aggregated Markets （Ticker）**

``
GET /data/api/v1/getTicker
``

>Request Parameter

Parameter | Type | True or false |Default Value |Description | Ranges
-|-|-|-|-|-
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...

>Response data

```js
{
  "high": 11776.93,                 // Highest price in 24 hours
  "low": 11012.17,                  // Lowest price in 24 hours
  "rate": 1.3900,                   // Changes within 24 hours
  "price": 11609.92,                // Last traded price
  "ask": 11618.25,                  // First sell order
  "bid": 11604.08,                  // First buy order
  "coinVol": 2944.208780,           // Volume
  "moneyVol": 33765013.61761934     // Turnover
}
```
<br/>

**Latest Ticker of all markets**

``
GET /data/api/v1/getTickers
``
>Request Parameter
`None`
>Response data
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

**Market Depth data**

``
GET /data/api/v1/getDepth
``
>Request Parameter

Parameter | Type | True or false | Default value |Description | Ranges
-|-|-|-|-|-
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...

>Response data
```js
{
  "last": 11591.26,     // Latest transaction price
  "asks": [             // Seller
    [
      11594.80,         //Turnover
      0.049472          //Volume
    ],
    [
      11594.86,
      0.048462
    ]
  ],
  "bids": [             //Buyer
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

**Latest Market transactions record**

``
GET /data/api/v1/getTrades
``
>Request Parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...

>Response data
```js
// [Timestamp, deal price, volume, Transaction type, Record ID]
[
  [
    1562924059762,
    11613.18,
    0.044448,
    "bid",
    156292405956105
  ],
  [
    1562924059006,      // Timestamp
    11613.22,           // Turnover
    0.000086,           // Volume
    "bid",              // Trading type [bid:buy ask：sell]
    156292405956104     // Record ID
  ]
]
```
<br/>
<br/>

### Trading API

**Get server time (no signature required)**

``
GET /trade/api/v1/getServerTime
``
>Request Parameter

`None`

>Response data

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

**Get trading (spot) account assets**

``
GET /trade/api/v1/getBalance
``
>Request Parameter


Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds|

>Response data
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // freeze
      "available": "0.00"   // available
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

**Get the account type(no signature required)**

``
GET /trade/api/v1/getAccounts
``
>Request Parameter

`None`

>Response data
```js
// Fixed system account, which can be directly written into the program without obtaining dynamically
{
  "code":200,
  "data":[
  	{"name":" wallet account ","id":1},
  	{"name":" Trading account ","id":2},
  	{"name":" Fiat account ","id":3}
  ],
  "info":"success"
}
```
<br/>

**Get specific account assets**

``
GET /trade/api/v1/getFunds
``
>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key
account|integer|true|N/A|account ID|Refer to getAccounts interface
nonce|integer|true|N/A|"13-bit milliseconds

>Response data
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // freeze
      "available": "0.00"   // available
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

**Place a new order**

``
POST /trade/api/v1/order
``
>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds|
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...
price|float|true|N/A|Order Price|
number|float|true|N/A|Order quantity|
type|integer|true|N/A|Trading type|1, buy, 0 sell
entrustType|integer|true|N/A|Order type|0, limit price,1 market price

>Response data
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

**Bulk Orders**

``
POST /trade/api/v1/batchOrder
``

>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds|
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...
data|string|true|N/A|Order data|

```js
Only limit orders are supported. One transaction will either succeed or failed.

Data is a JSON array. The maximum length of the array is only 100. Anything beyond 100 will be ignored. The format of the array element is as following:

{
  "price": 1000,
  "amount": 1,
  "type" : 1    // 1, buy, 0 sell
}
After the assembly is completed, the JSON array is converted to STRING, and then Base64.encode () is the final data to be submitted.

Please note that data is not involved in signing the JSON data itself, but STRING after Base64.decode ()
```

>Response data
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

**Cancel an order**

``
POST /trade/api/v1/cancel
``
>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds|
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...
id|integer|true|N/A|Order ID|

>Response data
```js
{
  "code": 200,
  "info": "The order has been canceled successfully"
}
```
<br/>

**Cancel the Bulk Orders**

``
POST /trade/api/v1/batchCancel
``
>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds|
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...
data|string|true|N/A|Order data|

```
Data is a JSON array. The maximum length of the array is only 100. Anything beyond 100 will be ignored. The format of the array element is the order ID, such as:

[123, 456, 789]

After the assembly is completed, the JSON array is converted to STRING, and then Base64.encode () is the final data to be submitted.

Please note that data is not involved in signing the JSON data itself, but STRING after Base64.decode ()
```
>Response data
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

**Order information**

``
GET /trade/api/v1/getOrder
``

>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds|
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...
id|integer|true|N/A|Order ID|

>Response data
```js
{
  "code": 200,
  "data": {
    "number": "0.002000",           // Order amount
    "price": "5000.00",             // Order price
    "avgPrice": "0.00",             // Average price
    "id": 156293034776987,          // Order ID
    "time": 1562930348000,          // Order time
    "type": 1,                      // Trading type：1、buy 0、sell
    "status": 3,                    // Status (0, submission not matched, 1, unsettled or partially completed, 2, completed, 3, cancelled, 4,matched but in the settlement)
    "completeNumber": "0.000000",   // Completed Quantities
    "completeMoney": "0.000000",    // Completed amount
    "entrustType": 0,               // Order type：1、Market price 0、Limited price
    "fee": "0.000000"               // Trading fees
  },
  "info": "success"
}
```
<br/>

**Get uncompleted Orders**

``
GET /trade/api/v1/getOpenOrders
``
>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds |
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...
page|integer|false|1|page number|
pageSize|integer|false|10|Order quantities|[10-1000]

>Response data
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

**Get a batch of orders information**

``
GET /trade/api/v1/getBatchOrders
``
>Request parameter

Parameter|Type|True or false|Default value|Description|Ranges
-|-|-|-|-|-
accesskey|string|true|N/A|Access private key|
nonce|integer|true|N/A|13-bit milliseconds|
market|string|true|N/A|Market pair|btc_usdt, eth_usdt...
data|string|true|N/A|Order data|

```
data is a JSON array. The maximum length of the array is only 100. Anything beyond 100 will be ignored. 

The format of the array element is the order ID, such as:[123, 456, 789]

After the assembly is completed, the JSON array is converted to STRING, and then Base64.encode () is the final data to be submitted.

Please note that data is not involved in signing the JSON data itself, but STRING after Base64.decode ()
```

>Response data
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



















