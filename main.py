import requests
from bs4 import BeautifulSoup
from datetime import datetime, date
import time

# === 텔레그램 설정 ===
BOT_TOKEN =  '7653665438:AAF53IH9ihXWXF_oLlAeoE2dqQw0Xn6K0Ns'
CHAT_ID = '7921452950'
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# === 날짜별 카운트 저장용 ===
counted_posts = set()
daily_count = 0
today = date.today()

# === 함수: 텔레그램 알림 보내기 ===
def send_telegram_message(message):
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    requests.post(TELEGRAM_API, data=payload)

# === 함수: 게시글 크롤링 ===
def check_ppomppu():
    global daily_count, today

    now = datetime.now()

    # 밤 11시 ~ 아침 6시는 건너뜀
    if 23 <= now.hour or now.hour < 6:
        print(f"[{now}] 체크 시간 아님. 패스")
        return

    # 날짜 바뀌면 초기화
    if today != now.date():
        today = now.date()
        daily_count = 0
        counted_posts.clear()

    url = "https://m.ppomppu.co.kr/new/bbs_list.php?id=phone"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    titles = soup.select("li.li > a > strong")
    links = soup.select("li.li > a")

    new_count = 0
    for i in range(len(titles)):
        title = titles[i].get_text()
        link = links[i].get("href")

        if "대란" in title and link not in counted_posts:
            counted_posts.add(link)
            daily_count += 1
            new_count += 1

    print(f"[{now}] 새 '대란' 글 {new_count}개 발견 / 오늘 누적: {daily_count}개")

    if daily_count >= 3:
        send_telegram_message(f"[알림] 오늘 '대란' 글이 {daily_count}개 올라왔습니다.")

# === 루프 실행 ===
if __name__ == "__main__":
    while True:
        check_ppomppu()
        time.sleep(3 * 60 * 60)  # 3시간 대기