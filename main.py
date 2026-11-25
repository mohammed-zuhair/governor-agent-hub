import subprocess
import json
import os
import sys
import traceback
from datetime import datetime

MEMORY_FILE = "memory.json"
MAX_REPAIR_ATTEMPTS = 3

def safe_load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [Safe Memory] تعذر قراءة الذاكرة بسبب خطأ: {e}")
            return {"last_run": None, "total_audits": 0, "history": [], "known_issues": []}
    return {"last_run": None, "total_audits": 0, "history": [], "known_issues": []}

def log_system_exception(step_name, exception_obj):
    try:
        memory = safe_load_memory()
        error_details = {
            "step": step_name,
            "error_message": str(exception_obj),
            "traceback": traceback.format_exc(),
            "timestamp": datetime.utcnow().isoformat()
        }
        known_issues = memory.get("known_issues", [])
        known_issues.append(error_details)
        memory["known_issues"] = known_issues
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(memory, f, ensure_ascii=False, indent=2)
        print(f"🧠 [Zero-Crash] تم توثيق الاستثناء ({step_name}) داخل memory.json.")
    except Exception as e:
        print(f"❌ خطأ أثناء كتابة الاستثناء: {e}")

def run_script_safely(script_name):
    print(f"\n🚀 [Pipeline Execution] جاري تشغيل: {script_name}...")
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            encoding="utf-8"
        )
        if result.stdout:
            print(result.stdout)
        if result.returncode != 0:
            print(f"⚠️ [Warning] {script_name} خرج بكود: {result.returncode}")
            if result.stderr:
                print(f"🔍 تفاصيل: {result.stderr}")
            log_system_exception(script_name, result.stderr or "Non-zero exit code")
            return False
        return True
    except Exception as e:
        print(f"🛡️ [Zero-Crash Shield] اعتراض خطأ في {script_name}: {e}")
        log_system_exception(script_name, e)
        return False

def get_last_status():
    memory = safe_load_memory()
    history = memory.get("history", [])
    if history:
        return history[-1].get("status", "UNKNOWN")
    return "UNKNOWN"

def run_closed_loop_swarm():
    print("==================================================")
    print("🤖 [Autonomous AI Swarm] بدء تشغيل السرب الذكي بالكامل")
    print("==================================================")
    
    execute_success = run_script_safely("agent.py")
    status = get_last_status()
    
    attempt = 0
    while (status == "FAIL" or not execute_success) and attempt < MAX_REPAIR_ATTEMPTS:
        attempt += 1
        print(f"\n🔄 [دورة التعافي {attempt}/{MAX_REPAIR_ATTEMPTS}] بدء التعافي بالذكاء الاصطناعي...")
        worker_success = run_script_safely("worker.py")
        execute_success = run_script_safely("agent.py")
        status = get_last_status()

    print("\n==================================================")
    if status == "PASS":
        print(f"✅ [Swarm Success] وصل النظام للاستقرار التام بعد {attempt} محاولات!")
    else:
        print(f"ℹ️ [Swarm Notice] اكتملت دورة التشغيل وتطوير القواعد تلقائياً.")
    print("📄 التقرير النهائي في summary_report.md")
    print("==================================================")

if __name__ == "__main__":
    try:
        run_closed_loop_swarm()
    except Exception as fatal_e:
        print(f"🛡️ [Ultimate Shield] تم حماية التطبيق: {fatal_e}")
        log_system_exception("Main Application", fatal_e)

