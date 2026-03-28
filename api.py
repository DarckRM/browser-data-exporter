import requests
import time
import json

# How to fetch Cookie
cookies: list = json.load(open('cookies/workbench_cookies.json', 'r'))

COMMON_HEADERS = {
    "Cookie": "; ".join(f"{k}={v}" for k, v in {cookie['name']: cookie['value'] for cookie in cookies}.items()),
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0",
}
DEPTS = []


def request_dept(url: str) -> list[dict]:
    # url = "https://contract.pgyl.cn/permission/getHasPermissionAuthOrgs"
    data = {"authorizationCodes": [
        "business", "common"], "hrOrgId": "", "hrOrgProviderId": ""}
    resp = requests.post(url, json=data, headers=COMMON_HEADERS, timeout=10)
    resp.raise_for_status()
    depts = resp.json()
    for dept in depts:
        DEPTS.append(dept)
    return DEPTS 

def request_contracts(url: str, autOrgId: str, startTime: str, endTime: str) -> None:
    # url = "https://contract.pgyl.cn/scc-contract-business/contract/select"
    data = {"isMainContract": "0", "contractStatusList": ["2", "4"], "listType": "WH", "authOrgId": autOrgId, "contractClassifyCodeList": [
        "CONTRACT_CLASSIFY01"], "dataType": "contract", "authOrgType": "2", "viewId": 1, "createTimeStart": startTime, "createTimeEnd": endTime, "isOperator": 0, "listQueryType": "CHECK", "qryScene": "JYF", "pageSize": 20, "pageNo": 1}
    resp = requests.post(url, json=data, headers=COMMON_HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()['data']
    print(f"Total Contracts: {data.get('total', 0)}")
    contracts = data.get('list', [])

    print("Available Contracts:")
    num = 1
    for contract in contracts:
        print(f"{num}: {contract['contractName']}")
        num += 1

    choice = input("请输入选项: ").strip()
    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(contracts):
            selected_contract = contracts[choice_num - 1]
            print(f"你选择了: {selected_contract['contractName']}")
            export_specific_contract(selected_contract)
        else:
            print("无效的选项，程序退出。")
    except ValueError:
        print("输入不是数字，程序退出。")


def request_materials(url: str) -> None:
    # url = "https://contract.pgyl.cn/scc-contract-business/material/qryMaterialList"
    data = {"pageNo": 1, "pageSize": 20, "materialName": "", "materialCode": "",
            "authOrgId": "00001000490002700056", "authOrgType": "2"}
    resp = requests.post(url, json=data, headers=COMMON_HEADERS, timeout=10)
    resp.raise_for_status()
    data = resp.json()['data']
    print(f"Total Materials: {data.get('total', 0)}")
    materials = data.get('list', [])

    print("Available Materials:")
    for material in materials:
        print(f"{material['materialName']}")


def export_specific_contract(url: str, contract: dict) -> None:
    # url = "https://contract.pgyl.cn/scc-contract-business/contract/qryContractRelevance"

    resp = requests.post(url, json=contract,
                         headers=COMMON_HEADERS, timeout=10)
    resp.raise_for_status()

    detail = resp.json().get('data', {})

    export_info = {
        "合同名称": detail['contractName'],
        "卖方合同编号": detail['contractCode'],
        "签约时间": detail['signDate'],
        "业务部门": detail['deptName'],
        "工程项目": detail['projectName'],
        "业务类型": detail['gdContractType'],
        "标的物信息": [
            {"memo": "参考标的物信息接口"}
        ]
    }
    print(f"Exported Contract Details for: {export_info}")


if __name__ == "__main__":
    now_time = time.strftime("%Y-%m-%d", time.localtime())
    decade_ago_time = time.strftime(
        "%Y-%m-%d", time.localtime(time.time() - 10 * 365 * 24 * 3600))

    request_contracts(startTime=decade_ago_time, endTime=now_time)
