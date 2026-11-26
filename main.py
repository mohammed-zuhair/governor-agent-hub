import os
import json
from ai_engine import call_ai
from notifier import send_telegram_message

def run_swarm():
    print("🚀 بدء تشغيل السرب الذاتي...")
    
    if os.path.exists("roadmap.md"):
        with open("roadmap.md", "r", encoding="utf-8") as f:
            prompt = f.read()
        
        print("🧠 جاري معالجة المهمة عبر محرك الذكاء الاصطناعي...")
        response, provider = call_ai(prompt, "أنت المعمار الأساسي للسرب الذاتي الذكي. قم بتقديم تحليل استراتيجي عميق يغطي المحاور المطلوبة بدقة.")
        
        if response:
            with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
                f.write(f"# 🚀 تقرير التطور الذاتي الصادر عن السرب ({provider})\n\n" + response)
            
            summary_msg = f"🧠 *تقرير وكيل الذكاء الاصطناعي [{provider}]:*\n\n" + response[:600] + "\n\n... 📄 التقرير الكامل تم حفظه في EVOLUTION_PLAN.md"
            send_telegram_message(summary_msg)
            print(f"✅ تم معالجة المهمة بنجاح عبر [{provider}] وإرسال التقرير لـ Telegram!")
            return

    send_telegram_message("✅ *إشعار السرب:* تم الفحص بنجاح بدون مهام مخطط جديدة.")

if __name__ == "__main__":
    run_swarm()
