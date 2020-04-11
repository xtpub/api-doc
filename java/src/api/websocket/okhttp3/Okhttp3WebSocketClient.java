package api.websocket.okhttp3;

import java.util.concurrent.TimeUnit;

import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;
import okhttp3.WebSocket;
import okhttp3.WebSocketListener;
import okio.ByteString;

public class Okhttp3WebSocketClient extends WebSocketListener {

	private WebSocket webSocket;
	
	private Request request;
	
	private Okhttp3WebSocketHandle handle;
	
	private String url;
	
	
	public Okhttp3WebSocketClient(String url, Okhttp3WebSocketHandle handle) {
		this.url = url;
		this.handle = handle;
	}
	
	public boolean connect() {
		try {
			OkHttpClient client = new OkHttpClient.Builder().readTimeout(0, TimeUnit.MILLISECONDS).build();
			request = new Request.Builder().url(url).build();
			client.newWebSocket(request, this);
			client.dispatcher().executorService().shutdown(); 
			this.latest = System.currentTimeMillis();
			int i = 0;
			do {
				if (i >= 30) break;
				if (webSocket != null) break;
				TimeUnit.MILLISECONDS.sleep(1000);
				i++;
			} while (webSocket == null);
			return true;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return false;
	}

	@Override
	public void onOpen(WebSocket webSocket, Response response) {
		this.webSocket = webSocket;
		handle.onOpen(webSocket, response);
	}

	@Override
	public void onMessage(WebSocket webSocket, String message) {
		handle.onMessage(webSocket, message);
	}

	@Override
	public void onMessage(WebSocket webSocket, ByteString bytes) {
		handle.onMessage(webSocket, bytes);
	}

	@Override
	public void onClosed(WebSocket webSocket, int code, String reason) {
       handle.onClosed(webSocket, code, reason);
    }

	@Override
	public void onFailure(WebSocket webSocket, Throwable t, Response response) {
		handle.onFailure(webSocket, t, response);
	}

	public boolean send(String s) {
		return this.webSocket.send(s);
	}

	public void close() {
		if (this.webSocket != null) {
			this.webSocket.close(200, "close");
		}
	}
	
	private long latest;
	
	public long getLatest() {
		return latest;
	}

	public void setLatest(long latest) {
		this.latest = latest;
	}

	public boolean isActive() {
		if(System.currentTimeMillis() - latest > 3 * 60 * 1000) {
			return false;
		}
		return true;
	}
}
