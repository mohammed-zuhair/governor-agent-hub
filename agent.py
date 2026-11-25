import os
import json
import glob
import asyncio
from datetime import datetime
from playwright.async_api import async_playwright
from ai_engine import call_ai

MEMORY_FILE = "memory.json"
RULES_FILE = "rules.json"
REPORT_FILE = "summary_report.md"

def load_json(filepath, default):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def save_json(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def ai_governor_reasoning(memory, rules):
    history = memory.get("history", [])
    if not history:
        return rules, False
        
    last_run = history[-1]
    system_prompt = "أنت الحاكم التنفيذي للسرب الذاتي (Executive Governor AI). تتخذ قرارات الحوكمة البرمجية والتشريعية."
    user_prompt = f"""
قم بتحليل نتائج التدقيق والتطور التاريخي لعمل السرب، وسَنّ قانون حوكمة جديد لرفع استقرار النظام:

📊 إحصائيات السرب:
- إجمالي عمليات التدقيق: {memory.get('total_audits', 0)}
- حالة الفحص الأخير: {last_run.get('status')}
- تفاصيل الأخطاء المرصودة: {json.dumps(last_run.get('errors', {}), ensure_ascii=False)}
- القواعد النافذة حالياً: {json.dumps(rules.get('global_rules', []), ensure_ascii=False)}

📋 المطلوب:
صاغ قانوناً وقائياً/تطويرياً واحداً باللغة العربية بأسلوب احترافي ودقيق ليتم إضافته إلى دستور السرب (Global Rules).
أرجع نص القانون فقط مباشرة دون أي مقدمات.
"""
    ai_rule, provider = call_ai(user_prompt, system_prompt)
    global_rules = rules.get("global_rules", [])
    
    if ai_rule and len(ai_rule) > 5:
        clean_rule = f"🤖 [{provider} Rule]: {ai_rule.strip()}"
        if clean_rule not in global_rules:
            global_rules.append(clean_rule)
            rules["global_rules"] = global_rules
            print(f"🛡️ [AI Governor - {provider}] تم سن قانون حوكمة جديد: {clean_rule}")
            return rules, True
    return rules, False

def generate_markdown_report(memory, rules):
    history = memory.get("history", [])
    if not history:
        return

    last_run = history[-1]
    status_emoji = "✅ PASS" if last_run.get("status") == "PASS" else "⚠️ FAIL"
    audited_files = last_run.get("audited_files", [])
    errors = last_run.get("errors", {})

    lines = [
        "# 📊 تقرير الفحص والتعافي الذاتي للسرب (Full Cloud AI Swarm Report)",
        "",
        f"**تاريخ الفحص:** `{last_run.get('timestamp')}`  ",
        f"**الحالة العامة:** {status_emoji}  ",
        f"**إجمالي الفحوصات المكتملة:** `{memory.get('total_audits', 0)}`  ",
        f"**بيئة الذكاء الاصطناعي:** `Cloud Multi-Model Swarm Engine`  ",
        "",
        "---",
        "",
        "## 🔎 ملخص تدقيق الملفات (Audited Files)",
        "",
        "| اسم الملف | الحالة | عدد الأخطاء | الصورة التشخيصية |",
        "| :--- | :---: | :---: | :--- |"
    ]

    for file_path in audited_files:
        if file_path in errors:
            err_info = errors[file_path]
            err_count = len(err_info.get("details", []))
            shot = err_info.get("screenshot", "N/A")
            shot_md = f"![Screenshot]({shot})" if shot != "N/A" else "لا توجد"
            lines.append(f"| `{file_path}` | ❌ FAIL | `{err_count}` | {shot_md} |")
        else:
            lines.append(f"| `{file_path}` | ✅ PASS | `0` | - |")

    lines.extend(["", "---", "", "## 📜 دستور وقواعد الحاكم الذكي (AI Governor Rules):"])
    for r in rules.get("global_rules", []):
        lines.append(f"- {r}")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📄 [AI Governor] تم توثيق التقرير في: {REPORT_FILE}")

async def audit_page(file_path):
    print(f"🧪 [AI Auditor] جاري تدقيق الصفحة: {file_path}")
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
        
        if errors:
            screenshot_path = f"error_{os.path.basename(file_path)}.png"
            await page.screenshot(path=screenshot_path)
            
        await browser.close()
        
    return errors, screenshot_path

if __name__ == "__main__":
    print("🏛️ [Full AI Governor] بدء جلسة التدقيق والحوكمة بالذكاء الاصطناعي...")
    rules = load_json(RULES_FILE, {"global_rules": [], "pattern_rules": []})
    memory = load_json(MEMORY_FILE, {"last_run": None, "total_audits": 0, "history": [], "known_issues": []})
    
    html_files = glob.glob("**/*.html", recursive=True)
    all_errors = {}
    
    for file_path in html_files:
        errors, screenshot = asyncio.run(audit_page(file_path))
        if errors:
            all_errors[file_path] = {"details": errors, "screenshot": screenshot}

    is_success = len(all_errors) == 0
    memory["total_audits"] += 1
    memory["last_run"] = datetime.utcnow().isoformat()
    memory["history"].append({
        "timestamp": memory["last_run"],
        "status": "PASS" if is_success else "FAIL",
        "audited_files": html_files,
        "errors": all_errors
    })
    
    rules, updated = ai_governor_reasoning(memory, rules)
    if updated:
        save_json(RULES_FILE, rules)
        
    save_json(MEMORY_FILE, memory)
    generate_markdown_report(memory, rules)

