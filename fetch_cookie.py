import sys
import time
import json
import asyncio
import typer
from playwright.async_api import async_playwright, Playwright
# https://xxxx.edu.cn/appportalweb/seatspace/

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




if __name__ == "__main__":
    # asyncio.run(main())
    grid = Table.grid(expand=True)
    grid.add_column()
    grid.add_column(justify="right")
    grid.add_row("Raising shields",
                 "[bold magenta]COMPLETED [green]:heavy_check_mark:")

    print(grid)
    # logic_enter()
