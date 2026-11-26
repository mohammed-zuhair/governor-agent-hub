import os
import json
import re
from ai_engine import call_ai

MEMORY_FILE = "memory.json"
RULES_FILE = "rules.json"

def load_json(filepath, default):
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return default
    return default

def ai_repair_file(file_path, content, error_info, rules):
    ext = os.path.splitext(file_path)[1].lower()
    system_prompt = f"أنت مهندس برمجي خبير ومسؤول تعافي ذاتي متخصص في لغة/تقنية ({ext}). تقوم بإصلاح وتعديل الكود بذكاء اصطناعي كامل."
    
    user_prompt = f"""
قم بإصلاح الملف البرمجي التالي وتعديله بدقة دون إتلاف بنيته:

📄 الملف: {file_path} (نوع التقنية: {ext})
🚨 تفاصيل الخطأ المرصود: {json.dumps(error_info, ensure_ascii=False)}
📜 القواعد النافذة: {json.dumps(rules, ensure_ascii=False)}

💻 الكود الحالي للملف:
```{ext.replace('.', '')}
{content}
```

📋 التعليمات المطلوبة:
1. قم بتشخيص وصيانة السبب الجذري للخطأ البرمجي في ({ext}).
2. أرجع الكود المكتمل السليم والنهائي فقط داخل العلامات دون أي مقدمات أو شروحات جانبية.
"""
    print(f"🧠 [AI Worker] جاري التعافي بالذكاء الاصطناعي للملف ({file_path})...")
    repaired_code, provider = call_ai(user_prompt, system_prompt)
    
    if repaired_code:
        if "```" in repaired_code:
            lines = repaired_code.splitlines()
            filtered = [l for l in lines if not l.strip().startswith("```")]
            repaired_code = "\n".join(filtered)
        print(f"✨ [AI Worker] تم التعافي الذاتي بنجاح عبر ({provider}) للملف: {file_path}")
        return repaired_code.strip(), True
    else:
        print(f"⚠️ [AI Worker] تنفيذ تعافي احتياطي طارئ للملف {file_path}...")
        if ext == ".html":
            img_pattern = r"(<img\s+[^>]*src=[\"']([^\"']+)[\"'][^>]*>)"
            for full_tag, src in re.findall(img_pattern, content):
                if not src.startswith(("http://", "https://", "data:")) and not os.path.exists(src):
                    fname = os.path.basename(src)
                    new_tag = full_tag.replace(src, f"https://placehold.co/600x400?text=Missing:+{fname}")
                    content = content.replace(full_tag, new_tag)
        return content, True

def run_worker():
    print("🐝 [Multi-Stack AI Worker] بدء صيانة مختلف تقنيات المشروع...")
    memory = load_json(MEMORY_FILE, {})
    rules = load_json(RULES_FILE, {})
    
    history = memory.get("history", [])
    if not history:
        print("ℹ️ لا توجد سجلات أخطاء في الذاكرة.")
        return

    last_run = history[-1]
    if last_run.get("status") == "FAIL":
        errors = last_run.get("errors", {})
        for file_path, error_info in errors.items():
            if os.path.exists(file_path):
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                repaired_content, success = ai_repair_file(file_path, content, error_info, rules)
                if success:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(repaired_content)

if __name__ == "__main__":
    run_worker()
    
