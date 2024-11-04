import base64
import hashlib
import hmac


def calculate_signature(timestamp: str, secret: str) -> str:
    # 计算签名字符串：timestamp + "\n" + 密钥
    to_sign = f'{timestamp}\n{secret}'
    hmac_code = hmac.new(to_sign.encode('utf-8'), digestmod=hashlib.sha256).digest()
    # 对结果进行base64处理
    return base64.b64encode(hmac_code).decode('utf-8')
