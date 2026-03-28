import base64
import json
from typing import Any, Dict, Union

JSONType = Union[Dict[str, Any], list, str, int, float, bool, None]

def b64url_encode_no_pad(data: bytes) -> str:
    # urlsafe_b64encode 会用 - _，符合 base64url
    s = base64.urlsafe_b64encode(data).decode("ascii")
    return s.rstrip("=")  # 去掉 padding，生成“单段 token”常见格式

def encode_single_segment_token(obj: JSONType, *, ensure_ascii: bool = False) -> str:
    # ensure_ascii=False: 中文会以 UTF-8 直接输出；更贴近你示例里包含中文的场景
    json_text = json.dumps(obj, ensure_ascii=ensure_ascii, separators=(",", ":"))
    return b64url_encode_no_pad(json_text.encode("utf-8"))

if __name__ == "__main__":
    payload = {
        "authOrgProviderId": "engineer",
        "authOrgId": "333638530171539456",
        "authOrgPath": "0000100049000270002200003",
        "orgSimpleName": "示例部门",
        "isDefault": False,
        "authHrOrgId": "17530628",
        "authHrOrgProviderId": "wuzi",
        "authOrgIdAndProviderId": "333638530171539456|engineer",
    }

    token = encode_single_segment_token(payload, ensure_ascii=False)
    print(token)