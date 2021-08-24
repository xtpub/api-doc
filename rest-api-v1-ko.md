## 액세스 설명

### REST API

```
형식적인:
https://api.xt.com
```
```
아껴서 안 쓰다:
https://api.xt.pub
```

### 인터페이스의 기본 정보

대기 시간이 길고 안정성이 낮기 때문에 프록시를 통해 XT API에 액세스하는 것은 권장하지 않습니다.

GET 요청 매개변수는 query Params에, POST 요청 매개변수는 request body에 넣습니다. 매개변수를 query Params와 request body에 동시에 넣지 마십시오.

요청 헤더 정보는 다음과 같이 설정해주세요：`Content-Type=application/x-www-form-urlencoded`

인터페이스 자체에 필요한 매개변수 외에도 서명 매개변수인 query Params 또는 request body에 signature이 전달되어야 합니다. 서명 매개변수를 전달할 필요가 없는 인터페이스에 대해서는 추가로 설명됩니다.

<br/>  

### 주파수 제한 규칙

자산 획득은 초당 3회, 기타 방법은 단일 사용자당 초당 10회, 단일 IP당 분당 1000회, 요청된 시간을 초과하면 계정이 10분 동안 잠깁니다.


<br/>

### Signature 설명


API 요청은 internet을 통한 전송 과정에서 변경될 가능성이 있습니다. 요청이 변경되지 않았는지 확인하기 위해서 퍼블릭 인터페이스(기본 정보, 시세 데이터)를 제외한 모든 개인 인터페이스는 전송 중에 변경되었는지 확인하려면 API Key를 사용해야 합니다.각 API Key는 적절한 권한이 있어야만 해당 인터페이스에 접근할 수 있습니다. 새로 생성된 모든 API Key에 권한을 할당해야 합니다. 권한 형식에는 읽기, 거래, 출금이 있습니다. 인터페이스를 사용하기 전에 각 인터페이스의 권한 유형을 확인하고 API Key에 해당 권한이 있는지 확인하십시오.


합법적인 요청은 다음과 같이 구성됩니다:

주소 요청 방법: 즉, 서버 주소 `api.xt.com`을 방문합니다. 예를 들면 `api.xt.com/trade/api/v1/order`.

API 방문 비밀키（accesskey）：신청하신 API Key에 Access Key가 있습니다

타임스탬프(nonce): 애플리케이션에서 요청한 타임스탬프, 13비트 밀리초입니다. XT는 이 타임스탬프를 기반으로 API 요청의 유효성을 확인합니다.

서명(signature): 서명이 유효하고 변조되지 않았는지 확인하기 위해 서명에 의해 계산된 값입니다. XT는 HmacSHA256을 사용합니다.

<br/>

### 서명 절차

서명 계산 요청을 표준화합니다. 서명 계산에 HMAC를 사용하면 다른 내용을 사용한 계산 결과가 완전히 달라집니다. 따라서 서명 계산을 수행하기 전에 요청을 표준화하십시오. 다음은 주문내역 조회요청을 예로 들어 설명하겠습니다.

`https://api.xt.com/trade/api/v1/getOrder?accesskey={AccessKey}&market={Market}&nonce={Timestamp}&id={OrderId}&signature={Signature}`

ASCII 코드의 순서에 따라 매개변수 이름을 정렬하고 각 매개변수를 "&" 문자로 연결합니다. 아래는 정렬 후 결과입니다:

`accesskey=myAccessKey&id=123&market=btc_usdt&nonce=1562919832183`

주의할 점: nonce 값은 13비트 밀리초입니다.

웹 사이트를 통해 신청받은 Secret Key를 사용하여 위에서 생성한 HmacSHA256 매개변수 문자열에 서명합니다. 위의 작업을 통해 얻은 결과:

`97b7b71741ca0aec6e0404a5b1c7cb2a78e7bd6c2a8088dbd84a20129dee4fe7`

마지막으로 서명은 매개변수 이름 signature에 할당되고 서버에 제출됩니다.

<br/>

### API Key 신청 절차

1. 공식 웹사이트를 방문하여 계정에 로그인합니다<br/>
2. 우측 계정을 클릭 한 후 API 관리를 선택하여 API Key 신청 페이지로 이동합니다<br/>
3. 비고, 화이트리스트, API 접근 권한, 보안 비밀번호, 동적 인증코드를 입력하여 AccessKey와 SecretKey를 생성합니다<br/>

### 반환 형식

모든 인터페이스의 반환은 JSON 형식입니다.

<br/>

### 에러 코드

상태 코드 | 오류 정보
-|:-
101 | 주문 실패, 알 수 없는 주문 유형
102 | 주문 실패, 매개변수 오류
103 | 주문 실패, 자금 부족
104 | 주문 실패, 잠시후에 다시 시도해 주세요
105 | 주문 실패, 주문수량은 시스템에서 설정한 최소 주문 수보다 작을 수 없습니다
106 | 주문 실패, 빈번한 주문 작업입니다
107 | 작업 실패, 거래 오픈 전입니다
108 | 주문 실패, 잘못된 촉발 가격입니다
109 | 주문 실패, 시장 가격 주문이 지원되지 않습니다
110 | 주문 실패, 손익 중단(stop-limited) 주문이 지원되지 않습니다
111 | 주문 실패, 시스템이 설정한 보호 가격 초과
121 | 주문 철회 실패, 주문이 존재하지 않거나 취소되었습니다
122 | 주문철회 실패, 주문 취소 또는 완료됨
123 | 주문 철회에 실패했습니다. 알 수 없는 오류입니다. 나중에 다시 시도해 주세요
124 | 주문 철회 실패, 빈번한 작업입니다
200 | 성공
307 | AccessKey 오류
308 | 서명 오류
400 | 요청 오류, 매개변수 표준화 여부 확인
404 | 기타 오류 알림

<br/>

### 시세 데이터(서명 필요 없음)

**거래 시장 구성**

``
GET /data/api/v1/getMarketConfig
``

>요청 매개변수

`None`

>응답 데이터
```js
{
  "ltc_usdt": {
    "minAmount": 0.00010,       // 최소 주문 수량
    "minMoney": 5,       	// 최소 주문 금액 
    "pricePoint": 2,            // 가격 소수점
    "coinPoint": 4,             // 숫자 소수점
    "maker": 0.00100000,        // 메이커 거래 수수료
    "taker": 0.00100000         // 테이커 거래 수수료
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
  ...
}
```

<br/>

**K라인 데이터**

``
GET /data/api/v1/getKLine
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
market | string | true | N/A | 거래 시장 | btc_usdt, eth_usdt...
type | string | true | N/A | K라인 유형 | 1min,5min,15min,30min,1hour,6hour,1day,7day,30day
since | integer | true | 0 | 시간 조건. 제어 증분 | 첫 번째는 0이고, 이후는 since의 값을 따릅니다.

>응답 데이터
```js
{
  "datas": [
    [
      1562923200,       //타임스탬프
      11634.64,         //오픈가격
      11637.22,         //최고가
      11627.58,         //최저가
      11631.43,         //종가
      1.144578,         //거래량
      13314.16264138    //거래액
    ]
  ],
  "since": 1562923200
}
```

<br/>

**시가 총액（Ticker）**

``
GET /data/api/v1/getTicker
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위   
-|-|-|-|-|-
market | string | true | N/A | 거래시장 | btc_usdt, eth_usdt...

>응답 데이터
```js
{
  "high": 11776.93,			// 24h 최고 	
  "low": 11012.17,			// 24h 최저 
  "rate": 1.3900,                       // 24h 등락폭 
  "price": 11609.92,                    // 최신 체결가 
  "ask": 11618.25,		    	// 첫 매도 주문
  "bid": 11604.08,		    	// 첫 매입 주문 
  "coinVol": 2944.208780,            	//거래량
  "moneyVol": 33765013.61761934    	//거래액
}
```

<br/>

**전체 시장의 최신 Ticker**

``
GET /data/api/v1/getTickers
``

>요청 매개변수

`None`

>응답 데이터
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
  ...
}
```

<br/>

**시장깊이 데이터**

``
GET /data/api/v1/getDepth
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위  
-|-|-|-|-|-
market | string | true | N/A | 거래 시장 | btc_usdt, eth_usdt...

>응답 데이터
```js
{
  "last": 11591.26,     //최신 체결가 
  "asks": [             //판매자 
    [
      11594.80,         //거래액
      0.049472          //거래량 
    ],
    [
      11594.86,
      0.048462
    ]
  ],
  "bids": [             //구매자 
       [
         11590.06,      //거래액 
         0.188749       //거래량 
       ],
       [
         11588.42,
         0.030403
       ]
   ]
}
```

<br/>

**최신 시장 거래 기록**

``
GET /data/api/v1/getTrades
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위  
-|-|-|-|-|-
market | string | true | N/A | 거래 시장 | btc_usdt, eth_usdt...

>응답 데이터
```js
[
  [
    1562924059762,      //타임스탬프
    11613.18,           //체결가
    0.044448,           //거래수량
    "bid",              //거래 유형 [bid: 매입 ask: 매도]
    156292405956105     //레코드 ID
  ],
  [
    1562924059006,
    11613.22,
    0.000086,
    "ask",
    156292405956104
  ]
  ...
]
```

<br/>
<br/>

### 거래 API

**서버 시간 가져오기(서명 필요 없음)**

``
GET /trade/api/v1/getServerTime
``

>요청 매개변수

`None`

>응답 데이터
```js
{
  "code": 200,
  "data": {
      "serverTime": 1562924059006 //밀리초 타임스탬프
  },
  "info": "success"
}
```
<br/>

**거래(현물) 계정 자산 가져오기**

``
GET /trade/api/v1/getBalance
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위  
-|-|-|-|-|-
accesskey | string | true | N/A | Access private key |
nonce | integer | true | N/A | 13-bit milliseconds |

>응답 데이터
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // 동결 
      "available": "0.00"   // 사용가능 
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
    ...
  },
  "info": "success"
}
```

<br/>

**계정 유형 가져오기(서명 필요 없음)**

``
GET /trade/api/v1/getAccounts
``

>요청 매개변수

`None`

>응답 데이터
```js
// 동적으로 획득하지 않고 프로그램에 직접 쓸 수 있는 고정 시스템 계정
{
  "code":200,
  "data":[
  	{"name":"월렛계정","id":1},
  	{"name":"거래계정","id":2},
  	{"name":"법정화폐 계정","id":3},
        ...
  ],
  "info":"success"
}
```


<br/>

**특정 계정 자산 가져오기**

``
GET /trade/api/v1/getFunds
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위  
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
account | integer | true | N/A | 계정ID | getAccounts 인터페이스 참조
nonce | integer | true | N/A | 13비트 밀리초 |

>응답 데이터
```js
{
  "code": 200,
  "data": {
    "btc": {
      "freeze": "0.00",     // 동결 
      "available": "0.00"   // 사용가능 
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
    ...
  },
  "info": "success"
}
```

<br/>

**새 주문하기**

``
POST /trade/api/v1/order
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위  
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
nonce | integer | true | N/A | 13비트 밀리초 |
market | string | true | N/A | 거래 시장 | btc_usdt, eth_usdt...
price | float | true | N/A | 주문 가격 |
number | float | true | N/A | 주문 수량 |
type | integer | true | N/A | 거래유형 | 1、매입 0、매도
entrustType | integer | true | N/A | 주문 유형 | 0、지정가，1、시가

>응답 데이터
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

**대량 주문**

``
POST /trade/api/v1/batchOrder
``

>요청 매개변수


매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
nonce | integer | true | N/A | 13비트 밀리초 |
market | string | true | N/A | 거래시장 | btc_usdt, eth_usdt...
data | string | true | N/A | 주문데이터 |

```
지정가 주문만 지원됩니다. 하나의 트랜잭션이 성공하거나 실패합니다.

data는 JSON 배열입니다. 배열의 최대 길이는 100입니다. 100을 초과하면 100개를 초과한 부분의 요소가 무시됩니다. 배열 요소의 형식은 다음과 같습니다.

{
  "price": 1000,  //주문가격 
  "amount": 1,    //주문수량 
  "type" : 1    // 1、매입 0、매도
}

어셈블리가 완료되면 JSON 배열이 STRING으로 변환되고, Base64.encode()를 진행하여야 만이 제출될 최종 데이터입니다. 

주의할 점, data는 JSON 데이터 자체에 서명하는 것과 관련이 없으며, 이는 Base64.decode() 이후에 STRING입니다.
```

>응답 데이터
```js
{
  "code": 200,
  "data": [
    {
      "amount": 0.0010,         //주문수량
      "price": 5000.0000,       //주문가격 
      "id": 156292972664756,
      "type": 1                 // 1、매입 0、매도 
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

**주문취소**

``
POST /trade/api/v1/cancel
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
nonce | integer | true | N/A | 13비트 밀리초 수준 |
market | string | true | N/A | 거래시장 | btc_usdt, eth_usdt...
id | integer | true | N/A | 주문ID |

>응답 데이터
```js
{
  "code": 200,
  "info": "The order has been canceled successfully"
}
```

<br/>

**대량 주문 취소**

``
POST /trade/api/v1/batchCancel
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
nonce | integer | true | N/A | 13비트 밀리초 수준 |
market | string | true | N/A | 거래시장 | btc_usdt, eth_usdt...
data | string | true | N/A | 주문 데이터 |

```
data는 JSON 배열입니다. 배열의 최대 길이는 100입니다. 100을 초과하면 100개를 초과한 부분의 요소가 무시됩니다. 배열 요소의 형식은 주문ID입니다. 예를 들면: 

[123, 456, 789]

어셈블리가 완료되면 JSON 배열이 STRING으로 변환되고, Base64.encode()를 진행하여야 만이 제출될 최종 데이터입니다. 

주의할 점, data는 JSON 데이터 자체에 서명하는 것과 관련이 없으며, 이는 Base64.decode() 이후에 STRING입니다.
```

>응답 데이터
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

**주문 정보**

``
GET /trade/api/v1/getOrder
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
nonce | integer | true | N/A | 13비트 밀리초 수준 |
market | string | true | N/A | 거래시장 | btc_usdt, eth_usdt...
id | integer | true | N/A | 주문ID |

>응답 데이터
```js
{
  "code": 200,
  "data": {
    "number": "0.002000",           // 주문수량
    "price": "5000.00",             // 주문가격
    "avgPrice": "0.00",             // 거래 평균 가격
    "id": 156293034776987,          // 주문ID
    "time": 1562930348000,          // 주문시간 
    "type": 1,                      // 거래유형：1、매입 0、매도
    "status": 3,                    // 상태  (0, 제출 미매칭 1, 미거래분 또는 부분거래 2, 완료됨 3, 취소됨 4, 매칭 완료 결제 중)
    "completeNumber": "0.000000",   // 완성수량 
    "completeMoney": "0.000000",    // 완성금액 
    "entrustType": 0,               // 주문유형：1、시가 0、지정가
    "fee": "0.000000"               // 거래수수료  
  },
  "info": "success"
}
```

<br/>

**미완료 주문 가져오기**

``
GET /trade/api/v1/getOpenOrders
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위  
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
nonce | integer | true | N/A | 13비트 밀리초 수준 |
market | string | true | N/A | 거래시장 | btc_usdt, eth_usdt...
page | integer | false | 1 | 페이지 번호 |
pageSize | integer | false | 10 | 주문수량 | [10-1000]

>응답 데이터
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

**더 많은 주문 정보 가져오기**

``
GET /trade/api/v1/getBatchOrders
``

>요청 매개변수

매개변수 | 데이터 유형 | 필수 여부 | 기본값 | 설명 | 범위  
-|-|-|-|-|-
accesskey | string | true | N/A | 개인 키에 액세스 |
nonce | integer | true | N/A | 13비트 밀리초 수준 |
market | string | true | N/A | 거래시장 | btc_usdt, eth_usdt...
data | string | true | N/A | 주문 데이터 |

```
data는 JSON 배열입니다. 배열의 최대 길이는 100입니다. 100을 초과하면 100개를 초과한 부분의 요소가 무시됩니다. 배열 요소의 형식은 주문ID입니다. 예를 들면: 


[123, 456, 789]

어셈블리가 완료되면 JSON 배열이 STRING으로 변환되고, Base64.encode()를 진행하여야 만이 제출될 최종 데이터입니다. 

주의할 점, data는 JSON 데이터 자체에 서명하는 것과 관련이 없으며, 이는 Base64.decode() 이후에 STRING입니다. 
```

>응답 데이터
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


