import os
import json
import urllib.request
from ai_engine import load_env_file

load_env_file()

def send_telegram_message(message):
    """إرسال إشعارات حية ومباشرة إلى Telegram Bot عند حدوث فحص أو تعافي"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        print("ℹ️ [Notifier] لم يتم ضبط TELEGRAM_BOT_TOKEN أو TELEGRAM_CHAT_ID (الإشعارات معطلة).")
        return False
        
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception as e:
        print(f"⚠️ [Notifier Error] تعذر إرسال إشعار Telegram: {e}")
        return False
