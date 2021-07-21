## README.md

Welcome to XT API! You can use this API to get market data, trade, and manage your account.
XT provides flexible APIs to help users integrate XT transaction quickly and efficiently into their applications.
XT supports both Rest API and WebSocket API.
It is recommended that developer use the Rest API when performing functions such as trading or withdrawal, and use the WebSocket API to obtain information such as market prices and trading depth.
<br/>

### Access Description

###WEBSOCKET API

```
Official:
wss://xtsocket.xt.com/websocket
```
```
Spare:
wss://xtsocket.xt.pub/websocket
```


### Data compression
All data of the WebSocket API is compressed by GZIP, then Base64.encode () is encoded and returned in binary mode, and the user needs to decode and decompress after receiving the binary data.
<br/>

### Prompt message

When the user's client Websocket connected to the XT Websocket server, the server will periodically send a ping message to user (currently set as 5 seconds) and include a timestamp.
After receiving this prompt message, the user should promptly return the pong message and include the same timestamp in the following format:

```js
{"ping": 1562979600}

{"pong": 1562979600}
```
If the Websocket server continuously sent ping messages for three times without receiving any “pong” messages, the server will automatically disconnect with the client.
However, after connecting to the server, the user can also send a message “ping” to the server. When the server received the information of ping , it will reply a “pong” message.



### Disconnect

The user may disconnect by themselves or send a “close” message to the XT Websocket server .



### Subscribe the topics


After connected with Websocket server, the Websocket client should send the following request to subscribe the specific topic:
```js
{"channel":"ex_single_market","market":{Market},"event":"addChannel"}

{"channel":"ex_group_market","group":{Group},"event":"addChannel"}

{"channel":"ex_last_trade","market":{Market},"since":{Since},"event":"addChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"addChannel"}

{"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}
```
After subscribed the topic, the Websocket client will receive all the data flow from the corresponding topic.
Next, once the subscribed topic is updated, the Websocket client will receive an update message “push” by the server:

<br/>

### Unsubscribe
The format of unsubscribing is as follows

```js
{"channel":"ex_single_market","market":{Market},"event":"removeChannel"}

{"channel":"ex_group_market","group":{Group},"event":"removeChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}

{"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}

{"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}
```

<br/>

**Kline/Candlestick status**
Subscribe

``
{"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}
``

Unsubscribe

``
{"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}
``

>Request parameter

Parameter | Data Type | True or false | Default value | Description | Ranges
-|-|-|-|-|-
market | string | true | N/A | Trading markets | btc_usdt, eth_usdt...
interval | string | true | N/A | Kline/candlestick type | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | Time condition | 0 or required timestamp, 10-bit seconds level

>Response data

```js
//[ Timestamp, Open price, Highest price, Lowest Price, Close price, Volume, Turnover]
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
Note: After the user has subscribed successfully , all data filtered by "since" will be returned, and there is a field with isFull as true in the data is an identifier. Once there is an update, the Websocket client will receive the incremental message send by the server.
``

<br/>

**Aggregate market**

Subscribe

``
{"channel":"ex_single_market","market":{Market},"event":"addChannel"}
``

Unsubscribe

``
{"channel":"ex_single_market","market":{Market},"event":"removeChannel"}
``

>Request Parameter

Parameter | Data Type | True or false | Default value | Description | Ranges
-|-|-|-|-|-
market | string | true | N/A | Trading markets | btc_usdt, eth_usdt...

>Response data
```js
// [Market name, Market Group, Market price, Price Fluctuation Limit, Highest Price, Lowest Price, Volume, Turnover]
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

**Grouped aggregate market**

Subscribe

``
    {"channel":"ex_group_market","group":{Group},"event":"addChannel"}
``

Unsubscribe

``
    {"channel":"ex_group_market","group":{Group},"event":"removeChannel"}
``

>Request Parameter

Parameter | Data Type | True or false | Default value | Description | Ranges
group | string | false | all | Group type | all or Trading area（eg：USDT）or trading pair(eg: BTC, USDT)

>Response data
```js
// [Market name, Market Group, Market price, Price Fluctuation Limit, Highest price, Lowest price, Volume, Turnover]
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

**Market Depth**

Subscribe

``
    {"channel":"ex_depth_data","market":{Market},"event":"addChannel"}
``

Unsubscribe

``
    {"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}
``

>Request Parameter

Parameter | Data Type | True or false | Default value | Description | Ranges
-|-|-|-|-|-
market | string | true | N/A | Trading markets | btc_usdt, eth_usdt...

>Response data
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
Note: After the user has subscribed successfully, all data will be returned at once, and there will be a field with isFull as true in the data as an identifier. Once there is an update, it will be returned incrementally. Incremental data of each price range is the latest data. If the quantity is 0, it means the price range has been traded or cancelled.
``
**Latest market transactions**

Subscribe

``
    {"channel":"ex_last_trade","market":{Market},"since":0,"event":"addChannel"}
``

Unsubscribe

``
    {"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}
``

>Request Parameter

Parameter | Data Type | True or false | Default value | Description | Ranges
-|-|-|-|-|-
market | string | true | N/A | Trading markets | btc_usdt, eth_usdt...
since | integer | true | 0 | Time Condition | 0 or required a timestamp, 13-bit milliseconds level

>Response data
```js
// [Timestamp, Strike Price, volume, transaction type, Record ID]
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
    Note: After the user has subscribed successfully , all data filtered by “since” will be returned at once, and there is a field with isFull as true in the data is an identifier. Once there is an update, the Websocket client will receive the incremental message send by the server.
``
