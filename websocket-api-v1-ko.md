## 액세스 설명

### WEBSOCKET API

```
형식적인:
wss://xtsocket.xt.com/websocket
```
```
아껴서 안 쓰다:
wss://xtsocket.xt.pub/websocket
```



<br/>

### 데이터 압축

WebSocket API의 모든 데이터를 GZIP에서 압축한 다음 Base64.encode () 인코딩을 하고 바이너리를 사용하여 되돌려줍니다. Client에서 바이너리 데이터를 수신한 후 디코딩 및 압축 해제해야 합니다.
<br/>

### 프롬프트 메시지


사용자의 클라이언트 Websocket이 XT Websocket 서버에 연결되면 서버는 주기적으로 사용자에게 ping 메시지(현재 5초로 설정됨)를 보내며, 이는 타임스탬프를 포함합니다.

이 프롬프트 메시지를 수신한 후, 사용자는 즉시 pong 메시지를 반환하고 동일한 타임스탬프를 다음 형식으로 작성해야 합니다.

```js
{"ping": 1562979600}

{"pong": 1562979600}
```

Websocket 서버가 3회 연속 'ping' 메시지를 보냈지만 "pong" 메시지를 수신하지 못한 경우, 서버는 자동으로 클라이언트와의 연결을 끊습니다.

물론 사용자는 서버에 접속한 후에도  "ping" 메시지를 서버에 보낼 수도 있으며, 서버는 ping 정보를 받으면 "pong" 메시지에 응답합니다.

<br/>

### 연결 해제

사용자는 스스로 연결을 끊거나 XT Websocket 서버에 "close" 메시지를 보낼 수 있습니다.

<br/>

### 주제 구독

Websocket 서버에 연결한 후 Websocket 클라이언트는 특정 주제를 구독하기 위해 다음 요청을 보내야 합니다.

```js

{"channel":"ex_single_market","market":{Market},"event":"addChannel"}

{"channel":"ex_group_market","group":{Group},"event":"addChannel"}

{"channel":"ex_last_trade","market":{Market},"since":{Since},"event":"addChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"addChannel"}

{"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}


```


주제를 구독한 후 Websocket 클라이언트는 해당 주제에서 모든 데이터 흐름을 수신합니다.

다음으로 구독된 주제가 업데이트되면 Websocket 클라이언트는 서버에서 업데이트 메시지(push)를 수신합니다:

<br/>

### 구독취소

구독 취소 형식은 다음과 같습니다:

```js
{"channel":"ex_single_market","market":{Market},"event":"removeChannel"}

{"channel":"ex_group_market","group":{Group},"event":"removeChannel"}

{"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}

{"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}

{"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}

```


<br/>


**K라인 데이터**

구독

``
{"channel":"ex_chart_update","market":{Market},"since":{Since},"interval":{Interval},"event":"addChannel"}
``

구독 취소

``
{"channel":"ex_chart_update","market":{Market},"interval":{Interval},"event":"removeChannel"}
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
market | string | true | N/A | 거래 마켓 | btc_usdt, eth_usdt...
interval | string | true | N/A | K라인 유형 | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | 시간 조건 | 0 또는 필수 타임스탬프, 10비트 밀리초 수준
>응답 데이터
```js
//[타임스탬프, 오픈가격, 최고가, 최저가, 종가, 거래량, 거래액 ]
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
설명: 사용자가 성공적으로 구독한 후 "since"로 필터링된 모든 데이터가 반환되고 data에 isFull이 true라는 필드가 표시되어 있으며, 이후 업데이트가 있으면 Websocket 클라이언트는 서버에서 보내는 추가 메시지를 받게 됩니다.``

<br/>

**시가 총액（Ticker）**

구독

``
{"channel":"ex_single_market","market":{Market},"event":"addChannel"}
``

구독 취소

``
{"channel":"ex_single_market","market":{Market},"event":"removeChannel"}
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위

-|-|-|-|-|-
market | string | true | N/A | 거래 시장 | btc_usdt, eth_usdt...

>응답 데이터
```js
// [마켓네임, 마켓그룹, 현재가격, 등락폭, 최고가, 최저가, 거래량, 거래액]
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

**그룹화된 애그리게이트 시장（Tickers）**

구독

``
{"channel":"ex_group_market","group":{Group},"event":"addChannel"}
``

구독 취소

``
{"channel":"ex_group_market","group":{Group},"event":"removeChannel"}
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위

-|-|-|-|-|-
group | string | false | all | 그룹 유형 | all 또는 거래구역(예: usdt)또는 거래페어(예: btc_usdt)

>응답 데이터
```js
// [마켓네임, 마켓그룹, 현재가격, 등락폭, 최고가, 최저가, 거래량, 거래액]
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

**시장깊이**

구독

``
{"channel":"ex_depth_data","market":{Market},"event":"addChannel"}
``

구독 취소

``
{"channel":"ex_depth_data","market":{Market},"event":"removeChannel"}
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
market | string | true | N/A | 거래 시장 | btc_usdt, eth_usdt...

>응답 데이터
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
설명: 사용자가 구독을 완료하면 모든 데이터가 한 번에 반환되고, data에 isFull이 true인 필드가 표시되며, 이후 업데이트가 있으면 증분 방식으로 되돌려줍니다. 증량 데이터는 각 가격대의 최신 데이터입니다. 만약 수량이 0이면 해당 가격대가 거래 또는 취소되었음을 의미합니다.
``

<br/>

**시장 최신 거래**

구독

``
{"channel":"ex_last_trade","market":{Market},"since":0,"event":"addChannel"}
``

구독 취소

``
{"channel":"ex_last_trade","market":{Market},"event":"removeChannel"}
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
market | string | true | N/A | 거래 시장 | btc_usdt, eth_usdt...
since | integer | true | 0 | 시간조건 | 0 또는 타임스탬프 필요, 13비트 밀리초 수준

>응답 데이터
```js
// [타임스탬프, 체결가, 거래수량, 거래 유형, 레코드 ID]
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
설명: 사용자는 구독이 완료되면 "since"로 필터링된 모든 데이터가 한 번에 반환되고, data에 isFull이 true인 필드가 표시되며, 이후 업데이트가 있으면 Websocket 클라이언트는 서버에서 전송되는 추가 메시지를 받게 됩니다.``
