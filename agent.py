import os
import json
import glob
import asyncio
import py_compile
import ast
from datetime import datetime
from playwright.async_api import async_playwright
from ai_engine import call_ai
from notifier import send_telegram_message

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

def audit_python_file(file_path):
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
        ast.parse(code, filename=file_path)
    except SyntaxError as se:
        errors.append(f"SyntaxError in {file_path} at line {se.lineno}: {se.msg}")
    except Exception as e:
        errors.append(f"File Error in {file_path}: {str(e)}")
    return errors

def audit_css_file(file_path):
    errors = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        open_braces = content.count("{")
        close_braces = content.count("}")
        if open_braces != close_braces:
            errors.append(f"CSS Syntax Mismatch: {open_braces} '{{' vs {close_braces} '}}'")
    except Exception as e:
        errors.append(f"CSS Read Error: {str(e)}")
    return errors

async def audit_html_file(file_path):
    errors = []
    screenshot_path = None
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        page.on("console", lambda msg: errors.append(f"[Console {msg.type.upper()}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(f"[Page Exception] {str(exc)}"))
        
        full_path = os.path.abspath(file_path)
        await page.goto(f"file://{full_path}")
        await page.wait_for_timeout(1000)
        
        if errors:
            screenshot_path = f"error_{os.path.basename(file_path)}.png"
            await page.screenshot(path=screenshot_path)
            
        await browser.close()
        
    return errors, screenshot_path

def ai_governor_reasoning(memory, rules):
    history = memory.get("history", [])
    if not history:
        return rules, False
        
    last_run = history[-1]
    system_prompt = "أنت الحاكم التنفيذي للسرب الذاتي (Executive Governor AI). تتخذ قرارات الحوكمة لتقنيات متعددة HTML/JS/CSS/Python."
    user_prompt = f"""
قم بتحليل نتائج التدقيق الشامل لتقنيات المشروع، وسَنّ قانون حوكمة جديد لرفع استقرار النظام:

📊 إحصائيات السرب:
- إجمالي عمليات التدقيق: {memory.get('total_audits', 0)}
- حالة الفحص الأخير: {last_run.get('status')}
- الأخطاء المرصودة عبر التقنيات: {json.dumps(last_run.get('errors', {}), ensure_ascii=False)}
- القواعد النافذة: {json.dumps(rules.get('global_rules', []), ensure_ascii=False)}

📋 المطلوب:
صاغ قانوناً وقائياً واحداً باللغة العربية ليتم إضافته إلى دستور السرب (Global Rules). أرجع نص القانون فقط مباشرة دون أي كلام آخر.
"""
    ai_rule, provider = call_ai(user_prompt, system_prompt)
    global_rules = rules.get("global_rules", [])
    
    if ai_rule and len(ai_rule) > 5:
        clean_rule = f"🤖 [{provider} Rule]: {ai_rule.strip()}"
        if clean_rule not in global_rules:
            global_rules.append(clean_rule)
            rules["global_rules"] = global_rules
            print(f"🛡️ [AI Governor - {provider}] تم سن قانون جديد: {clean_rule}")
            send_telegram_message(f"📜 *قانون حوكمة جديد من السرب:*\n{clean_rule}")
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
        "# 📊 تقرير الفحص الشامل للسرب (Multi-Stack Cloud AI Swarm Report)",
        "",
        f"**تاريخ الفحص:** `{last_run.get('timestamp')}`  ",
        f"**الحالة العامة:** {status_emoji}  ",
        f"**إجمالي التدقيقات:** `{memory.get('total_audits', 0)}`  ",
        f"**التقنيات المدعومة:** `HTML5, CSS3, JavaScript, Python 3.10+`  ",
        "",
        "---",
        "",
        "## 🔎 نتائج تدقيق تقنيات المشروع (Multi-Stack Audit)",
        "",
        "| اسم الملف | التقنية | الحالة | عدد الأخطاء |",
        "| :--- | :---: | :---: | :---: |"
    ]

    for file_path in audited_files:
        ext = os.path.splitext(file_path)[1].upper().replace(".", "")
        if file_path in errors:
            err_info = errors[file_path]
            err_count = len(err_info.get("details", []))
            lines.append(f"| `{file_path}` | `{ext}` | ❌ FAIL | `{err_count}` |")
        else:
            lines.append(f"| `{file_path}` | `{ext}` | ✅ PASS | `0` |")

    lines.extend(["", "---", "", "## 📜 دستور وقواعد الحاكم الذكي (AI Governor Rules):"])
    for r in rules.get("global_rules", []):
        lines.append(f"- {r}")

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"📄 [AI Governor] تم توثيق التقرير في: {REPORT_FILE}")

def run_multi_stack_agent():
    print("🏛️ [Multi-Stack AI Governor] بدء التدقيق الشامل لكامل تقنيات المشروع...")
    rules = load_json(RULES_FILE, {"global_rules": [], "pattern_rules": []})
    memory = load_json(MEMORY_FILE, {"last_run": None, "total_audits": 0, "history": [], "known_issues": []})
    
    html_files = glob.glob("**/*.html", recursive=True)
    css_files = glob.glob("**/*.css", recursive=True)
    py_files = [f for f in glob.glob("**/*.py", recursive=True) if not f.startswith("venv") and not f.startswith(".")]
    
    all_audited_files = html_files + css_files + py_files
    all_errors = {}
    
    for file_path in html_files:
        errors, screenshot = asyncio.run(audit_html_file(file_path))
        if errors:
            all_errors[file_path] = {"details": errors, "screenshot": screenshot}
            
    for file_path in css_files:
        errors = audit_css_file(file_path)
        if errors:
            all_errors[file_path] = {"details": errors, "screenshot": None}
            
    for file_path in py_files:
        if file_path in ["main.py", "agent.py", "worker.py", "ai_engine.py", "notifier.py"]:
            continue
        errors = audit_python_file(file_path)
        if errors:
            all_errors[file_path] = {"details": errors, "screenshot": None}

    is_success = len(all_errors) == 0
    memory["total_audits"] += 1
    memory["last_run"] = datetime.utcnow().isoformat()
    memory["history"].append({
        "timestamp": memory["last_run"],
        "status": "PASS" if is_success else "FAIL",
        "audited_files": all_audited_files,
        "errors": all_errors
    })
    
    rules, updated = ai_governor_reasoning(memory, rules)
    if updated:
        save_json(RULES_FILE, rules)
        
    save_json(MEMORY_FILE, memory)
    generate_markdown_report(memory, rules)

if __name__ == "__main__":
    run_multi_stack_agent()
