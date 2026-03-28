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

def compare_tokens(token1: str, token2: str):
    data1 = decode_single_segment_token(token1)
    data2 = decode_single_segment_token(token2)

    for key in data1.keys():
        if key not in data2:
            print(f"Key '{key}' is missing in token2")
        elif data1[key] != data2[key]:
            print(f"Value for key '{key}' differs: token1 has {data1[key]!r}, token2 has {data2[key]!r}")

    print("Token Good data:")
    print(json.dumps(data1, ensure_ascii=False, indent=2))
    print("\nToken Bad data:")
    print(json.dumps(data2, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i-S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL-S4nOWMl-WFrOWPuC_ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJhdXRoT3JnSWRBbmRQcm92aWRlcklkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2fGVuZ2luZWVyIn0"""
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i-S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL-S4nOWMl-WFrOWPuC_ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJhdXRoT3JnSWRBbmRQcm92aWRlcklkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2fGVuZ2luZWVyIn0"""
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzQxMjMxMDU3NjcwMTQ0IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1MCIsIm9yZ1NpbXBsZU5hbWUiOiLlpKfov57kuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuWkp+i/nuS6i+S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL+S4nOWMl+WFrOWPuC/lpKfov57kuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJhdXRoT3JnSWRBbmRQcm92aWRlcklkIjoiNDY0MzQxMjMxMDU3NjcwMTQ0fGVuZ2luZWVyIn0="""
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i+S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL+S4nOWMl+WFrOWPuC/ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOnRydWUsImF1dGhIck9yZ0lkIjoiMTc1MzA2MjgiLCJhdXRoSHJPcmdQcm92aWRlcklkIjoid3V6aSIsImF1dGhPcmdJZEFuZFByb3ZpZGVySWQiOiI0NjQzMjIzODQ3OTU2OTMwNTZ8ZW5naW5lZXIifQ=="""
    # token = """eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i-S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL-S4nOWMl-WFrOWPuC_ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJjb21wYW55SWQiOiJkODg0ZmI3OS0zOTJjLTQyYzUtYmExMy1lYWIzYmRiOTkzZWQiLCJjb21wYW55UGF0aCI6IjAwMDAxMDAwNDkwMDAyNyIsImNvbXBhbnlOYW1lIjoi5Lic5YyX5YWs5Y-4IiwiY29tcGFueUZ1bGxOYW1lIjoi5Lit6ZOB54mp6LWE6ZuG5Zui5Lic5YyX5pyJ6ZmQ5YWs5Y-4IiwiYXV0aE9yZ0lkQW5kUHJvdmlkZXJJZCI6IjQ2NDMyMjM4NDc5NTY5MzA1NnxlbmdpbmVlciJ9"""
    token_pars = 'eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i-S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL-S4nOWMl-WFrOWPuC_ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOnRydWUsImF1dGhIck9yZ0lkIjoiMTc1MzA2MjgiLCJhdXRoSHJPcmdQcm92aWRlcklkIjoid3V6aSIsImF1dGhPcmdJZEFuZFByb3ZpZGVySWQiOiI0NjQzMjIzODQ3OTU2OTMwNTZ8ZW5naW5lZXIiLCJjb21wYW55SWQiOiJkODg0ZmI3OS0zOTJjLTQyYzUtYmExMy1lYWIzYmRiOTkzZWQiLCJjb21wYW55UGF0aCI6IjAwMDAxMDAwNDkwMDAyNyIsImNvbXBhbnlOYW1lIjoi5Lic5YyX5YWs5Y-4IiwiY29tcGFueUZ1bGxOYW1lIjoi5Lit6ZOB54mp6LWE6ZuG5Zui5Lic5YyX5pyJ6ZmQ5YWs5Y-4In0'
    token_good = 'eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i+S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL+S4nOWMl+WFrOWPuC/ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOnRydWUsImF1dGhIck9yZ0lkIjoiMTc1MzA2MjgiLCJhdXRoSHJPcmdQcm92aWRlcklkIjoid3V6aSIsImF1dGhPcmdJZEFuZFByb3ZpZGVySWQiOiI0NjQzMjIzODQ3OTU2OTMwNTZ8ZW5naW5lZXIiLCJjb21wYW55SWQiOiJkODg0ZmI3OS0zOTJjLTQyYzUtYmExMy1lYWIzYmRiOTkzZWQiLCJjb21wYW55UGF0aCI6IjAwMDAxMDAwNDkwMDAyNyIsImNvbXBhbnlOYW1lIjoi5Lic5YyX5YWs5Y+4IiwiY29tcGFueUZ1bGxOYW1lIjoi5Lit6ZOB54mp6LWE6ZuG5Zui5Lic5YyX5pyJ6ZmQ5YWs5Y+4In0='
    token_bad = 'eyJhdXRoT3JnUHJvdmlkZXJJZCI6ImVuZ2luZWVyIiwiYXV0aE9yZ0lkIjoiNDY0MzIyMzg0Nzk1NjkzMDU2IiwiYXV0aE9yZ1BhdGgiOiIwMDAwMTAwMDQ5MDAwMjcwMDA1NiIsIm9yZ1NpbXBsZU5hbWUiOiLms7DlronkuovkuJrpg6giLCJhdXRoT3JnTmFtZSI6IuazsOWuieS6i-S4mumDqCIsImF1dGhPcmdGdWxsUGF0aE5hbWUiOiLkuK3lm73pk4Hlu7ov5Lit6ZOB54mp6LWEL-S4nOWMl-WFrOWPuC_ms7DlronkuovkuJrpg6giLCJhdXRoT3JnVHlwZSI6IjIiLCJpc0RlZmF1bHQiOmZhbHNlLCJhdXRoSHJPcmdJZCI6IjE3NTMwNjI4IiwiYXV0aEhyT3JnUHJvdmlkZXJJZCI6Ind1emkiLCJjb21wYW55SWQiOiJkODg0ZmI3OS0zOTJjLTQyYzUtYmExMy1lYWIzYmRiOTkzZWQiLCJjb21wYW55UGF0aCI6IjAwMDAxMDAwNDkwMDAyNyIsImNvbXBhbnlOYW1lIjoi5Lic5YyX5YWs5Y-4IiwiY29tcGFueUZ1bGxOYW1lIjoi5Lit6ZOB54mp6LWE6ZuG5Zui5Lic5YyX5pyJ6ZmQ5YWs5Y-4IiwiYXV0aE9yZ0lkQW5kUHJvdmlkZXJJZCI6IjQ2NDMyMjM4NDc5NTY5MzA1NnxlbmdpbmVlciJ9'

    compare_tokens(token_good, token_bad)

    # data = decode_single_segment_token(token)
    # print(json.dumps(data, ensure_ascii=False, indent=2))