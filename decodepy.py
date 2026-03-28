import base64
import json

def b64url_decode_to_bytes(s: str) -> bytes:
    # 兼容 Base64URL / Base64：先把 URL-safe 字符替换回标准 Base64
    s = s.strip().replace("-", "+").replace("_", "/")

    # 补齐 padding（Base64 长度必须是 4 的倍数）
    s += "=" * ((4 - len(s) % 4) % 4)

    return base64.b64decode(s)

def decode_single_segment_token(token: str):
    raw = b64url_decode_to_bytes(token)

    # 有的接口直接把 JSON bytes base64 了；也有的会 gzip/deflate（这里先按 utf-8 尝试）
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        # 如果不是 utf-8，可先打印原始 bytes 看看
        raise ValueError(f"Decoded bytes are not UTF-8. First 50 bytes: {raw[:50]!r}")

    # 尝试按 JSON 解析
    try:
        obj = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Decoded text is not valid JSON: {e}\nDecoded text preview: {text[:200]}")

    return obj

if __name__ == "__main__":
    token = """"""


    data = decode_single_segment_token(token)
    print(json.dumps(data, ensure_ascii=False, indent=2))