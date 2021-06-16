#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   AES_py_java.py    
@Contact :   china.xiaowei@163.com
@License :   (C)Copyright 2021-2024, wochonglai

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2021/6/10 21:57   wayne      cryptography-linux离线安装.0         None
'''
# https://blog.csdn.net/qq_39248703/article/details/100999523
# 参考2 https://blog.csdn.net/qq_28205153/article/details/55798628
import base64
from Crypto.Cipher import AES

# 此处16|24|32个字符 默认16
AES_KEY = "aesencryptiontst"
IV = "1234567890123456"

# Padding算法
BS = len(AES_KEY)
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1:])]


class AESEncrypt(object):
    def __init__(self):
        self.key = AES_KEY
        self.mode = AES.MODE_CBC

    # 加密函数
    def encrypt(self, text):
        cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        self.ciphertext = cryptor.encrypt(bytes(pad(text), encoding="utf8"))
        # AES加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题，使用base64编码
        return base64.b64encode(self.ciphertext)

    # 解密函数
    def decrypt(self, text):
        decode = base64.b64decode(text)
        cryptor = AES.new(self.key.encode("utf8"), self.mode, IV.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        return unpad(plain_text)


if __name__ == '__main__':
    aes_encrypt = AESEncrypt()
    # 加密文本
    aes_text = "aestest"
    encrypt = aes_encrypt.encrypt(aes_text)
    aes_encrypt = aes_encrypt.decrypt(encrypt)
    print("加密文本: ", aes_text)
    print("加密后: ", encrypt)
    print("解密后: ", aes_encrypt)



'''
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;
 
import javax.crypto.Cipher;
import javax.crypto.spec.IvParameterSpec;
import javax.crypto.spec.SecretKeySpec;
 
public class AesTest {
 
    /**
     * 加密用的Key 可以用26个字母和数字组成
     * 此处使用AES-128-CBC加密模式，key需要为16位。
     */
    private static String sKey = "aesencryptiontst";
    private static String ivParameter = "1234567890123456";
 
    // 加密
    public static String encrypt(String sSrc) throws Exception {
        Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
        byte[] raw = sKey.getBytes();
        SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
        IvParameterSpec iv = new IvParameterSpec(ivParameter.getBytes());//使用CBC模式，需要一个向量iv，可增加加密算法的强度
        cipher.init(Cipher.ENCRYPT_MODE, skeySpec, iv);
        byte[] encrypted = cipher.doFinal(sSrc.getBytes("utf-8"));
        return new BASE64Encoder().encode(encrypted);//此处使用BASE64做转码。
    }
 
    // 解密
    public static String decrypt(String sSrc) {
        try {
            byte[] raw = sKey.getBytes("ASCII");
            SecretKeySpec skeySpec = new SecretKeySpec(raw, "AES");
            Cipher cipher = Cipher.getInstance("AES/CBC/PKCS5Padding");
            IvParameterSpec iv = new IvParameterSpec(ivParameter.getBytes());
            cipher.init(Cipher.DECRYPT_MODE, skeySpec, iv);
            byte[] encrypted1 = new BASE64Decoder().decodeBuffer(sSrc);//先用base64解密
            byte[] original = cipher.doFinal(encrypted1);
            String originalString = new String(original, "utf-8");
            return originalString;
        } catch (Exception ex) {
            return null;
        }
    }
 
    public static void main(String[] args) {
        String aes_text = "aestest";
        try {
            String sec = encrypt(aes_text);
            System.out.println(sec);
            System.out.println(decrypt("CcOtM9WXv0N+Owh/xxedZJnuNUaTU7y3aUBESQLUvVM="));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
'''