import os
import traceback
from notifier import send_telegram_message

def run_swarm():
    print("🚀 بدء تشغيل السرب الذاتي...")
    
    # فحص وجود المفاتيح في بيئة الخادم السحابي
    gemini_k = "موجود ✅" if os.environ.get("GEMINI_API_KEY") else "مفقود ❌"
    groq_k = "موجود ✅" if os.environ.get("GROQ_API_KEY") else "مفقود ❌"
    deepseek_k = "موجود ✅" if os.environ.get("DEEPSEEK_API_KEY") else "مفقود ❌"

    try:
        from ai_engine import call_ai
        
        task_prompt = "قم بفحص وتطوير مشروع governor-agent-hub وزيادة استقراره."
        if os.path.exists("roadmap.md"):
            with open("roadmap.md", "r", encoding="utf-8") as f:
                task_prompt = f.read()

        report, provider = call_ai(task_prompt, "أنت المعمار والمنفذ البرمجي للسرب.")
        
        if not report:
            status_msg = (
                f"⚠️ *تشخيص السرب لمفاتيح API:*\n\n"
                f"• `GEMINI_API_KEY`: {gemini_k}\n"
                f"• `GROQ_API_KEY`: {groq_k}\n"
                f"• `DEEPSEEK_API_KEY`: {deepseek_k}\n\n"
                f"📌 *سبب التوقف:* إذا كان المفتاح مكتوب أمامه (مفقود ❌)، فالاسم المسجل في GitHub Secrets غير مطابق تماماً للحروف المكتوبة أعلاه."
            )
            send_telegram_message(status_msg)
            return

        # حفظ وإرسال التقرير
        with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
            f.write(f"# 🚀 تقرير التطور الذاتي للسرب ({provider})\n\n{report}")
        
        send_telegram_message(f"🧠 *تقرير وكيل الذكاء الاصطناعي [{provider}]:*\n\n{report[:600]}\n\n... 📄 تم حفظ التقرير في EVOLUTION_PLAN.md")

    except Exception as e:
        err_msg = f"💥 *خطأ في تنفيذ المحرك:*\n`{str(e)}`"
        send_telegram_message(err_msg)

if __name__ == "__main__":
    run_swarm()
