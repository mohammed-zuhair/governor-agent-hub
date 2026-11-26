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

    report, provider = call_ai(task_prompt, "أنت المعمار والمنفذ البرمجي للسرب.")
    
    if not report:
        err_details = provider if provider else "تعذر الاتصال بالسيرفرات"
        send_telegram_message(f"⚠️ *تشخيص خطأ السيرفرات التفصيلي:*\n\n`{err_details}`")
        return

    with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
        f.write(f"# 🚀 تقرير التطور الذاتي للسرب ({provider})\n\n{report}")
    
    send_telegram_message(f"🧠 *تقرير وكيل الذكاء الاصطناعي [{provider}]:*\n\n{report[:600]}\n\n... 📄 تم حفظ التقرير في EVOLUTION_PLAN.md")

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
