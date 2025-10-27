import requests
from bs4 import BeautifulSoup
from telegram import Bot
from telegram.ext import Updater, CommandHandler
import time

# Telegram Bot Tokenını buraya yapıştır:
TOKEN = "BURAYA_KENDİ_TOKENİNİ_YAZ"
CHAT_ID = "BURAYA_KENDİ_CHAT_ID'İNİ_YAZ"

bot = Bot(token=TOKEN)

def get_news():
    urls = [
        "https://www.ntv.com.tr/son-dakika",
        "https://www.haberler.com/son-dakika/",
        "https://www.sozcu.com.tr/son-dakika/",
        "https://www.sabah.com.tr/son-dakika-haberleri",
        "https://www.aa.com.tr/tr/rss/default?cat=guncel"
    ]
    headlines = []
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")
            for title in soup.find_all(["h2", "h3"]):
                text = title.get_text().strip()
                if len(text) > 20 and text not in headlines:
                    headlines.append(text)
        except:
            continue
    return headlines[:5]

def send_news(context):
    news_list = get_news()
    for news in news_list:
        try:
            bot.send_message(chat_id=CHAT_ID, text=f"🗞 {news}")
            time.sleep(2)
        except:
            continue

def start(update, context):
    update.message.reply_text("🔔 SondakikaTR bot aktif! Son dakika haberleri otomatik gönderilecek.")

updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))

job_queue = updater.job_queue
job_queue.run_repeating(send_news, interval=600, first=10)  # 10 dakikada bir

updater.start_polling()
updater.idle()
