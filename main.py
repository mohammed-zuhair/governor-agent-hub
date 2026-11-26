import os
import subprocess
from ai_engine import call_ai
from notifier import send_telegram_message

def run_swarm():
    print("🚀 بدء تشغيل السرب الذاتي...")
    
    task_prompt = "قم بفحص وتطوير مشروع governor-agent-hub وزيادة استقراره."
    if os.path.exists("roadmap.md"):
        with open("roadmap.md", "r", encoding="utf-8") as f:
            task_prompt = f.read()

    print("🧠 جاري معالجة المهمة عبر الذكاء الاصطناعي...")
    report, provider = call_ai(task_prompt, "أنت المعمار والمنفذ البرمجي للسرب. قدم تحليلاً استراتيجياً مفصلاً.")
    
    if not report:
        send_telegram_message("⚠️ *تنبيه السرب:* فشل الاتصال بواجهات API. يُرجى التأكد من نسخ قيمة الـ API Key بشكل صحيح دون مسافات إضافية في GitHub Secrets.")
        return

    # كتابة التقرير
    with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
        f.write(f"# 🚀 تقرير التطور الذاتي للسرب ({provider})\n\n{report}")
    
    # إرسال التقرير لـ Telegram
    send_telegram_message(f"🧠 *تقرير وكيل الذكاء الاصطناعي [{provider}]:*\n\n{report[:600]}\n\n... 📄 التقرير الكامل تم حفظه في EVOLUTION_PLAN.md")

    # رفع التقرير سحابياً إلى المستودع
    try:
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=False)
        subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=False)
        subprocess.run(['git', 'add', 'EVOLUTION_PLAN.md'], check=False)
        subprocess.run(['git', 'commit', '-m', '🤖 Auto-generate EVOLUTION_PLAN.md [skip ci]'], check=False)
        subprocess.run(['git', 'push', 'origin', 'main'], check=False)
    except Exception as e:
        print(f"تخطي الرفع التلقائي: {e}")

if __name__ == "__main__":
    run_swarm()
