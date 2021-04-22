import os.path

from flask import Flask
import ssl
import base64

app = Flask(__name__)


@app.route('/')
def index():
    return "Hello World"


if __name__ == '__main__':
    path = os.path.dirname(os.path.realpath(__file__))
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.load_cert_chain(path + "cert.crt", path + "key.key", "mypassword")
    # 私钥加密：openssl rsa -in ssl_key_.key -aes256 -passout pass:mypassword -out ssl_encryted.key
    # context.load_cert_chain(path + "cert.pem", path + "key.pem", base64.b64decode("密码"))
    app.run(host="0.0.0.0", port=9999, debug=True, ssl_context=context)
