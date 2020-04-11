package api.utils;


import java.io.UnsupportedEncodingException;

import org.apache.commons.codec.binary.Base64;

public class Base64CoderC {

    private static Base64 base64 = new Base64();

    public static String encode(String str){
        try {
            str = base64.encodeToString(str.getBytes("UTF-8"));
        } catch (UnsupportedEncodingException e) {
            //just ignore
        }
        return str;
    }

    public static String decode(String str){
        return new String(Base64.decodeBase64(str));
    }
    
}