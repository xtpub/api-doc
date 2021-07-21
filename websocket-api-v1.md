## 接入说明

### WEBSOCKET API

```
正式:
wss://xtsocket.xt.com/websocket
```
```
备用:
wss://xtsocket.xt.pub/websocket
```



<br/>

### 数据压缩

WebSocket API 的所有数据都 GZIP 压缩之后再进行 Base64.encode() 编码并使用二进制方式返回，需要 client 在收到二进制数据之后进行解码解压。

<br/>

### 心跳消息


当用户的Websocket客户端连接到XT Websocket服务器后，服务器会定期（当前设为5秒）向其发送ping消息并包含一个时间戳，

当用户接收到此心跳消息后，应及时返回pong消息并包含同一时间戳，格式如：

```js
{"ping": 1562979600}

{"pong": 1562979600}
```

当Websocket服务器连续三次发送了`ping`消息却没有收到任何一次`pong`消息返回后，服务器将主动断开与此客户端的连接。

当然，用户连接到服务器后，也可以主动向服务器发送消息`ping`，当服务器接到信息为`ping`字符串后主动返回一个`pong`的字符串。

<br/>

### 断开连接

用户主动断开或者主动向XT Websocket服务器发送消息`close`；

<br/>

### 订阅主题

成功建立与Websocket服务器的连接后，Websocket客户端应发送如下请求以订阅特定主题：

```js

{"channel":"ex_single_market","market":{Market},"event":"addChannel"}

{"channel":"ex_group_market","group":{Group},"event":"addChannel"}

{"channel":"ex_last_trade","market":{Market},"since":{Since},"event":"addChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"addChannel"}

{"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}


```


成功订阅后，Websocket客户端将收到对应主题返回的全量数据，

之后, 一旦所订阅的主题有更新，Websocket客户端将收到服务器推送的更新消息（push）：

<br/>

### 取消订阅

取消订阅的格式如下：

```js
{"channel":"ex_single_market","market":{Market},"event":"removeChannel"}

{"channel":"ex_group_market","group":{Group},"event":"removeChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}

{"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}

{"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}

```


<br/>


**K线数据**

订阅

``
   {"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}
``

退订

``
   {"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
interval | string | true | N/A | K线类型 | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | 时间条件 | 0或需要的时间节点的时间戳，10位秒级

>响应数据
```js
//[时间戳，开盘价，最高价，最低价，收盘价，成交量，成交额]
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "records":[[1562987700,101.0,101.0,101.0,101.0,4.0,404.0]], 
        "channel":"ex_chart_update",
        "interval":"15min",
        "isFull":true,
        "since":1562987700
    },
    "info":"success"
}
```

``
    说明：用户订阅成功之后，会返回一次根据since过滤的全量数据，并且在data里有一个isFull为true的字段做为标识，之后, 一旦有更新，Websocket客户端将收到服务器推送的增量消息。
``

<br/>

**聚合行情（Ticker）**

订阅

``
   {"channel":"ex_single_market","market":{Market},"event":"addChannel"}
``

退订

``
   {"channel":"ex_single_market","market":{Market},"event":"removeChannel"}
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...

>响应数据
```js
// [市场名称，市场分组，当前价格，涨跌幅，最高价，最低价，成交量，成交额]
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "records":[["eth_usdt",1,101.00,1.98,101.00,101.00,4.0000,404.000000]],
        "channel":"ex_single_market"
    },
    "info":"success"
}
```

<br/>

**分组聚合行情（Tickers）**

订阅

``
   {"channel":"ex_group_market","group":{Group},"event":"addChannel"}
``

退订

``
   {"channel":"ex_group_market","group":{Group},"event":"removeChannel"}
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
group | string | false | all | 分组类型 | all或交易区(如：usdt)或交易对(如：btc_usdt)

>响应数据
```js
// [市场名称，市场分组，当前价格，涨跌幅，最高价，最低价，成交量，成交额]
{
    "code":200,
    "data":{
        "records":[["eth_usdt",1,103.00,1.9800,103.00,101.00,7.0000,711.000000]],
        "channel":"ex_group_market",
        "group":"usdt"
    },
    "info":"success"
}
```

<br/>

**市场深度**

订阅

``
   {"channel":"ex_depth_data","market":{Market},"event":"addChannel"}
``

退订

``
  {"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...

>响应数据
```js
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "depth":"0",
        "last":301.22,
        "asks":[[101.00,2.0000],[102.00,1.0000],[103.00,1.0000]],
        "bids":[[100.00,1.0000],[99.00,1.0000],[98.00,1.0000]],
        "channel":"ex_depth_data",
        "isFull":true
    },
    "info":"success"
}
```
``
    说明：用户订阅成功之后，会返回一次全量数据，并且在data里会有一个isFull为true的字段做为标识，之后, 一旦有更新将以增量方式返回。增量数据每个价格档位都是最新的数据，如果数量为0表示这个价格档位已经被成交或取消。
``

<br/>

**市场最新成交**

订阅

``
   {"channel":"ex_last_trade","market":{Market},"since":0,"event":"addChannel"}
``

退订

``
  {"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}
``

>请求参数

参数 | 数据类型 | 是否必须 | 默认值 | 描述 | 取值范围  
-|-|-|-|-|-
market | string | true | N/A | 交易市场 | btc_usdt, eth_usdt...
since | integer | true | 0 | 时间条件 | 0或需要的时间节点的时间戳，13位毫秒级

>响应数据
```js
// [时间戳，成交价，成交数量，交易类型，记录ID]
{
    "code":200,
    "data":{
        "market":"eth_usdt",
        "records":[[1561697199380,301.22,0.1407,"bid",156169718700197],[1561697198572,301.18,4.0000,"bid",156169718600146],[1561697198302,301.18,0.9883,"ask",156169718400145]],
        "channel":"ex_last_trade",
        "isFull":true
    },
    "info":"success"
}
```
``
    说明：用户订阅成功之后，会返回一次根据since过滤的全量数据，并且在data里有一个isFull为true的字段做为标识，之后, 一旦有更新，Websocket客户端将收到服务器推送的增量消息。
``
