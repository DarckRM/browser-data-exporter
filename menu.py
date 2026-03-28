import json
import time
import typer
import argparse
import api
import asyncio
import fetch_cookie
from rich import print
from rich.console import Console
from rich.table import Table
from playwright.async_api import Page, async_playwright, Playwright

DEPTS_CACHE = []

CURRENT_USER = "Anyone"
CURRENT_DEPT = {}

CONS = json.load(open('CONSTANTS', 'r'))

async def login_method_callback(choice, playwright: Playwright) -> Page:
    if choice == "1":
        # 这里可以调用使用 cookies 登录的函数
        page = await fetch_cookie.login_with_cookies(playwright)
    elif choice == "2":
        # 这里可以调用扫码登录的函数
        page = await fetch_cookie.login(playwright)
    else:
        print("❌ 无效的选择，请重新选择。")


async def ui_choose_login(console: Console, playwright: Playwright):
    table = Table(title="登录方式选择")

    table.add_column("选项", justify="center", style="cyan", no_wrap=True)
    table.add_column("描述", justify="left", style="cyan")

    table.add_row("1", "使用上次保存的账户（cookies 登录）")
    table.add_row("2", "新账户扫码登录")

    console.print(table)

    choice = typer.prompt("请输入选项编号")

    page = await login_method_callback(choice, playwright)
    # 刷新屏幕
    console.clear()
    print(
        f"✅ [green]已成功登录工作平台[/green]: 用户({CURRENT_USER}) - 部门({CURRENT_DEPT})")

async def ui_select_dept(console: Console, playwright: Playwright):
    global DEPTS_CACHE
    if len(DEPTS_CACHE) == 0:
        DEPTS_CACHE = api.request_dept(CONS['DEPT_LIST_URL'])

    # 选择部门后

    # 等待某个响应并获取 RespoRes Header
    # async with page.expect_response(RESPONSE_URL, timeout=3000000) as resp_info:
    #     text = await resp_info.value
    #     print(text)
    
    table = Table()
    table.add_column("序号", justify="center", style="cyan", no_wrap=True)
    table.add_column("部门名称", justify="left", style="cyan")

    for idx, dept in enumerate(DEPTS_CACHE, start=1):
        table.add_row(str(idx), dept['orgSimpleName'])

    console.print(table)

    choice = typer.prompt("请输入部门序号")

    try:
        choice_num = int(choice)
        if 1 <= choice_num <= len(DEPTS_CACHE):
            global CURRENT_DEPT
            CURRENT_DEPT = DEPTS_CACHE[choice_num - 1]
            print(f"✅ 已选择部门: {CURRENT_DEPT['orgSimpleName']}")
            await ui_feature_menu(console, playwright)
        else:
            print("❌ 无效的选项，重新选择。")
            await ui_select_dept(console, playwright)
    except ValueError:
        print("❌ 输入不是数字，重新选择。")
        await ui_select_dept(console, playwright)


async def ui_feature_menu(console: Console, playwright: Playwright):
    table = Table(title="功能选择", title_justify="left")

    table.add_column("选项", justify="center", style="cyan", no_wrap=True)
    table.add_column("描述", justify="left", style="cyan")

    table.add_row("1", "选择部门（当前部门: [yellow]{}[/yellow]）".format(CURRENT_DEPT['orgSimpleName'] if CURRENT_DEPT else "未选择"))
    table.add_row("2", "指定合同编号导出表格")
    table.add_row("3", "根据预设条件导出合同表格")

    console.print(table)

    choice = console.input("请输入选项编号: ")
    console.clear()
    await ui_feature_callback(choice, console, playwright)


async def ui_feature_callback(choice, console: Console, playwright: Playwright):
    if choice == "1":
        await ui_select_dept(console, playwright)
    elif choice == "2":
        await ui_export_specific_contract(console)
    elif choice == "3":
        await ui_auto_export_contracts(console)
    else:
        print("❌ 无效的选择，请重新选择。")
        await ui_feature_menu(console, playwright)


async def ui_auto_export_contracts(console: Console):
    table = Table()
    table.add_column("序号", justify="center", style="cyan", no_wrap=True)
    table.add_column("合同编号", justify="left", style="cyan", no_wrap=True)
    table.add_column("合同名称", justify="left", style="cyan")
    for idx, item in enumerate(load_contracts(), start=1):
        table.add_row(str(idx), item['contractCode'], item['contractName'])
    console.print(table)
    export = typer.confirm("⚠️ 将要导出以上合同的数据，请做最后确认", abort=False)
    if export:
        print("正在导出合同数据... (功能正在开发中)")
    else:
        console.clear()
        console.print("[yellow]已取消导出，返回功能菜单[/yellow]")
        await ui_feature_menu(console)


async def ui_export_specific_contract(console: Console):
    table = Table()
    table.add_column("序号", justify="center", style="cyan", no_wrap=True)
    table.add_column("合同编号", justify="left", style="cyan", no_wrap=True)
    table.add_column("合同名称", justify="left", style="cyan")
    for idx, item in enumerate(load_contracts(), start=1):
        table.add_row(str(idx), item['contractCode'], item['contractName'])
    console.print(table)
    contract_code = typer.prompt("请输入要导出的合同序号")
    console.clear()
    console.print(f"❌ 未找到合同编号 {contract_code}，请检查输入是否正确。")
    await ui_feature_menu(console)


def load_contracts(path='./data/contracts.json'):
    datas = api.request_contracts(CONS['CONTRACT_LIST_URL'], CURRENT_DEPT['authOrgId'], "2024-01-01", "2024-12-31")
    # datas = json.load(open('./data/contracts.json', 'r'))
    return datas


async def logic_enter(playwright: Playwright):
    console = Console()
    console.clear()
    await ui_choose_login(console, playwright)
    await ui_feature_menu(console, playwright)

async def main():
    async with async_playwright() as playwright:
        await logic_enter(playwright)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--sso-url', type=str, default="", help='SSO 登录页面 URL')
    parser.add_argument('--cookie-file', type=str,
                        default="", help='保存 cookies 的文件路径')
    parser.add_argument('--target-url-a', type=str, default="", help='A 目标页面 URL')
    parser.add_argument('--target-url-b', type=str, default="", help='B 目标页面 URL')
    parser.add_argument('--target-url-c', type=str, default="", help='C 目标页面 URL')

    args = parser.parse_args()

    asyncio.run(main())

    while True:
        time.sleep(1)
