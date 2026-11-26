import os
import glob
import subprocess
from ai_engine import call_ai
from notifier import send_telegram_message

def collect_project_code():
    """تجميع جميع ملفات المشروع البرمجية وتمريرها مع أرقام الأسطر"""
    files_to_scan = glob.glob("*.py") + glob.glob(".github/workflows/*.yml") + ["requirements.txt"]
    codebase_summary = ""
    
    for filepath in files_to_scan:
        if os.path.exists(filepath):
            codebase_summary += f"\n\n========================================\n"
            codebase_summary += f"📄 FILE: {filepath}\n"
            codebase_summary += f"========================================\n"
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
                for line_num, line in enumerate(lines, 1):
                    codebase_summary += f"{line_num:03d} | {line}"
                    
    return codebase_summary

def run_deepseek_audit():
    print("🔍 جاري تجميع ملفات المشروع وترقيم الأسطر...")
    codebase = collect_project_code()

    system_prompt = (
        "أنت تدقق كود متمارس وخبير بصلابة الأنظمة (DeepSeek Senior Code Auditor).\n"
        "وظيفتك فحص ملفات المشروع المقدمة سطرًا بسطر.\n"
        "المطلوب منك استخراج كافة الأخطاء البرمجية بكل دقة (Syntax errors, Import failures, Logic bugs, Undefined variables, API misconfigurations).\n\n"
        "لكل خطأ تكتشفه، قم بتنسيقه بالشكل التالي:\n"
        "❌ **الملف:** [اسم الملف]\n"
        "📍 **السطر:** [رقم السطر]\n"
        "⚠️ **نوع الخطأ:** [وصف دقيق للخطأ]\n"
        "🛠️ **التصحيح المقترح:** [الكود الصحيح]\n\n"
        "إذا كانت كافة الملفات سليمة 100%، اذكر ذلك صراحة مع تأكيد استقرار المستودع."
    )

    user_prompt = f"إليك كود مشروع governor-agent-hub كاملاً مقسماً بالأرقام والملفات:\n\n{codebase}\n\nقم بإجراء الفحص الشامل وتحديد الأخطاء بالأسطر."

    print("🧠 جاري إرسال الكود الكامل إلى DeepSeek للفحص...")
    report, provider = call_ai(user_prompt, system_prompt)

    if not report:
        send_telegram_message(f"⚠️ *تنبيه:* تعذر إجراء الفحص بواسطة DeepSeek:\n`{provider}`")
        return

    # حفظ التقرير في ملف مستقل
    with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
        f.write(f"# 🕵️ تقرير التدقيق الشامل لـ DeepSeek [{provider}]\n\n{report}")

    # إرسال التقرير إلى Telegram على أجزاء لتفادي تجاوز حد الرسائل
    header = f"🕵️ *تقرير تدقيق DeepSeek الشامل للمشروع [{provider}]:*\n\n"
    full_text = header + report

    chunk_size = 3800
    if len(full_text) > chunk_size:
        chunks = [full_text[i:i + chunk_size] for i in range(0, len(full_text), chunk_size)]
        for idx, chunk in enumerate(chunks, 1):
            send_telegram_message(f"📄 *التقرير - جزء ({idx}/{len(chunks)}):*\n\n{chunk}")
    else:
        send_telegram_message(full_text)

    # الرفع الآلي إلى GitHub
    try:
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=False)
        subprocess.run(['git', 'config', 'user.email', 'github-actions[bot]@users.noreply.github.com'], check=False)
        subprocess.run(['git', 'add', 'EVOLUTION_PLAN.md'], check=False)
        subprocess.run(['git', 'commit', '-m', '🤖 DeepSeek full audit report generated [skip ci]'], check=False)
        subprocess.run(['git', 'push', 'origin', 'main'], check=False)
    except Exception as e:
        print(f"تخطي الرفع التلقائي: {e}")

if __name__ == "__main__":
    run_deepseek_audit()
