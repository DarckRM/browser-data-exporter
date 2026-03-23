import json
import typer
import argparse
import api
from rich import print
from rich.console import Console
from rich.table import Table

CURRENT_USER = "Anyone"
CURRENT_DEPT = "Moon Base"


def login_method_callback(choice):
    if choice == "1":
        # 这里可以调用使用 cookies 登录的函数
        print("使用 cookies 登录功能正在开发中...")
    elif choice == "2":
        # 这里可以调用扫码登录的函数
        print("扫码登录功能正在开发中...")
    else:
        print("❌ 无效的选择，请重新选择。")


def ui_choose_login(console: Console):
    table = Table(title="登录方式选择")

    table.add_column("选项", justify="center", style="cyan", no_wrap=True)
    table.add_column("描述", justify="left", style="cyan")

    table.add_row("1", "使用上次保存的账户（cookies 登录）")
    table.add_row("2", "新账户扫码登录")

    console.print(table)

    choice = typer.prompt("请输入选项编号")

    login_method_callback(choice)
    # 刷新屏幕
    console.clear()
    print(
        f"✅ [green]已成功登录工作平台[/green]: 用户({CURRENT_USER}) - 部门({CURRENT_DEPT})")

def ui_select_dept(console: Console):
    api.request_dept('')
    return


def ui_feature_menu(console: Console):
    table = Table(title="功能选择", title_justify="left")

    table.add_column("选项", justify="center", style="cyan", no_wrap=True)
    table.add_column("描述", justify="left", style="cyan")

    table.add_row("1", "指定合同编号导出表格")
    table.add_row("2", "根据预设条件导出合同表格")

    console.print(table)

    choice = console.input("请输入选项编号: ")
    console.clear()
    ui_feature_callback(choice, console)


def ui_feature_callback(choice, console: Console):
    if choice == "1":
        ui_export_specific_contract(console)
    elif choice == "2":
        ui_auto_export_contracts(console)
    else:
        print("❌ 无效的选择，请重新选择。")


def ui_auto_export_contracts(console: Console):
    table = Table()
    table.add_column("合同编号", justify="center", style="cyan", no_wrap=True)
    table.add_column("合同名称", justify="left", style="cyan")
    for item in load_contracts():
        table.add_row(item['contractCode'], item['contractName'])
    console.print(table)
    export = typer.confirm("⚠️ 将要导出以上合同的数据，请做最后确认", abort=False)
    if export:
        print("正在导出合同数据... (功能正在开发中)")
    else:
        console.clear()
        console.print("[yellow]已取消导出，返回功能菜单[/yellow]")
        ui_feature_menu(console)


def ui_export_specific_contract(console: Console):
    contract_code = typer.prompt("请输入要导出的合同编号")
    for contract in load_contracts() if contract_code else []:
        if contract['contractCode'] == contract_code:
            print(f"正在导出合同 {contract_code} 的数据... (功能正在开发中)")
            return
    console.clear()
    console.print(f"❌ 未找到合同编号 {contract_code}，请检查输入是否正确。")
    ui_feature_menu(console)


def load_contracts(path='./data/contracts.json'):
    datas = json.load(open('./data/contracts.json', 'r'))
    return datas


def logic_enter():
    console = Console()
    console.clear()
    ui_choose_login(console)
    ui_feature_menu(console)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sso-url', type=str, default="", help='SSO 登录页面 URL')
    parser.add_argument('--cookie-file', type=str,
                        default="", help='保存 cookies 的文件路径')
    parser.add_argument('--target-url-a', type=str, default="", help='A 目标页面 URL')
    parser.add_argument('--target-url-b', type=str, default="", help='B 目标页面 URL')
    parser.add_argument('--target-url-c', type=str, default="", help='C 目标页面 URL')

    args = parser.parse_args()
    logic_enter()
