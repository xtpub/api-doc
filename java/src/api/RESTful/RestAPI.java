package api.RESTful;

import java.util.HashMap;
import java.util.Map;

import org.junit.Test;

import com.alibaba.fastjson.JSONArray;
import com.alibaba.fastjson.JSONObject;

import api.utils.Base64CoderC;
import api.utils.HttpUtil;

public class RestAPI {

	/**
	 * zh 网站申请的密钥对
	 * en Key pair applied by the website
	 */
	private final static String accessKey = "";
	private final static String secretKey = "";
	
	private final static String URL = "https://api.xt.com";

	/**
	 * zh 交易市场配置
	 * en Trading market configuration
	 */
	@Test
	public void getMarketConfig() {
		String text = HttpUtil.get(URL + "/data/api/v1/getMarketConfig");
		System.out.println(text);
	}

	/**
	 * zh K线数据
	 * en K line data
	 */
	@Test
	public void getKLine() {
		String text = HttpUtil.get(URL + "/data/api/v1/getKLine?market=btc_usdt&type=1min&since=0");
		System.out.println(text);
	}

	/**
	 * zh 聚合行情（Ticker）
	 * en Aggregate Quotes (Ticker)
	 */
	@Test
	public void getTicker() {
		String text = HttpUtil.get(URL + "/data/api/v1/getTicker?market=btc_usdt");
		System.out.println(text);
	}

	/**
	 * zh 所有市场的最新行情
	 * en The latest quotes in all markets
	 */
	@Test
	public void getTickers() {
		String text = HttpUtil.get(URL + "/data/api/v1/getTickers");
		System.out.println(text);
	}
	
	/**
	 * zh 市场深度数据
	 * en Market Depth Data
	 */
	@Test
	public void getDepth() {
		String text = HttpUtil.get(URL + "/data/api/v1/getDepth?market=btc_usdt");
		System.out.println(text);
	}
	
	/**
	 * zh 最近市场成交记录
	 * en Recent market transaction records
	 */
	@Test
	public void getTrades() {
		String text = HttpUtil.get(URL + "/data/api/v1/getTrades?market=btc_usdt");
		System.out.println(text);
	}
	
	/**
	 * zh 获取交易账户资产
	 * en Get trading account assets
	 */
	@Test
	public void getBalance() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		
		String text = HttpUtil.get(URL + "/trade/api/v1/getBalance", map);
		System.out.println(text);
	}

	/**
	 * zh 获取账户类型
	 * en Get account type
	 */
	@Test
	public void getAccounts() {
		String text = HttpUtil.get(URL + "/trade/api/v1/getAccounts");
		System.out.println(text);
	}

	/**
	 * zh 获取指定账户资金
	 * en Get funds in a designated account
	 */
	@Test
	public void getFunds() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("account", 2);	// 现货账户(en:Spot account)
		map.put("nonce", System.currentTimeMillis());
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		String text = HttpUtil.get(URL + "/trade/api/v1/getFunds", map);
		System.out.println(text);
	}

	/**
	 * zh 转账
	 * en Transfer
	 */
	@Test
	public void transfer() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("from", 1);
		map.put("to", 2);
		map.put("amount", 0.1);
		map.put("coin", "btc");
		map.put("safePwd", "123456");
		map.put("nonce", System.currentTimeMillis());
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		String text = HttpUtil.post(URL + "/trade/api/v1/transfer", map);
		System.out.println(text);
	}

	/**
	 * zh 委托
	 * en Entrust
	 */
	@Test
	public void order() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		map.put("price", "10000");
		map.put("number", "1.23");
		map.put("type", 1);		// 0.sell 1.buy
		map.put("entrustType", 0);	// 0.Limited price  1.Market price matching
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		// 
		String text = HttpUtil.post(URL + "/trade/api/v1/order", map);
		System.out.println(text);
	}
	
	// 批量委托

	/**
	 * zh 批量委托
	 * en Batch Entrust
	 */
	@Test
	public void batchOrder() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		
		JSONArray array = new JSONArray();
		for(int i = 0; i < 10; i++) {
			JSONObject bid = new JSONObject();
			bid.put("price", "10000.123");
			bid.put("amount", "0.1");
			bid.put("type", 1);
			array.add(bid);
			JSONObject ask = new JSONObject();
			ask.put("price", "10001.123");
			ask.put("amount", "0.1");
			ask.put("type", 0);
			array.add(ask);
		}
		// put data
		String data = Base64CoderC.encode(array.toJSONString());
		
		map.put("data", data);
		
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		// 
		String text = HttpUtil.post(URL + "/trade/api/v1/batchOrder", map);
		System.out.println(text);
	}

	/**
	 * zh 撤单
	 * en Cancel an order
	 */
	@Test
	public void cancel() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		map.put("id", "156387346384491");
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		
		String text = HttpUtil.post(URL + "/trade/api/v1/cancel", map);
		System.out.println(text);
	}
	
	/**
	 * zh 批量撤单
	 * en Batch cancellation
	 */
	@Test
	public void batchCancel() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		
		JSONArray array = new JSONArray();
		array.add("157154392122493");
		array.add("157154392122494");
		array.add("157154392122495");
		array.add("157154392122496");
		array.add("157154392122497");
		
		// put data
		String data = Base64CoderC.encode(array.toJSONString());
		
		map.put("data", data);
		
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		// 
		String text = HttpUtil.post(URL + "/trade/api/v1/batchCancel", map);
		System.out.println(text);
	}
	
	/**
	 * zh 获取订单
	 * en Get order
	 */
	@Test
	public void getOrder() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		map.put("id", "156387346384491");
		// 签名 (en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		
		String text = HttpUtil.get(URL + "/trade/api/v1/getOrder", map);
		System.out.println(text);
	}

	/**
	 * zh 获取未完成的订单
	 * en Get outstanding orders
	 */
	@Test
	public void getOpenOrders() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		map.put("page", 1);
		map.put("pageSize", 10);
		
		// 签名 (en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		
		String text = HttpUtil.get(URL + "/trade/api/v1/getOpenOrders", map);
		System.out.println(text);
	}
	
	/**
	 * zh 批量获取订单
	 * en Get orders in bulk
	 */
	@Test
	public void getBatchOrders() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("market", "btc_usdt");
		
		JSONArray array = new JSONArray();
		array.add("157154392122493");
		array.add("157154392122494");
		array.add("157154392122495");
		array.add("157154392122496");
		array.add("157154392122497");
		
		// put data
		String data = Base64CoderC.encode(array.toJSONString());
		
		map.put("data", data);
		// 签名 (en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		
		String text = HttpUtil.get(URL + "/trade/api/v1/getBatchOrders", map);
		System.out.println(text);
	}

	/**
	 * zh 获取充值记录
	 * en Get recharge record
	 */
    @Test
    public void getPayInRecord() {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("accesskey", accessKey);
        map.put("nonce", System.currentTimeMillis());
        map.put("coin", "eth");
        map.put("page", 1);
        map.put("pageSize", 10);

        // 签名(en:Signature)
        String signature = HttpUtil.getSignature(map, secretKey);
        map.put("signature", signature);

        String text = HttpUtil.get(URL + "/trade/api/v1/getPayInRecord", map);
        System.out.println(text);
    }

	/**
	 * zh 获取提现记录
	 * en Get withdrawal record
	 */
    @Test
    public void getPayOutRecord() {
        Map<String, Object> map = new HashMap<String, Object>();
        map.put("accesskey", accessKey);
        map.put("nonce", System.currentTimeMillis());
        map.put("coin", "eth");
        map.put("page", 1);
        map.put("pageSize", 10);
        // 签名(en:Signature)
        String signature = HttpUtil.getSignature(map, secretKey);
        map.put("signature", signature);

        String text = HttpUtil.get(URL + "/trade/api/v1/getPayOutRecord", map);
        System.out.println(text);
    }

	/**
	 * zh 获取充值地址
	 * en Get recharge Address
	 */
	@Test
	public void getPayInAddress() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("coin", "eth");
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);

		String text = HttpUtil.get(URL + "/trade/api/v1/getPayInAddress", map);
		System.out.println(text);
	}

	/**
	 * zh 获取提现地址
	 * en Get withdrawal address
	 */
	@Test
	public void getPayOutAddress() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("coin", "eth");
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		String text = HttpUtil.get(URL + "/trade/api/v1/getPayOutAddress", map);
		System.out.println(text);
	}

	/**
	 * zh 提现
	 * en Withdraw
	 */
	@Test
	public void withdraw() {
		Map<String, Object> map = new HashMap<String, Object>();
		map.put("accesskey", accessKey);
		map.put("nonce", System.currentTimeMillis());
		map.put("coin", "eth");
		map.put("safePwd", "");
		map.put("amount", "1");
		map.put("address", "");
		// 签名(en:Signature)
		String signature = HttpUtil.getSignature(map, secretKey);
		map.put("signature", signature);
		String text = HttpUtil.get(URL + "/trade/api/v1/withdraw", map);
		System.out.println(text);
	}
	
	// To be continued...
	
}
