import sys
import time
import json
import asyncio
import typer
from playwright.async_api import Page, async_playwright, Playwright
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

CONS = json.load(open('CONSTANTS', 'r'))

async def init_browser(playwright: Playwright): 
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context()
    page = await context.new_page()

    return browser, context, page

async def direct_to_target(page):
    target_url = CONS['WORKBENCH_URL']
    await page.goto(target_url)

    try:
        await page.wait_for_function(
            f"window.location.href.startsWith('{target_url}')",
            timeout=6200000
        )
        print("✅ 已经成功进入目标页面！")
        # 保持该页面 cookie

    except Exception:
        print("❌ 等待超时，未检测到进入目标页面。程序退出。")
        await page.close()
        sys.exit(1)

async def run_with_cookies(playwright: Playwright) -> "Page":
    browser, context, page = await init_browser(playwright)

    workbench_url = CONS['WORKBENCH_URL']

    # 从文件加载 cookies
    with open('./cookies/sso_cookies.json', 'r') as json_file:
        cookies = json.load(json_file)
        await context.add_cookies(cookies)
    
    await page.goto(workbench_url)

    try:
        await page.wait_for_function(
            f"window.location.href.startsWith('{workbench_url}')",
            timeout=6200000
        )
        print("✅ 使用 cookies 登录成功！")
        workbench_cookies = await context.cookies()

        with open('./cookies/workbench_cookies.json', 'w') as json_file:
            json.dump(workbench_cookies, json_file)

    except Exception:
        print("❌ 等待超时，未检测到登录成功。程序退出。")
        await page.close()
        await context.close()
        sys.exit(1)

    return page


async def run(playwright: Playwright, sso_url: str = CONS['SSO_URL'], verify_url: str = CONS['VERIFY_URL'] ) -> "Page":
    browser, context, page = await init_browser(playwright)

    await page.goto(verify_url)

    # if user token is expired redirect to sso login page
    try:
        # waiting user manually login and redirect to verify_url
        await page.wait_for_function(
            f"window.location.href.startsWith('{verify_url}')",
            timeout=6200000
        )
        print("✅ 登录成功！")
        sso_cookies = await context.cookies()

        # verify page cookie is different from business page, saved with different name
        with open('./cookies/sso_cookies.json', 'w') as json_file:
            json.dump(sso_cookies, json_file)
    except Exception:
        print("❌ 等待超时，未检测到登录成功。程序退出。")
        await page.close()
        await context.close()
        sys.exit(1)

    await page.reload()

    # 等待某个响应并获取 RespoRes Header
    # async with page.expect_response(RESPONSE_URL, timeout=3000000) as resp_info:
    #     text = await resp_info.value
    #     print(text)

    return page



async def login_with_cookies(playwright: Playwright) -> "Page":
    return await run_with_cookies(playwright)


async def login(playwright: Playwright) -> "Page":
    return await run(playwright)


if __name__ == "__main__":
    asyncio.run(login())