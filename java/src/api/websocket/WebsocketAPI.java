package api.websocket;

import java.util.concurrent.TimeUnit;

import com.alibaba.fastjson.JSONObject;

public class WebsocketAPI {

	private static final String URL = "wss://ws.ubiex.co/websocket";
	
	private WebsocketClient wc;
	
	private boolean connect() {
		this.wc = new WebsocketClient(URL);
		return this.wc.connect();
	}
	
	public void send(String text) {
		this.wc.send(text);
	}
	
	public static void main(String[] args) {
		
		WebsocketAPI api = new WebsocketAPI();
		if(!api.connect()) {
			return;
		}
		
		// 订阅
		JSONObject subscribe = new JSONObject();
		subscribe.put("channel", "ex_depth_data");
		subscribe.put("market", "btc_usdt");
		subscribe.put("event", "addChannel");
		api.send(subscribe.toJSONString());
		
		try {
			TimeUnit.MILLISECONDS.sleep(60 * 1000);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		// 取消订阅
		JSONObject unsubscribe = new JSONObject();
		unsubscribe.put("channel", "ex_depth_data");
		unsubscribe.put("market", "btc_usdt");
		unsubscribe.put("event", "removeChannel");
		api.send(unsubscribe.toJSONString());
		
		// 关闭
		api.send("close");
	}
}
