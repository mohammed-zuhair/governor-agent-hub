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
    return {}

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

async def audit_page(file_path):
    print(f"🧪 [وكيل الفحص] بدء فحص الملف: {file_path}")
    errors = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        
        full_path = os.path.abspath(file_path)
        await page.goto(f"file://{full_path}")
        await page.wait_for_timeout(1000)
        
        await browser.close()
        
    return errors

if __name__ == "__main__":
    print("🏛️ تشغيل الحاكم التنفيذي (Executive Governor)...")
    
    # 1. قراءة الدستور والذاكرة 📜🧠
    rules = load_rules()
    memory = load_memory()
    
    global_rules = rules.get("global_rules", [])
    print(f"📜 تم تحميل {len(global_rules)} قوانين من rules.json")
    
    # 2. اكتشاف جميع صفحات HTML وتكليف الوكلاء بفحصها 📂🐝
    html_files = glob.glob("**/*.html", recursive=True)
    print(f"🔎 تم اكتشاف {len(html_files)} ملفات HTML لفحصها بواسطة السرب.")
    
    all_errors = {}
    total_errors_count = 0
    
    for file_path in html_files:
        errors = asyncio.run(audit_page(file_path))
        if errors:
    screenshot_path = f"error_{os.path.basename(file_path)}.png"
    await page.screenshot(path=screenshot_path)
    all_errors[file_path] = {
        "details": errors,
        "screenshot": screenshot_path
    }

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
    
    # 4. تفعيل التطور الذاتي للقوانين 🔄
    rules, rules_updated = evaluate_and_evolve_rules(memory, rules)
    if rules_updated:
        save_rules(rules)
        print("💾 تم حفظ القواعد الجديدة في rules.json!")
    
        # 5. حفظ الذاكرة المحدثة 💾
    save_memory(memory)
    
    if is_success:
        print(f"✅ الفحص التوسعي اكتمل بنجاح تحت إشراف الحاكم! إجمالي الفحوصات: {memory['total_audits']}")
    else:
        print(f"⚠️ تم رصد أخطاء وتسجيلها في الذاكرة وسَنّ قوانين وقائية: {all_errors}")


    
