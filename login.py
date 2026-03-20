import asyncio
from playwright.async_api import async_playwright
import pickle
import os
import requests
from urllib.parse import urljoin
from PIL import Image
import io
import sys

COOKIE_DIR = "cookies"
COOKIE_FILE = os.path.join(COOKIE_DIR, "cookies.pkl")
STATE = os.path.join(COOKIE_DIR, "state")
TARGET_URL_PREFIX = "https://mh.crmg.cn/portal/toMain/"

async def save_cookies(context, path=COOKIE_FILE):
    # 确保目录存在
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cookies = await context.cookies()
    with open(path, "wb") as f:
        pickle.dump(cookies, f)
    await save_state(context)  # 同时保存状态

async def save_state(context, path=STATE):
    # 确保目录存在
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump(context, f)

async def load_cookies(context, path=COOKIE_FILE):
    if os.path.exists(path):
        print("步骤 1: 检测到 cookies 文件，尝试加载...")
        with open(path, "rb") as f:
            cookies = pickle.load(f)
        await context.add_cookies(cookies)
        page = await context.new_page()
        await page.goto(TARGET_URL_PREFIX)
        if page.url.startswith(TARGET_URL_PREFIX):
            print("✅ Cookies 有效，已直接进入主页面")
            return True
        else:
            print("⚠️ Cookies 已过期或无效，删除旧文件")
            os.remove(path)
            return False
    else:
        print("⚠️ 未找到 cookies 文件，需要重新扫码登录")
        return False

def show_block_qrcode(img_bytes, width=40, border=4):
    """把 PNG 图片转成黑白方块二维码并打印到终端"""
    img = Image.open(io.BytesIO(img_bytes)).convert("1")  # 转黑白

    # 给二维码加白边
    w, h = img.size
    new_w, new_h = w + 2 * border, h + 2 * border
    bordered = Image.new("1", (new_w, new_h), 1)  # 白色背景
    bordered.paste(img, (border, border))
    img = bordered

    # 缩放到指定宽度
    w, h = img.size
    aspect_ratio = h / w
    new_height = int(width * aspect_ratio)
    img = img.resize((width, new_height))

    pixels = list(img.getdata())
    ascii_lines = []
    for i in range(0, len(pixels), width):
        # 黑色像素用方块，白色用空格
        line = "".join("  " if pixel == 0 else "██" for pixel in pixels[i:i+width])
        ascii_lines.append(line)

    for line in ascii_lines:
        print(line)

async def login_qrcode(page, context):
    print("步骤 1: 打开登录页面...")
    await page.goto("https://mh.crmg.cn/portal/toMain/")

    print("步骤 2: 点击扫码登录按钮...")
    try:
        await page.click("text=扫码登录")
        print("✅ 已点击扫码登录按钮")
    except:
        await page.evaluate("changeLoginMode('scan')")
        print("✅ 已通过 JS 切换到扫码登录模式")
    await page.wait_for_timeout(2000)

    print("步骤 3: 遍历所有 iframe 查找二维码...")
    qr_url = None
    for frame in page.frames:
        imgs = await frame.query_selector_all("img")
        for img in imgs:
            src = await img.get_attribute("src")
            if src and "qrImg" in src:  # 关键字匹配二维码
                qr_url = urljoin(frame.url, src)
                print(f"✅ 在 iframe 中找到二维码地址: {qr_url}")
                break
        if qr_url:
            break

    if qr_url:
        print("步骤 4: 下载二维码并在终端显示黑白方块...")
        resp = requests.get(qr_url)
        show_block_qrcode(resp.content, width=40, border=4)
        print("✅ 二维码已显示在终端，请用手机扫码登录...")
    else:
        print("❌ 未能提取到二维码地址，保存截图调试")
        await page.screenshot(path="debug.png")
        print("⚠️ 已保存页面截图 debug.png 供排查")

    print("步骤 5: 检测是否跳转到主页面...")
    try:
        await page.wait_for_function(
            f"window.location.href.startsWith('{TARGET_URL_PREFIX}')",
            timeout=120000
        )
        print("✅ 登录成功！")
        await save_cookies(context)  # 登录成功后再保存
        print(f"✅ Cookies 已保存到 {COOKIE_FILE}")
    except Exception:
        print("❌ 等待超时，未检测到登录成功。程序退出。")
        await page.close()
        await context.close()
        sys.exit(1)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()

        # 交互界面放在最前面
        print("请选择登录方式：")
        print("1. 使用上次保存的账户（cookies 登录）")
        print("2. 新账户扫码登录")
        choice = input("请输入选项 (1/2): ").strip()

        if choice == "1":
            if not await load_cookies(context):
                print("⚠️ Cookies 无效或不存在，切换到扫码登录")
                page = await context.new_page()
                await login_qrcode(page, context)
        elif choice == "2":
            page = await context.new_page()
            await login_qrcode(page, context)
        else:
            print("❌ 输入无效，程序退出")
            sys.exit(1)
        


        print("步骤 6: 已进入主页面，可以继续后续操作...")
        await browser.close()

        # 登录成功后调用另一个 py 文件
        subprocess.run([sys.executable, "menu.py"])

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
