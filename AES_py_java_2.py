'''
https://www.cnblogs.com/whm-blog/p/12808176.html
'''
import base64
import hashlib
from Crypto.Cipher import AES as _AES


class AES:

    def __init__(self, key: str):
        """Init aes object used by encrypt or decrypt.
        AES/ECB/PKCS5Padding  same as aes in java default.
        """

        self.aes = _AES.new(self.get_sha1prng_key(key), _AES.MODE_ECB)

    @staticmethod
    def get_sha1prng_key(key: str) -> bytes:
        """encrypt key with SHA1PRNG.
        same as java AES crypto key generator SHA1PRNG.
        SecureRandom secureRandom = SecureRandom.getInstance("SHA1PRNG" );
        secureRandom.setSeed(decryptKey.getBytes());
        keygen.init(128, secureRandom);
        :param string key: original key.
        :return bytes: encrypt key with SHA1PRNG, 128 bits or 16 long bytes.
        """

        signature: bytes = hashlib.sha1(key.encode()).digest()
        signature: bytes = hashlib.sha1(signature).digest()
        return signature[:16]

    @staticmethod
    def padding(s: str) -> str:
        """Padding PKCS5"""

        pad_num: int = 16 - len(s) % 16
        return s + pad_num * chr(pad_num)

    @staticmethod
    def unpadding(s):
        """Unpadding PKCS5"""

        padding_num: int = ord(s[-1])
        return s[: -padding_num]

    def encrypt_to_bytes(self, content_str):
        """From string encrypt to bytes ciphertext.
        """

        content_bytes = self.padding(content_str).encode()
        ciphertext_bytes = self.aes.encrypt(content_bytes)
        return ciphertext_bytes

    def encrypt_to_base64(self, content_str):
        """From string encrypt to base64 ciphertext.
        """

        ciphertext_bytes = self.encrypt_to_bytes(content_str)
        ciphertext_bs64 = base64.b64encode(ciphertext_bytes).decode()
        return ciphertext_bs64

    def decrypt_from_bytes(self, ciphertext_bytes):
        """From bytes ciphertext decrypt to string.
        """

        content_bytes = self.aes.decrypt(ciphertext_bytes)
        content_str = self.unpadding(content_bytes.decode())
        return content_str

    def decrypt_from_base64(self, ciphertext_bs64):
        """From base64 ciphertext decrypt to string.
        """

        ciphertext_bytes = base64.b64decode(ciphertext_bs64)
        content_str = self.decrypt_from_bytes(ciphertext_bytes)
        return content_str


def encrypt_to_bytes(content_str, encrypt_key: str):
    """From string encrypt to bytes ciphertext.
    """

    aes: AES = AES(encrypt_key)
    ciphertext_bytes = aes.encrypt_to_bytes(content_str)
    return ciphertext_bytes


def encrypt_to_base64(content_str, encrypt_key: str) -> str:
    """From string encrypt to base64 ciphertext.
    """

    aes: AES = AES(encrypt_key)
    ciphertext_bs64 = aes.encrypt_to_base64(content_str)
    return ciphertext_bs64


def decrypt_from_bytes(ciphertext_bytes, decrypt_key: str) -> str:
    """From bytes ciphertext decrypt to string.
    """

    aes: AES = AES(decrypt_key)
    content_str = aes.decrypt_from_bytes(ciphertext_bytes)
    return content_str


def decrypt_from_base64(ciphertext_bs64, decrypt_key: str) -> str:
    """From base64 ciphertext decrypt to string.
    """

    aes: AES = AES(decrypt_key)
    content_str = aes.decrypt_from_base64(ciphertext_bs64)
    return content_str


if __name__ == "__main__":
    key = "57bf1661-3aad-4786-89a2-e187b38966ea"
    ct = "uafBlgURdmIJtSSe5Li/V1mByS3XZrpjXL+F/FCJmmro1bczVkVuHBBGcIk+Msi6hRSdCyJGZ+ox\nRHEA/QL0WjNXqw0BhgXE6oWYe/d0o3w="
    ret = decrypt_from_base64(ct, key)
    print(ret)

# Java 版本
'''
/**
     * aes解密
     * @param
     * @param content  密文
     * @return
     */
    public static String AESDncode(String appkey, String content) {
        try {
            // 1.构造密钥生成器，指定为AES算法,不区分大小写
            KeyGenerator keygen = KeyGenerator.getInstance("AES");
            // 2.根据ecnodeRules规则初始化密钥生成器
            SecureRandom secureRandom = SecureRandom.getInstance("SHA1PRNG");
            secureRandom.setSeed(appkey.getBytes());
            // 生成一个128位的随机源,根据传入的字节数组
            keygen.init(128, secureRandom);
            // 3.产生原始对称密钥
            SecretKey original_key = keygen.generateKey();
            // 4.获得原始对称密钥的字节数组
            byte[] raw = original_key.getEncoded();
            // 5.根据字节数组生成AES密钥
            SecretKey key = new SecretKeySpec(raw, "AES");
            // 6.根据指定算法AES自成密码器
            Cipher cipher = Cipher.getInstance("AES");
            // 7.初始化密码器，第一个参数为加密(Encrypt_mode)或者解密(Decrypt_mode)操作，第二个参数为使用的KEY
            cipher.init(Cipher.DECRYPT_MODE, key);
            // 8.将加密并编码后的内容解码成字节数组
            byte[] byte_content = new BASE64Decoder().decodeBuffer(content);
            /*
             * 解密
             */
            byte[] byte_decode = cipher.doFinal(byte_content);
            String AES_decode = new String(byte_decode, "utf-8");
            return AES_decode;
        } catch (Exception e) {
            e.printStackTrace();
        }

        // 如果有错就返加nulll
        return null;
    }
'''