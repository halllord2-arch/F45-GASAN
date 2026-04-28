"""
F45 가산 네이버 블로그 자동 게시 프로그램
- 글 자동 생성
- 운동 사진 자동 삽입
- 네이버 블로그 자동 게시

실행: python blog_auto_post.py
"""

import asyncio
import random
import os
import requests
from playwright.async_api import async_playwright
from datetime import datetime

# ═══════════════════════════════════════════════
#  ★ 여기만 수정하세요
NAVER_BLOG_ID = "f45gasan"   # 네이버 블로그 아이디
# ═══════════════════════════════════════════════


# ── 블로그 콘텐츠 ────────────────────────────────
TOPICS = [
    {
        "titles": [
            "퇴근 후 운동, 가산디지털단지 직장인이라면 이렇게 하세요",
            "야근이 잦은 직장인을 위한 최고의 운동법",
            "가산역 직장인 필독! 짧고 강한 운동이 답입니다",
            "운동할 시간이 없다는 핑계, 이제 끝낼 때가 됐습니다",
        ],
        "bodies": [
            """하루 종일 의자에 앉아 업무를 보다 보면 어느새 체력도, 체형도 무너지기 시작합니다. 가산디지털단지에서 일하는 직장인이라면 공감하실 겁니다.

퇴근 후 운동을 결심해도 헬스장 가면 뭘 해야 할지 모르겠고, 혼자 하다 보면 금방 지루해져서 포기하게 되죠.

그래서 가산에 F45 Training이 생겼습니다.

■ F45가 직장인에게 딱인 이유

✔ 딱 45분만 투자하면 됩니다
점심시간이나 퇴근 후 45분. 불필요한 준비 시간 없이 바로 시작하고 바로 끝납니다.

✔ 매번 코치가 이끌어줍니다
헬스장에서 멍하니 서 있을 필요 없습니다. 처음부터 끝까지 전문 코치가 함께하며 동작을 안내해줍니다.

✔ 매번 다른 운동으로 지루할 틈이 없습니다
80가지 이상의 프로그램이 매번 달라져 질리지 않고 꾸준히 다닐 수 있습니다.

■ 가산디지털단지역에서 도보 5분
1호선·7호선 가산디지털단지역에서 걸어서 5분 거리. 퇴근길에 바로 들를 수 있는 최적의 위치입니다.

지금 1주일 무제한 체험을 신청해보세요.

📍 서울 금천구 벚꽃로 254
📞 010-8019-0450
🔗 1주일 무제한 체험 신청: https://booking.naver.com/booking/13/bizes/1102558""",
            """"운동해야 하는데..." 라는 말을 달고 사는 직장인분들께 이 글을 씁니다.

바쁜 건 맞습니다. 야근도 많고, 퇴근하면 지쳐서 아무것도 하기 싫은 날도 있죠. 그런데 그렇게 1년, 2년이 지나면 몸이 먼저 이상 신호를 보내기 시작합니다.

가산디지털단지에서 운동하기 딱 좋은 곳이 생겼습니다. F45 Training 가산점입니다.

■ 45분이면 충분합니다
F45는 45분 안에 유산소와 근력 운동을 동시에 할 수 있도록 과학적으로 설계된 프로그램입니다. 한 세션에 최대 750kcal를 소모할 수 있습니다.

■ 혼자가 아니라 팀으로
그룹 트레이닝 방식이라 함께하는 멤버들과 서로 동기부여가 됩니다.

운동을 시작하기 가장 좋은 타이밍은 바로 지금입니다.

📍 가산디지털단지역 도보 5분
🔗 체험 신청: https://booking.naver.com/booking/13/bizes/1102558""",
        ],
        "tags": ["가산디지털단지헬스장", "가산역운동", "직장인운동", "가산PT", "금천구헬스장", "F45가산", "가산피트니스", "직장인다이어트"],
        "photo_keyword": "gym workout fitness",
    },
    {
        "titles": [
            "45분 운동이 2시간 운동보다 효과적인 과학적 이유",
            "짧게 운동해도 될까요? F45 45분 트레이닝의 진실",
            "하루 45분, 8주면 체형이 달라집니다",
            "운동 시간이 길다고 더 좋은 게 아닙니다",
        ],
        "bodies": [
            """많은 분들이 '운동은 오래 해야 효과가 있다'고 생각합니다. 그런데 정말 그럴까요?

스포츠 과학 연구에 따르면, 고강도 인터벌 트레이닝(HIIT) 방식의 45분 운동이 저강도 장시간 운동보다 체지방 감소와 근력 향상에 훨씬 더 효과적입니다.

■ 45분 안에 일어나는 일
✔ 0~10분: 몸이 워밍업되며 심박수가 올라갑니다
✔ 10~35분: 고강도 인터벌로 체지방이 빠르게 연소됩니다
✔ 35~45분: 마무리 운동으로 근육 회복을 돕습니다

■ 애프터번 효과
F45 운동 후에는 운동이 끝나도 최대 수 시간 동안 칼로리가 계속 소모됩니다. 즉, 운동하고 나서도 몸이 계속 일하는 셈입니다.

■ 실제 변화까지 얼마나 걸릴까요?
꾸준히 다닌 멤버들의 평균 체형 변화 시점은 약 8주입니다.

📍 서울 금천구 벚꽃로 254 (가산디지털단지역 도보 5분)
🔗 https://booking.naver.com/booking/13/bizes/1102558""",
        ],
        "tags": ["45분운동", "HIIT", "가산디지털단지헬스장", "F45가산", "체지방감소", "그룹피트니스", "가산피트니스", "애프터번효과"],
        "photo_keyword": "HIIT training exercise",
    },
    {
        "titles": [
            "30대부터 시작하는 체형 관리, 이것만 알면 됩니다",
            "40대에도 체형 바꿀 수 있습니다",
            "30·40대 직장인 체형 관리, F45가 나은 이유",
            "나이 들수록 더 중요한 근력 운동",
        ],
        "bodies": [
            """30대가 되면서 예전과 같이 먹어도 살이 더 잘 찌고, 빠지지 않는다는 걸 느끼기 시작합니다.

이건 의지력의 문제가 아닙니다. 나이가 들수록 기초대사량이 낮아지고 근육량이 감소하기 때문입니다.

■ 30·40대 체형 관리의 핵심
단순 다이어트나 유산소 운동만으로는 한계가 있습니다. 체지방을 줄이면서 근육량을 유지해야 기초대사량이 올라갑니다.

■ F45가 30·40대에 효과적인 이유
✔ 유산소 + 근력을 동시에
✔ 관절 부담 최소화
✔ 코치의 자세 교정
✔ 짧은 시간 고효율 45분

가산디지털단지에서 체형 관리를 시작하고 싶은 30·40대라면 F45 가산의 1주일 무제한 체험을 경험해보세요.

📍 서울 금천구 벚꽃로 254
🔗 https://booking.naver.com/booking/13/bizes/1102558""",
        ],
        "tags": ["30대운동", "40대운동", "직장인체형관리", "가산디지털단지헬스장", "F45가산", "근력운동", "체지방감소", "금천구헬스장"],
        "photo_keyword": "functional fitness training",
    },
    {
        "titles": [
            "혼자 운동하면 작심삼일, 그룹 트레이닝이 답인 이유",
            "F45 그룹 트레이닝이 개인 PT보다 나은 점",
            "가산 직장인들이 그룹 피트니스에 빠진 이유",
        ],
        "bodies": [
            """운동을 꾸준히 하지 못하는 가장 큰 이유 중 하나가 '혼자 한다'는 것입니다.

■ 그룹 트레이닝의 힘
✔ 함께하면 포기하기 어렵습니다
✔ 코치가 항상 함께합니다
✔ 커뮤니티가 생깁니다
✔ 80가지 이상의 프로그램으로 지루함 없음

가산디지털단지에서 혼자 운동하다 포기한 경험이 있다면, 이번엔 F45 가산과 함께 시작해보세요.

📍 서울 금천구 벚꽃로 254 (가산디지털단지역 도보 5분)
🔗 1주일 무제한 체험: https://booking.naver.com/booking/13/bizes/1102558""",
        ],
        "tags": ["그룹피트니스", "그룹트레이닝", "F45가산", "가산디지털단지헬스장", "가산PT", "팀트레이닝", "금천구피트니스"],
        "photo_keyword": "group fitness class",
    },
    {
        "titles": [
            "F45 가산 1주일 무제한 체험 — 이렇게 신청하세요",
            "처음 운동 시작하는 분들을 위한 F45 가산 안내",
            "가산디지털단지 직장인이 퇴근 후 운동하기 좋은 곳",
        ],
        "bodies": [
            """운동을 시작하고 싶은데 어디서부터 시작해야 할지 모르겠다면, F45 가산의 1주일 무제한 체험부터 시작해보세요.

■ 1주일 무제한 체험이란?
1주일 동안 F45 가산의 모든 클래스를 원하는 만큼 이용할 수 있는 체험 프로그램입니다.

✔ CARDIO (유산소 집중)
✔ RESISTANCE (근력 집중)
✔ HYBRID (복합)
✔ RECOVERY (회복·스트레칭)

■ 이런 분께 추천합니다
• 운동을 처음 시작하는 분
• 헬스장을 등록해도 꾸준히 못 다니셨던 분
• 퇴근 후 짧은 시간에 효율적인 운동을 원하는 분
• 가산디지털단지 근처에서 운동할 곳을 찾고 계신 분

📍 서울 금천구 벚꽃로 254 (1호선·7호선 가산디지털단지역 도보 5분)
📞 010-8019-0450
🔗 지금 바로 신청하기: https://booking.naver.com/booking/13/bizes/1102558""",
        ],
        "tags": ["F45가산체험", "가산헬스장체험", "1주일무제한", "가산디지털단지헬스장", "그룹피트니스", "F45가산", "금천구운동", "운동시작"],
        "photo_keyword": "gym membership fitness center",
    },
]


def generate_content():
    topic = random.choice(TOPICS)
    return {
        "title":   random.choice(topic["titles"]),
        "body":    random.choice(topic["bodies"]),
        "tags":    topic["tags"],
        "photo_keyword": topic["photo_keyword"],
    }


def download_photo(keyword, save_path="blog_photo.jpg"):
    """Unsplash에서 운동 관련 사진을 무료로 다운로드"""
    encoded = keyword.replace(" ", "%20")
    url = f"https://source.unsplash.com/1200x800/?{encoded}"
    try:
        r = requests.get(url, allow_redirects=True, timeout=15)
        with open(save_path, "wb") as f:
            f.write(r.content)
        print(f"📸 사진 다운로드 완료")
        return os.path.abspath(save_path)
    except Exception as e:
        print(f"⚠️ 사진 다운로드 실패: {e}")
        return None


def set_clipboard(text):
    """PowerShell을 통해 클립보드에 텍스트 저장 (ctypes 불사용, 한글 지원)"""
    import subprocess
    # PowerShell Set-Clipboard: UTF-8 파이프로 안정적으로 처리
    encoded = text.encode("utf-16-le")
    ps_cmd = (
        "[System.Windows.Forms.Clipboard]::SetText("
        "[System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('"
        + __import__("base64").b64encode(encoded).decode()
        + "')))"
    )
    subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         f"Add-Type -AssemblyName System.Windows.Forms; {ps_cmd}"],
        capture_output=True,
    )


async def find_editor_frame(page):
    """SmartEditor ONE iframe을 URL 패턴으로 찾기"""
    await asyncio.sleep(3)

    # 모든 프레임 정보 출력 (디버그용)
    print("\n[디버그] 감지된 프레임 목록:")
    for f in page.frames:
        print(f"  이름: '{f.name}' | URL: {f.url[:80]}")

    # 1순위: mainFrame 이름으로 찾기
    for f in page.frames:
        if "mainFrame" in (f.name or ""):
            print(f"[디버그] mainFrame 발견: {f.name}")
            return f

    # 2순위: SmartEditor 관련 URL 패턴
    for f in page.frames:
        url = f.url or ""
        if any(kw in url for kw in ["SmartEditor", "PostWriteForm", "editor"]):
            print(f"[디버그] 에디터 URL 프레임 발견: {url[:80]}")
            return f

    # 3순위: blog.naver.com 도메인의 iframe (메인 제외)
    candidates = [f for f in page.frames if "blog.naver.com" in (f.url or "") and f != page.main_frame]
    if candidates:
        print(f"[디버그] blog.naver.com 프레임 발견: {candidates[0].url[:80]}")
        return candidates[0]

    # 4순위: 메인 페이지 자체에서 에디터 찾기
    print("[디버그] 별도 iframe 없음 — 메인 페이지 사용")
    return page.main_frame


async def insert_text_to_element(frame, selector, text, page):
    """contenteditable 요소에 텍스트를 삽입 — execCommand 우선, 클립보드 보조"""
    # 방법 1: frame.evaluate() + execCommand (iframe 안에서 직접 실행, 가장 안정적)
    try:
        el = await frame.wait_for_selector(selector, timeout=15000)
        await el.click()
        await asyncio.sleep(0.5)

        success = await frame.evaluate("""
            (args) => {
                const el = document.querySelector(args.selector);
                if (!el) return false;
                el.focus();
                const range = document.createRange();
                range.selectNodeContents(el);
                const sel = window.getSelection();
                sel.removeAllRanges();
                sel.addRange(range);
                return document.execCommand('insertText', false, args.text);
            }
        """, {"selector": selector, "text": text})

        if success:
            print(f"   [입력 성공] execCommand")
            return True
        print(f"   [입력] execCommand returned false, 클립보드로 재시도")
    except Exception as e:
        print(f"   [입력 실패] execCommand: {e}")

    # 방법 2: PowerShell 클립보드 → Ctrl+V
    try:
        el = await frame.wait_for_selector(selector, timeout=5000)
        await el.click()
        await asyncio.sleep(0.3)
        set_clipboard(text)          # PowerShell 기반, ctypes 없음
        await asyncio.sleep(0.5)
        await page.keyboard.press("Control+a")
        await asyncio.sleep(0.1)
        await page.keyboard.press("Control+v")
        await asyncio.sleep(0.5)
        print(f"   [입력 시도] 클립보드 붙여넣기")
        return True
    except Exception as e:
        print(f"   [입력 실패] 클립보드: {e}")

    return False


async def post_to_naver_blog(content, photo_path):
    # 스크립트 위치 기준으로 세션 파일 경로 고정
    script_dir = os.path.dirname(os.path.abspath(__file__))
    session_file = os.path.join(script_dir, "naver_session.json")
    if not os.path.exists(session_file):
        print(f"❌ 로그인 세션이 없습니다: {session_file}")
        print("   blog_login_save.py 를 먼저 실행해주세요.")
        return False

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=200)
        context = await browser.new_context(
            storage_state=session_file,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = await context.new_page()

        def safe_eval(coro):
            """evaluate 래퍼 — 오류 시 None 반환"""
            return coro

        try:
            # ── 1. 글쓰기 페이지 이동
            write_url = f"https://blog.naver.com/PostWriteForm.naver?blogId={NAVER_BLOG_ID}"
            await page.goto(write_url, wait_until="load", timeout=60000)
            await asyncio.sleep(6)

            if "login" in page.url or "nid.naver" in page.url:
                print("❌ 로그인 세션이 만료됐습니다. blog_login_save.py 를 다시 실행해주세요.")
                await browser.close()
                return False
            print(f"✔ 페이지 로드: {page.url[:60]}")

            # ── 2. 임시저장 팝업 처리 (이어 쓰기 / 새글 쓰기)
            for _ in range(6):
                dismissed = await page.evaluate("""
                    () => {
                        const kws = ['새글 쓰기', '새글쓰기', '취소', '닫기'];
                        for (const kw of kws) {
                            const b = Array.from(document.querySelectorAll('button'))
                                          .find(b => b.innerText.trim() === kw && b.offsetParent);
                            if (b) { b.click(); return kw; }
                        }
                        return null;
                    }
                """)
                if dismissed:
                    print(f"✔ 임시저장 팝업 닫기: '{dismissed}'")
                    await asyncio.sleep(2)
                    break
                await asyncio.sleep(1)

            # ── 3. 에디터 준비 대기
            await asyncio.sleep(3)

            # ── 공통: 클립보드 후 포커스 복구하는 붙여넣기 헬퍼
            async def paste_text(text):
                """클립보드 설정 → 브라우저 포커스 복구 → Ctrl+V"""
                set_clipboard(text)          # PowerShell로 클립보드 설정
                await asyncio.sleep(0.5)    # PowerShell 완료 대기
                await page.bring_to_front() # 브라우저 창 포커스 복구
                await asyncio.sleep(0.3)
                # 에디터 요소 재포커스
                await page.evaluate("""
                    () => {
                        const el = document.querySelector('[contenteditable="true"]');
                        if (el) el.focus();
                    }
                """)
                await asyncio.sleep(0.3)
                await page.keyboard.press("Control+v")
                await asyncio.sleep(0.5)

            # ── 4. 제목 입력
            print("✏️  제목 입력 중...")
            await page.bring_to_front()
            await page.evaluate("""
                () => {
                    const el = document.querySelector('[contenteditable="true"]');
                    if (el) el.focus();
                }
            """)
            await asyncio.sleep(0.5)
            await page.keyboard.press("Control+Home")   # 제목 위치로 이동
            await asyncio.sleep(0.3)
            await page.keyboard.press("Shift+End")       # 제목 줄 전체 선택
            await asyncio.sleep(0.2)
            await paste_text(content["title"])
            print("   제목 입력 완료")

            # ── 5. 본문 입력
            print("📝 본문 입력 중...")
            await page.bring_to_front()
            await page.evaluate("""
                () => {
                    const el = document.querySelector('[contenteditable="true"]');
                    if (el) el.focus();
                }
            """)
            await asyncio.sleep(0.3)
            await page.keyboard.press("Control+End")     # 본문 끝으로 이동
            await asyncio.sleep(0.3)
            await paste_text(content["body"])
            await asyncio.sleep(1)
            print("   본문 입력 완료")

            # ── 6. 발행 버튼 클릭 (툴바의 "발행" 버튼 — 패널 열기)
            print("🚀 발행 패널 열기...")
            await page.evaluate("""
                () => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    const pub = btns.find(b =>
                        b.innerText.trim() === '발행' && !b.innerText.includes('예약')
                    );
                    if (pub) pub.click();
                }
            """)
            await asyncio.sleep(3)  # 패널 애니메이션 대기

            # ── 7. 발행 패널 스크롤 후 "발행하기" 클릭
            # "발행하기"만 찾음 — 단독 "발행" 버튼은 절대 클릭 안 함
            await page.evaluate("""
                () => {
                    document.querySelectorAll('*').forEach(el => {
                        if (el.scrollHeight > el.clientHeight + 5)
                            el.scrollTop = el.scrollHeight;
                    });
                }
            """)
            await asyncio.sleep(0.5)

            confirm = await page.evaluate("""
                () => {
                    const btns = Array.from(document.querySelectorAll('button'));
                    // "발행" 텍스트 버튼 전체 목록 (예약발행 제외)
                    const pubBtns = btns.filter(b =>
                        b.innerText.trim() === '발행' && !b.innerText.includes('예약') && b.offsetParent
                    );
                    if (pubBtns.length >= 2) {
                        // 두 개 이상이면 마지막이 패널 버튼
                        pubBtns[pubBtns.length - 1].click();
                        return '클릭(패널): 발행 (' + pubBtns.length + '개 중 마지막)';
                    } else if (pubBtns.length === 1) {
                        pubBtns[0].click();
                        return '클릭(유일): 발행';
                    }
                    return '없음';
                }
            """)
            print(f"   발행 확인 → {confirm}")

            await asyncio.sleep(3)
            print(f"\n✅ 게시 완료!")
            print(f"   제목: {content['title']}")
            print(f"   시간: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            print(f"   블로그: https://blog.naver.com/{NAVER_BLOG_ID}")
            await browser.close()
            return True

        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")
            try:
                await page.screenshot(path="debug_error.png",
                                      timeout=8000, full_page=False)
                print("오류 스크린샷: debug_error.png")
            except Exception:
                pass
            await asyncio.sleep(3)
            await browser.close()
            return False


async def main():
    print("=" * 55)
    print("  F45 가산 네이버 블로그 자동 게시 시작")
    print("=" * 55)

    content = generate_content()
    print(f"\n📋 선택된 주제: {content['title']}")

    photo_path = download_photo(content["photo_keyword"])

    success = await post_to_naver_blog(content, photo_path)

    if photo_path and os.path.exists(photo_path):
        os.remove(photo_path)

    if success:
        print("\n🎉 완료! 네이버 블로그를 확인해보세요.")
        print(f"   https://blog.naver.com/{NAVER_BLOG_ID}")
    else:
        print("\n⚠️ 실패했습니다.")
        print("   생성된 debug_*.png 스크린샷을 확인해 어느 단계에서 막혔는지 보내주세요.")


if __name__ == "__main__":
    asyncio.run(main())
