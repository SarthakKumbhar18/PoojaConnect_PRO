import time
import base64
import hmac
import hashlib
import struct
import json


def generate_zego_token(app_id, server_secret, user_id):
    version = 0x04
    nonce = int(time.time())
    expire = nonce + 3600  # 1 hour validity

    payload = {
        "app_id": app_id,
        "user_id": user_id,
        "nonce": nonce,
        "ctime": nonce,
        "expire": expire,
    }

    payload_str = json.dumps(payload, separators=(",", ":"))
    payload_bytes = payload_str.encode("utf-8")

    signature = hmac.new(
        server_secret.encode("utf-8"),
        payload_bytes,
        hashlib.sha256
    ).digest()

    token = struct.pack("!BII", version, app_id, len(payload_bytes))
    token += payload_bytes
    token += signature

    return base64.b64encode(token).decode("utf-8")