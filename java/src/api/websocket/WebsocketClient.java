package api.websocket;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.util.zip.GZIPInputStream;

import org.apache.log4j.Logger;

import com.alibaba.fastjson.JSONObject;

import api.utils.ZipUtil;
import api.websocket.okhttp3.Okhttp3WebSocketClient;
import api.websocket.okhttp3.Okhttp3WebSocketHandle;
import okhttp3.Response;
import okhttp3.WebSocket;
import okio.ByteString;

public class WebsocketClient implements Okhttp3WebSocketHandle {

	private static Logger logger = Logger.getLogger(WebsocketClient.class);
	
	
	private String url;
	
	private Okhttp3WebSocketClient websocket;
	
	public WebsocketClient(String url) {
		this.url = url;
	}
	
	public boolean connect() {
		websocket = new Okhttp3WebSocketClient(url, this);
		return websocket.connect();
	}
	
	public boolean isAlive() {
		return websocket.isActive();
	}
	
	public boolean send(String str) {
		return websocket.send(str);
	}
	
	public void close() {
		websocket.close();
	}
	
	@Override
	public void onOpen(WebSocket webSocket, Response response) {
		// TODO Auto-generated method stub
		System.out.println("connected");
	}

	@Override
	public void onMessage(WebSocket webSocket, String message) {
		// TODO Auto-generated method stub
		System.out.println(message);
		websocket.setLatest(System.currentTimeMillis());
	}

	@Override
	public void onMessage(WebSocket webSocket, ByteString bytes) {
		// TODO Auto-generated method stub
		try {
			String text = ZipUtil.ungzip(bytes.toByteArray());
			System.out.println(text);
			if(text != null && text.startsWith("{")) {
				JSONObject data = JSONObject.parseObject(text);
				if(data.containsKey("ping")) {
					JSONObject pong = new JSONObject();
					pong.put("pong", data.getLongValue("ping"));
					System.out.println(pong.toJSONString());
					send(pong.toJSONString());
				}
			}
			websocket.setLatest(System.currentTimeMillis());
		}catch(Exception ex){
			ex.printStackTrace();
		}
	}

	@Override
	public void onClosed(WebSocket webSocket, int code, String reason) {
		// TODO Auto-generated method stub
		System.out.println("closed: " + reason);
	}

	@Override
	public void onFailure(WebSocket webSocket, Throwable t, Response response) {
		// TODO Auto-generated method stub
		System.out.println("error: " + t.getMessage());
	}
}
