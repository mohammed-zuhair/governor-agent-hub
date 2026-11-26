import os
from ai_engine import call_ai
from notifier import send_telegram

def main():
    print("🚀 Swarm Agent Initializing...")
    prompt = "قم بفحص وتحديث مشروع governor-agent-hub وتقديم تقرير عن استقرار المستودع."
    
    response, provider = call_ai(prompt, "أنت المعمار البرمجي الرئيسي للسرب.")
    
    if response:
        with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
            f.write(f"# 🚀 Swarm Evolution Report ({provider})\n\n{response}")
        
        msg = f"✅ *تم تشغيل السرب النظيف بنجاح عبر [{provider}]:*\n\n{response[:500]}...\n\n📄 تم حفظ التقرير في EVOLUTION_PLAN.md"
        send_telegram(msg)
        print("Done!")
    else:
        msg = f"⚠️ *تشخيص السرب:* تعذر الاتصال بالنماذج:\n\n`{provider}`"
        send_telegram(msg)

if __name__ == "__main__":
    main()
