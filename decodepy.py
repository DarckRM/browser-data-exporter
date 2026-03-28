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
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i-S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL-S4nOWMl-WFrOWPuC_ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJhdXRoT3JnSWRBbmRQcm92aWRlcklkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2fGVuZ2luZWVyIn0"""
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i-S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL-S4nOWMl-WFrOWPuC_ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJhdXRoT3JnSWRBbmRQcm92aWRlcklkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2fGVuZ2luZWVyIn0"""
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzQxMjMxMDU3NjcwMTQ0IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1MCIsIm9yZ1NpbXBsZU5hbWUiOiLlpKfov57kuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuWkp+i/nuS6i+S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL+S4nOWMl+WFrOWPuC/lpKfov57kuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJhdXRoT3JnSWRBbmRQcm92aWRlcklkIjoiNDY0MzQxMjMxMDU3NjcwMTQ0fGVuZ2luZWVyIn0="""
    token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i+S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL+S4nOWMl+WFrOWPuC/ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOnRydWUsImF1dGhIck9yZ0lkIjoiMTc1MzA2MjgiLCJhdXRoSHJPcmdQcm92aWRlcklkIjoid3V6aSIsImF1dGhPcmdJZEFuZFByb3ZpZGVySWQiOiI0NjQzMjIzODQ3OTU2OTMwNTZ8ZW5naW5lZXIifQ=="""

    data = decode_single_segment_token(token)
    print(json.dumps(data, ensure_ascii=False, indent=2))