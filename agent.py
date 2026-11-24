import os
import json
import glob
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

MEMORY_FILE = "memory.json"
RULES_FILE = "rules.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_run": None, "total_audits": 0, "history": [], "known_issues": []}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_rules():
    if os.path.exists(RULES_FILE):
        with open(RULES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"global_rules": [], "pattern_rules": []}

def save_rules(data):
    with open(RULES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def evaluate_and_evolve_rules(memory, rules):
    history = memory.get("history", [])
    if not history:
        return rules, False
    
    updated = False
    global_rules = rules.get("global_rules", [])
    
    # ❌ الشرط الأول: التعلم الفوري من الأخطاء
    last_run = history[-1]
    if last_run.get("status") == "FAIL":
        rule = "تلقائي: يجب تطبيق فحص وقائي إضافي عند رصد خطأ في الفحص السابق."
        if rule not in global_rules:
            global_rules.append(rule)
            updated = True
            print("🛡️ الحاكم يسن قانوناً وقائياً لمنع تكرار الخطأ!")

    # 📊 الشرط الثاني: التطوير عند النجاح المستمر (3 فحوصات متتالية)
    recent_status = [h.get("status") for h in history[-3:]]
    if len(recent_status) == 3 and all(s == "PASS" for s in recent_status):
        rule = "تلقائي: استقرار النظام مثبت، يُسمح بتوسيع نطاق السرب وزيادة الفحوصات."
        if rule not in global_rules:
            global_rules.append(rule)
            updated = True
            print("🚀 الحاكم يسن قانوناً لترقية كفاءة ونطاق عمل السرب!")

    rules["global_rules"] = global_rules
    return rules, updated

def update_rules_engine(memory_data, rules_data):
    """📜 محرك القواعد النمطية: يحلل التكرار ويضيف القواعد النمطية مع الحفاظ على القواعد العامة"""
    history = memory_data.get("history", [])
    error_counts = {}

    # 📊 إحصاء تكرار الأنماط عبر السجل التاريخي
    for run in history:
        if run.get("status") == "FAIL":
            for file_path, details in run.get("errors", {}).items():
                err_type = "console_error" if "console_error" in str(details) else "general_error"
                error_counts[err_type] = error_counts.get(err_type, 0) + 1

    pattern_rules = rules_data.get("pattern_rules", [])
    updated = False

    # 📜 صياغة القواعد النمطية عند التكرار (مرتين فأكثر)
    for err_type, count in error_counts.items():
        if count >= 2:
            existing = next((r for r in pattern_rules if r.get("error_type") == err_type), None)
            if not existing:
                pattern_rules.append({
                    "error_type": err_type,
                    "preventative_action": "comment_out",
                    "created_at": datetime.now().strftime("%Y-%m-%d"),
                    "occurrence_count": count
                })
                updated = True
                print(f"📜 [Governor] تم تسجيل قاعدة نمطية جديدة للخطأ: {err_type}")
            else:
                if existing.get("occurrence_count") != count:
                    existing["occurrence_count"] = count
                    updated = True

    rules_data["pattern_rules"] = pattern_rules
    return rules_data, updated

async def audit_page(file_path):
    print(f"🧪 [وكيل الفحص] بدء فحص الملف: {file_path}")
    errors = []
    screenshot_path = None
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        
        full_path = os.path.abspath(file_path)
        await page.goto(f"file://{full_path}")
        await page.wait_for_timeout(1000)
        
        # 📸 الفحص الوقائي: التقاط صورة عند رصد أخطاء
        if errors:
            screenshot_path = f"error_{os.path.basename(file_path)}.png"
            await page.screenshot(path=screenshot_path)
            print(f"📸 تم التقاط صورة تشخيصية: {screenshot_path}")
        
        await browser.close()
        
    return errors, screenshot_path

if __name__ == "__main__":
    print("🏛️ تشغيل الحاكم التنفيذي (Executive Governor)...")
    
    # 1. قراءة الدستور والذاكرة 📜🧠
    rules = load_rules()
    memory = load_memory()
    
    global_rules = rules.get("global_rules", [])
    print(f"📜 تم تحميل {len(global_rules)} قوانين عامة من rules.json")
    
    # 2. اكتشاف جميع صفحات HTML وتكليف الوكلاء بفحصها 📂🐝
    html_files = glob.glob("**/*.html", recursive=True)
    print(f"🔎 تم اكتشاف {len(html_files)} ملفات HTML لفحصها بواسطة السرب.")
    
    all_errors = {}
    total_errors_count = 0
    
    for file_path in html_files:
        errors, screenshot = asyncio.run(audit_page(file_path))
        if errors:
            all_errors[file_path] = {
                "details": errors,
                "screenshot": screenshot
            }
            total_errors_count += len(errors)

    is_success = total_errors_count == 0
    
    # 3. تحديث سجلات الذاكرة 📊
    memory["total_audits"] += 1
    memory["last_run"] = datetime.utcnow().isoformat()
    memory["history"].append({
        "timestamp": memory["last_run"],
        "status": "PASS" if is_success else "FAIL",
        "audited_files": html_files,
        "errors": all_errors,
        "governor_approval": True
    })
    
    # 4. تفعيل التطور الذاتي للقوانين العامة 🔄
    rules, rules_updated = evaluate_and_evolve_rules(memory, rules)
    
    # 5. تفعيل محرك الأنماط المتكررة 📜
    rules, pattern_updated = update_rules_engine(memory, rules)
    
    if rules_updated or pattern_updated:
        save_rules(rules)
        print("💾 تم حفظ القواعد المحدثة (العامة والنمطية) في rules.json!")
    
    # 6. حفظ الذاكرة المحدثة 💾
    save_memory(memory)
    
    if is_success:
        print(f"✅ الفحص التوسعي اكتمل بنجاح تحت إشراف الحاكم! إجمالي الفحوصات: {memory['total_audits']}")
    else:
        print(f"⚠️ تم رصد أخطاء وتسجيلها في الذاكرة وسَنّ قوانين وقائية: {all_errors}")
        
