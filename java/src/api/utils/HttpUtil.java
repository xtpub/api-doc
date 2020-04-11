package api.utils;

import java.io.IOException;
import java.security.KeyManagementException;
import java.security.KeyStoreException;
import java.security.NoSuchAlgorithmException;
import java.security.cert.CertificateException;
import java.security.cert.X509Certificate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Enumeration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.net.ssl.SSLContext;
import javax.servlet.http.HttpServletRequest;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.config.RequestConfig;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ssl.SSLConnectionSocketFactory;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.ssl.SSLContextBuilder;
import org.apache.http.ssl.TrustStrategy;
import org.apache.http.util.EntityUtils;
import org.apache.log4j.Logger;

public class HttpUtil {

	private static final String DEFAULT_CHARSET = "UTF-8";
	private static Logger log = Logger.getLogger(HttpUtil.class.getName());
	private static final int CONNECT_TIME_OUT = 5000; // 设置连接超时
	private static final int SOCKET_TIME_OUT = 10000; // 设置读取超时

	public static String post(String url, Map<String, Object> params) {
		String result = null;
		CloseableHttpClient httpClient = HttpClientBuilder.create().build();
		HttpPost httpPost = new HttpPost(url);
		// 设置客户端请求的头参数getParams已经过时,现在用requestConfig对象替换
		httpPost.setConfig(getRequestConfig());
		try {
			httpPost.setHeader("User-Agent",
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36");
			httpPost.setHeader("Accept", "application/json, text/javascript, */*; q=0.01");
			httpPost.setHeader("Accept-Encoding", " deflate, sdch");
			httpPost.setHeader("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2");
			httpPost.setHeader("Content-Type", "application/x-www-form-urlencoded");
			if (params != null && !params.isEmpty()) {
				List<NameValuePair> urlParams = new ArrayList<NameValuePair>();
				for (String key : params.keySet()) {
					urlParams.add(new BasicNameValuePair(key, params.get(key).toString()));
				}
				UrlEncodedFormEntity entity = new UrlEncodedFormEntity(urlParams, DEFAULT_CHARSET);
				httpPost.setEntity(entity);
			}
			HttpResponse httpResponse = httpClient.execute(httpPost);
			HttpEntity httpEntity = httpResponse.getEntity();
			if (httpEntity != null) {
				// 按指定编码转换结果实体为String类型
				result = EntityUtils.toString(httpEntity, DEFAULT_CHARSET);
				EntityUtils.consume(httpEntity);
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (Exception e) {
			e.printStackTrace();
		} finally {
			try {
				httpClient.close();
				httpPost.releaseConnection();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		return result;
	}

	public static String get(String url, Map<String, Object> params) {
		return get(url + "?" + paramToUrl(params));
	}
	
	public static String get(String url) {
		String result = "";
		CloseableHttpClient httpClient = HttpClientBuilder.create().build();
		HttpGet httpGet = new HttpGet(url);
		try {
			// 设置客户端请求的头参数getParams已经过时,现在用requestConfig对象替换
			httpGet.setConfig(getRequestConfig());
			httpGet.setHeader("User-Agent",
					"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36");
			httpGet.setHeader("Accept", "application/json, text/javascript, */*; q=0.01");
			httpGet.setHeader("Accept-Encoding", " deflate, sdch");
			httpGet.setHeader("Accept-Language", "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2");
			httpGet.setHeader("Content-Type", "application/x-www-form-urlencoded");
			HttpResponse httpResponse = httpClient.execute(httpGet);
			HttpEntity httpEntity = httpResponse.getEntity();
			if (httpEntity != null) {
				// 按指定编码转换结果实体为String类型
				result = EntityUtils.toString(httpEntity, "UTF-8");
				EntityUtils.consume(httpEntity);
			}
		} catch (Exception e) {
			log.info("连接地址：" + url + "不可用！！！");
			e.printStackTrace();
		} finally {
			try {
				httpClient.close();
				httpGet.releaseConnection();
			} catch (IOException e) {
				e.printStackTrace();
			}

		}
		return result;
	}

	private static String paramToUrl(Map<String, Object> data) {
        Set<String> keySet = data.keySet();
        String[] keyArray = keySet.toArray(new String[keySet.size()]);
        Arrays.sort(keyArray);
        StringBuilder sb = new StringBuilder();
        for (String k : keyArray) {
            sb.append(k).append("=").append(data.get(k).toString().trim()).append("&");
        }
        return sb.toString();
    }
	
	public static String getSignature(final Map<String, Object> data, String secretKey) {
		try {
			Set<String> keySet = data.keySet();
			String[] keyArray = keySet.toArray(new String[keySet.size()]);
			Arrays.sort(keyArray);
			StringBuilder sb = new StringBuilder();
			for (String k : keyArray) {
				sb.append(k).append("=").append(data.get(k).toString().trim()).append("&");
			}
			if (sb.length() > 0) {
				sb.deleteCharAt(sb.length() - 1);
			}
			return EncryptUtil.hmacSha256(sb.toString(), secretKey);
		} catch (Exception e) {
			e.printStackTrace();
		}
		return null;
	}

	private static RequestConfig getRequestConfig() {
		return RequestConfig.custom().setSocketTimeout(SOCKET_TIME_OUT).setConnectTimeout(CONNECT_TIME_OUT).build();
	}

	public static CloseableHttpClient createSSLInsecureClient() {
		try {
			SSLContext sslContext = new SSLContextBuilder().loadTrustMaterial(null, new TrustStrategy() {
				// 默认信任所有证书
				public boolean isTrusted(X509Certificate[] arg0, String arg1) throws CertificateException {
					return true;
				}
			}).build();
			// AllowAllHostnameVerifier: 这种方式不对主机名进行验证，验证功能被关闭，是个空操作(域名验证)
			SSLConnectionSocketFactory sslcsf = new SSLConnectionSocketFactory(sslContext,
					SSLConnectionSocketFactory.ALLOW_ALL_HOSTNAME_VERIFIER);
			return HttpClients.custom().setSSLSocketFactory(sslcsf).build();
		} catch (KeyManagementException e) {
			e.printStackTrace();
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		} catch (KeyStoreException e) {
			e.printStackTrace();
		}
		// 如果创建失败，就创建一个默认的Http的连接
		return HttpClients.createDefault();
	}

	public static Map<String, Object> getRequstMap(HttpServletRequest request) {
		Map<String, Object> param = new HashMap<String, Object>();
		Enumeration<String> em = request.getParameterNames();
		while (em.hasMoreElements()) {
			String name = em.nextElement();
			// if("signature".equalsIgnoreCase(name)) continue;
			String value = request.getParameter(name);
			param.put(name, value);
		}
		return param;
	}
}

class SSLClient {
	public static CloseableHttpClient createSSLClientDefault() {
		try {
			SSLContext sslContext = new SSLContextBuilder().loadTrustMaterial(null, new TrustStrategy() {
				// 信任所有
				public boolean isTrusted(X509Certificate[] chain, String authType) throws CertificateException {
					return true;
				}
			}).build();
			SSLConnectionSocketFactory sslsf = new SSLConnectionSocketFactory(sslContext);
			return HttpClients.custom().setSSLSocketFactory(sslsf).build();
		} catch (KeyManagementException e) {
			e.printStackTrace();
		} catch (NoSuchAlgorithmException e) {
			e.printStackTrace();
		} catch (KeyStoreException e) {
			e.printStackTrace();
		}
		return HttpClients.createDefault();
	}
}
