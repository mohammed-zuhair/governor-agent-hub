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
    report, provider = call_ai(task_prompt, "أنت المعمار والمنفذ البرمجي للسرب. قدم تحليلاً استراتيجياً وتقرير تنفيذ مفصل.")
    
    # في حال فشل الاستجابة، يرسل تنبيهاً صريحاً لـ Telegram
    if not report:
        print("⚠️ تعثر الحصول على استجابة من الذكاء الاصطناعي.")
        send_telegram_message("⚠️ *تنبيه السرب:* تعذر التنسيق مع نماذج الذكاء الاصطناعي. يُرجى التحقق من مفاتيح API في GitHub Secrets.")
        return

    # 1. كتابة التقرير
    with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
        f.write(f"# 🚀 تقرير التطور الذاتي للسرب ({provider})\n\n{report}")
    print(f"✅ تم حفظ التقرير بنجاح عبر [{provider}]")

    # 2. إرسال النتيجة فوراً لـ Telegram
    telegram_msg = f"🧠 *تقرير وكيل الذكاء الاصطناعي [{provider}]:*\n\n{report[:600]}\n\n... 📄 التقرير الكامل تم حفظه في EVOLUTION_PLAN.md"
    send_telegram_message(telegram_msg)

    # 3. أمر الرفع الآلي السحابي لـ GitHub من داخل Actions
    try:
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=False)
        subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=False)
        subprocess.run(['git', 'add', 'EVOLUTION_PLAN.md'], check=False)
        subprocess.run(['git', 'commit', '-m', '🤖 Auto-generate EVOLUTION_PLAN.md [skip ci]'], check=False)
        subprocess.run(['git', 'push', 'origin', 'main'], check=False)
        print("✅ تم رفع ملف EVOLUTION_PLAN.md إلى المستودع سحابياً!")
    except Exception as e:
        print(f"تخطي الرفع التلقائي: {e}")

if __name__ == "__main__":
    run_swarm()
