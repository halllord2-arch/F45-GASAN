"""
[1단계] 처음 한 번만 실행하세요.
네이버에 직접 로그인하면 세션이 저장됩니다.
이후 blog_auto_post.py 가 저장된 세션으로 자동 게시합니다.
"""

import asyncio
import os
from playwright.async_api import async_playwright

async def save_login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--no-sandbox", "--disable-setuid-sandbox"],
        )
        context = await browser.new_context()
        page = await context.new_page()

        print("=" * 50)
        print("  브라우저가 열리면 네이버에 직접 로그인해주세요.")
        print("  로그인 완료 후 이 창을 닫지 말고 기다려주세요.")
        print("=" * 50)

        await page.goto(
            "https://nid.naver.com/nidlogin.login?mode=form",
            wait_until="domcontentloaded",
            timeout=60000,
        )
        await page.wait_for_url("https://www.naver.com/**", timeout=120000)

        session_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "naver_session.json"
        )
        await context.storage_state(path=session_path)
        print(f"\n✅ 로그인 세션이 저장되었습니다! ({session_path})")
        print("   이제 blog_auto_post.py 를 실행하면 자동으로 게시됩니다.")

        await browser.close()

asyncio.run(save_login())
