from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Util.Padding import pad, unpad
from hashlib import md5
import base64
import os

iv = b'0102030405060708'
presetKey = b'0CoJUm6Qyw8W8jud'
linuxapiKey = b'rFgB&h#%2?^eDg:Q'
eapiKey = b'e82ckenh8dichen8'
publicKey = (
    '-----BEGIN PUBLIC KEY-----\n'
    'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgtQn2JZ34ZC28NWYpAUd98iZ37BUrX/aKzmFbt7clFSs6sXqHauqKWqdtLkF2KexO40H1YTX8z2lSgBBOAxLsvaklV8k4cBFK9snQXE9/DDaFt6Rr7iVZMldczhC0JNgTz+SHXT6CBHuX3e9SdB1Ua44oncaTWz7OBGLbCiK45wIDAQAB\n'
    '-----END PUBLIC KEY-----'
)
base62 = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def aes_encrypt(buffer, mode, key, iv_):
    if mode == 'aes-128-cbc':
        cipher = AES.new(key, AES.MODE_CBC, iv_)
    else:  # 'aes-128-ecb'
        cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(buffer, AES.block_size))

def aes_decrypt(cipher_buffer, mode, key, iv_):
    if mode == 'aes-128-cbc':
        cipher = AES.new(key, AES.MODE_CBC, iv_)
    else:  # 'aes-128-ecb'
        cipher = AES.new(key, AES.MODE_ECB)
    return unpad(cipher.decrypt(cipher_buffer), AES.block_size)

def rsa_encrypt(buffer, key):
    # 填充到128字节
    buffer = b'\x00' * (128 - len(buffer)) + buffer
    rsakey = RSA.importKey(key)
    cipher = PKCS1_v1_5.new(rsakey)
    return cipher.encrypt(buffer)

def weapi(obj):
    import json
    text = json.dumps(obj)
    secretKey = bytes([ord(base62[ord(os.urandom(1)) % 62]) for _ in range(16)])
    encText = aes_encrypt(aes_encrypt(text.encode(), 'aes-128-cbc', presetKey, iv), 'aes-128-cbc', secretKey, iv)
    params = base64.b64encode(encText).decode()
    encSecKey = rsa_encrypt(secretKey[::-1], publicKey).hex()
    return {
        'params': params,
        'encSecKey': encSecKey
    }

def linuxapi(obj):
    import json
    text = json.dumps(obj)
    eparams = aes_encrypt(text.encode(), 'aes-128-ecb', linuxapiKey, b'').hex().upper()
    return {'eparams': eparams}

def eapi(url, obj):
    import json
    text = json.dumps(obj) if isinstance(obj, dict) else obj
    message = f"nobody{url}use{text}md5forencrypt"
    digest = md5(message.encode()).hexdigest()
    data = f"{url}-36cd479b6b5-{text}-36cd479b6b5-{digest}"
    params = aes_encrypt(data.encode(), 'aes-128-ecb', eapiKey, b'').hex().upper()
    return {'params': params}

def eapi_decrypt(cipher_buffer):
    return aes_decrypt(cipher_buffer, 'aes-128-ecb', eapiKey, b'').decode()


