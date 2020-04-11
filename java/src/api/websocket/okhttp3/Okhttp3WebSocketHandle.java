package api.websocket.okhttp3;

import okhttp3.Response;
import okhttp3.WebSocket;
import okio.ByteString;

public interface Okhttp3WebSocketHandle {

	public void onOpen(WebSocket webSocket, Response response);

	public void onMessage(WebSocket webSocket, String message);

	public void onMessage(WebSocket webSocket, ByteString bytes);

	public void onClosed(WebSocket webSocket, int code, String reason);

	public void onFailure(WebSocket webSocket, Throwable t, Response response);

}
