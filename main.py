import subprocess
import json
import os
import sys
import traceback
from datetime import datetime

MEMORY_FILE = "memory.json"
MAX_REPAIR_ATTEMPTS = 3  # 🛡️ حد أقصى لعدد محاولات الإصلاح في الدورة الواحدة

def safe_load_memory():
    """قراءة الذاكرة بأمان تام مع حماية من أخطاء القراءة"""
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [Safe Memory] تعذر قراءة الذاكرة بسبب خطأ: {e}")
            return {"last_run": None, "total_audits": 0, "history": [], "known_issues": []}
    return {"last_run": None, "total_audits": 0, "history": [], "known_issues": []}

def log_system_exception(step_name, exception_obj):
    """🧠 تسجيل أي استثناء غير متوقع في الذاكرة ليتعلم منه الحاكم لاحقاً"""
    try:
        memory = safe_load_memory()
        error_details = {
            "step": step_name,
            "error_message": str(exception_obj),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # إضافة الخطأ غير المتوقع إلى قائمة الأخطاء المعروفة في الذاكرة
        known_issues = memory.get("known_issues", [])
        known_issues.append(error_details)
        memory["known_issues"] = known_issues
        
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        print(f"🧠 [Zero-Crash] تم توثيق الاستثناء غير المتوقع ({step_name}) داخل memory.json للتعلم منه.")
    except Exception as e:
        print(f"❌ خطأ طارئ أثناء كتابة الاستثناء: {e}")

def run_script_safely(script_name):
    """⚡ تشغيل الوكلاء (agent.py / worker.py) تحت مظلة الحماية الشاملة"""
    print(f"\n🚀 [Pipeline Execution] جاري تشغيل: {script_name}...")
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        
        # طباعة المخرجات العادية
        if result.stdout:
            print(result.stdout)
            
        # التحقق مما إذا خرج السكربت بخطأ غير معالج
        if result.returncode != 0:
            print(f"⚠️ [Warning] {script_name} خرج بكود تنبيه: {result.returncode}")
            if result.stderr:
                print(f"🔍 تفاصيل الخطأ: {result.stderr}")
            log_system_exception(script_name, result.stderr or "Non-zero exit code")
            return False
        return True

    except Exception as e:
        # 🛡️ التقاط أي خطأ نظامي يمنع الانهيار ويضمن استمرار السرب
        print(f"🛡️ [Zero-Crash Shield] تم اعتراض خطأ أثناء تشغيل {script_name}: {e}")
        log_system_exception(script_name, e)
        return False

def get_last_status():
    """قراءة حالة آخر فحص من الذاكرة"""
    memory = safe_load_memory()
    history = memory.get("history", [])
    if history:
        return history[-1].get("status", "UNKNOWN")
    return "UNKNOWN"

def run_closed_loop_swarm():
    print("==================================================")
    print("🤖 [Autonomous Swarm] بدء تشغيل المنظومة ذاتية التعافي والحماية")
    print("==================================================")
    
    # 1️⃣ المرحلة الأولى: الفحص والتدقيق بواسطة الحاكم
    execute_success = run_script_safely("agent.py")
    status = get_last_status()
    
    attempt = 0
    # 2️⃣ حلقة التعافي والتدقيق المرتدة (Self-Healing Loop)
    while (status == "FAIL" or not execute_success) and attempt < MAX_REPAIR_ATTEMPTS:
        attempt += 1
        print(f"\n🔄 [دورة التعافي {attempt}/{MAX_REPAIR_ATTEMPTS}] رصد أخطاء أو عدم استقرار! بدء الإصلاح الذاتي...")
        
        # تشغيل العامل لتنفيذ الإصلاح النشط (Active Repair)
        worker_success = run_script_safely("worker.py")
        
        # إعادة الفحص بواسطة الحاكم لتأكيد التعافي وتحديث التقرير
        execute_success = run_script_safely("agent.py")
        status = get_last_status()

    # 3️⃣ النتيجة النهائية والدعم
    print("\n==================================================")
    if status == "PASS":
        print(f"✅ [Swarm Success] وصل النظام إلى حالة الاستقرار التام بعد {attempt} محاولات!")
    else:
        print(f"ℹ️ [Swarm Notice] اكتملت دورة التشغيل مع حفظ جميع الأنماط والأخطاء في الذاكرة لتطوير القواعد تلقائياً.")
    print("📄 يمكنك الاطلاع على التقرير المحدث دائماً في summary_report.md")
    print("==================================================")

if __name__ == "__main__":
    try:
        run_closed_loop_swarm()
    except Exception as fatal_e:
        print(f"🛡️ [Ultimate Shield] تم حماية التطبيق من الانهيار النهائي: {fatal_e}")
        log_system_exception("Main Application", fatal_e)
  
