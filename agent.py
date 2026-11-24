import os
import json
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_run": None, "total_audits": 0, "history": [], "known_issues": []}

def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

async def audit_page(file_path):
    print(f"🧪 بدء فحص الملف: {file_path}")
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
    print("🤖 محرك Playwright Audit والذاكرة يعملان الآن...")
    
    # 1. قراءة الذاكرة الحالية 📖
    memory = load_memory()
    
    # 2. تشغيل الفحص 🧪
    errors = asyncio.run(audit_page("index.html"))
    is_success = len(errors) == 0
    
    # 3. تحديث سجلات الذاكرة 📊
    memory["total_audits"] += 1
    memory["last_run"] = datetime.utcnow().isoformat()
    memory["history"].append({
        "timestamp": memory["last_run"],
        "status": "PASS" if is_success else "FAIL",
        "errors": errors
    })
    
    # 4. حفظ الذاكرة المحدثة 💾
    save_memory(memory)
    
    if is_success:
        print(f"✅ الفحص اكتمل بنجاح! إجمالي مرات الفحص: {memory['total_audits']}")
    else:
        print(f"❌ تم اكتشاف أخطاء: {errors}")
        exit(1)
        
