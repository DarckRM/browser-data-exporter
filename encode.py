import base64
import json
from typing import Any, Dict, Union

JSONType = Union[Dict[str, Any], list, str, int, float, bool, None]

def b64url_encode_no_pad(data: bytes) -> str:
    # urlsafe_b64encode 会用 - _，符合 base64url
    s = base64.b64encode(data).decode("utf-8")
    return s.rstrip("=")  # 去掉 padding，生成“单段 token”常见格式

def encode_single_segment_token(obj: JSONType, *, ensure_ascii: bool = False) -> str:
    # ensure_ascii=False: 中文会以 UTF-8 直接输出；更贴近你示例里包含中文的场景
    json_text = json.dumps(obj, ensure_ascii=ensure_ascii, separators=(",", ":"))
    return b64url_encode_no_pad(json_text.encode("utf-8"))

if __name__ == "__main__":
    payload = {
        "authOrgProviderId": "engineer",
        "authOrgId": "464322384795693056",
        "authOrgPath": "00001000490002700056",
        "orgSimpleName": "泰安事业部",
        "authOrgName": "泰安事业部",
        "authOrgFullPathName": "中国铁建/中铁物资/东北公司/泰安事业部",
        "authOrgType": "2",
        "isDefault": True,
        "authHrOrgId": "17530628",
        "authHrOrgProviderId": "wuzi",
        "authOrgIdAndProviderId": "464322384795693056|engineer",
        "companyId": "d884fb79-392c-42c5-ba13-eab3bdb993ed",
        "companyPath": "000010004900027",
        "companyName": "东北公司",
        "companyFullName": "中铁物资集团东北有限公司"
    }

    token = encode_single_segment_token(payload, ensure_ascii=False)
    print(token)