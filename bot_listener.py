import os
import time
import json
import urllib.request
import urllib.parse
from ai_engine import call_ai, load_env_file

load_env_file()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
    try:
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"Error sending message: {e}")

def handle_update(update):
    message = update.get("message", {})
    chat_id = str(message.get("chat", {}).get("id"))
    text = message.get("text", "")

    # التأكد من أن الرسالة قادمة منك فقط للحماية
    if ALLOWED_CHAT_ID and chat_id != str(ALLOWED_CHAT_ID):
        return

    if not text:
        return

    print(f"📩 رسالة جديدة من المستخدم: {text}")

    if text.startswith("/start"):
        send_message(chat_id, "👋 *أهلاً بك في الحاكم التنفيذي للسرب الذاتي!*\nأنا جاهز لتلقي أوامرك وإدارة المشروع.")
    elif text.startswith("/status"):
        if os.path.exists("memory.json"):
            with open("memory.json", "r", encoding="utf-8") as f:
                mem = json.load(f)
            send_message(chat_id, f"📊 *حالة السرب:*\n- إجمالي الفحوصات: `{mem.get('total_audits', 0)}`\n- الفحص الأخير: `{mem.get('last_run')}`")
        else:
            send_message(chat_id, "⚠️ لا توجد ذاكرة مسجلة حتى الآن.")
    else:
        # التحدث مع الذكاء الاصطناعي وإرسال إجابة أو تنفيذ أمر
        send_message(chat_id, "🧠 *جاري التفكير والتنفيذ...*")
        reply, provider = call_ai(text, "أنت مساعد ذكي ومطور برمجيات لسرب أوتوماتيكي.")
        if reply:
            send_message(chat_id, f"🤖 *[{provider}]:*\n{reply}")
        else:
            send_message(chat_id, "⚠️ تعذر معالجة الطلب عبر محركات الذكاء الاصطناعي.")

def start_bot():
    print("🤖 بدء تشغيل بوت التلغرام التفاعلي...")
    offset = None
    while True:
        try:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates?timeout=30"
            if offset:
                url += f"&offset={offset}"
            
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=35) as resp:
                result = json.loads(resp.read().decode('utf-8'))
                for update in result.get("result", []):
                    offset = update["update_id"] + 1
                    handle_update(update)
        except Exception as e:
            print(f"⚠️ خطأ في الاتصال: {e}")
            time.sleep(5)

if __name__ == "__main__":
    start_bot()
  
