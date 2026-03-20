import sys
import time
import json
import asyncio
import typer
from playwright.async_api import async_playwright, Playwright
# https://xxxx.edu.cn/appportalweb/seatspace/
from rich import print
from rich.console import Console
from rich.table import Table

CURRENT_USER = "Anyone"
CURRENT_DEPT = "Moon Base"

"""
需要提前10分钟获取ck
"""
# WEB_DOMAIN = "http://172.16.0.12"
WEB_DOMAIN = "http://127.0.0.1:8081"
# TARGET_URL_PREFIX = 'http://172.16.0.12/managerPage'
TARGET_URL_PREFIX = 'http://127.0.0.1:8081/dashboard/home'
# RESPONSE_URL = "http://172.16.0.12/api/sys/user/userInfo"
RESPONSE_URL = "http://127.0.0.1:8081/jsgy-api/sys/permission/getUserPermissionByToken*"


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False)

    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(WEB_DOMAIN)

    try:
        await page.wait_for_function(
            f"window.location.href.startsWith('{TARGET_URL_PREFIX}')",
            timeout=1200000
        )
        print("✅ 登录成功！")
        print("[bold red]Alert![/bold red] [green]Portal gun[/green] shooting! :boom:")
        cookies = await context.cookies()

        # 将数据写入 JSON 文件
        with open('./config.json', 'w') as json_file:
            json.dump(cookies, json_file)
    except Exception:
        print("❌ 等待超时，未检测到登录成功。程序退出。")
        await page.close()
        await context.close()
        sys.exit(1)

    await page.reload()

    # 等待某个响应并获取 RespoRes Header
    async with page.expect_response(RESPONSE_URL, timeout=3000000) as resp_info:
        text = await resp_info.value
        print(text)

    # ---------------------
    while True:
        time.sleep(1)

    context.close()
    browser.close()


async def main():
    async with async_playwright() as playwright:
        typer.run(await run(playwright))


def login_method_callback(choice):
    if choice == "1":
        # 这里可以调用使用 cookies 登录的函数
        print("使用 cookies 登录功能正在开发中...")
    elif choice == "2":
        # 这里可以调用扫码登录的函数
        print("扫码登录功能正在开发中...")
    else:
        print("❌ 无效的选择，请重新选择。")


def ui_main(console: Console):
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
        logic_enter()


def ui_export_specific_contract(console: Console):
    contract_code = typer.prompt("请输入要导出的合同编号")
    for contract in load_contracts() if contract_code else []:
        if contract['contractCode'] == contract_code:
            print(f"正在导出合同 {contract_code} 的数据... (功能正在开发中)")
            return
        else:
            print(f"❌ 未找到合同编号 {contract_code}，请检查输入是否正确。")


def load_contracts(path='./data/contracts.json'):
    datas = json.load(open('./data/contracts.json', 'r'))
    return datas


def logic_enter():
    console = Console()
    console.clear()
    ui_main(console)
    ui_feature_menu(console)


if __name__ == "__main__":
    # asyncio.run(main())
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row("Raising shields", "[bold magenta]COMPLETED [green]:heavy_check_mark:")

    print(grid)
    # logic_enter()
