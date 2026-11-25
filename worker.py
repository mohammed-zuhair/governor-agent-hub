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
    system_prompt = "أنت مهندس برمجي ومسؤول تعافي وتكيف تلقائي عالي الخبرة. تقوم بتعديل وإصلاح الكود بذكاء اصطناعي كامل."
    user_prompt = f"""
قم بإصلاح وتعديل ملف الويب التالي بشكل كامل وذكائي دون إتلاف التنسيق:

📄 الملف المستهدف: {file_path}
🚨 خطأ التدقيق المرصود: {json.dumps(error_info, ensure_ascii=False)}
📜 دستور الحوكمة والقواعد: {json.dumps(rules, ensure_ascii=False)}

💻 كود الملف الحالي:
```html
{content}
```

📋 المطلوب منك كوكيل ذكاء اصطناعي مستقِل:
1. قم بإصلاح السبب الجذري للخطأ (Missing image, JS error, broken link, structural unclosed tag).
2. إذا كان الخطأ بسيطاً، قم بإعادة كتابته جراحياً بشكل صحيح.
3. إذا كان الخطأ غير مضمون، حوطه بـ try...catch أو إدراج fallback ديناميكي آمن (مثل https://placehold.co/600x400?text=Missing+File).
4. أرجع الكود المكتمل النهائي فقط دون أي مقدمات أو شروحات جانبية.
"""
    print(f"🧠 [AI Worker] جاري التحليل والتعافي بواسطة الذكاء الاصطناعي...")
    repaired_code, provider = call_ai(user_prompt, system_prompt)
    
    if repaired_code:
        if "```" in repaired_code:
            lines = repaired_code.splitlines()
            filtered = [l for l in lines if not l.strip().startswith("```")]
            repaired_code = "\n".join(filtered)
        print(f"✨ [AI Worker] تم التعافي الذاتي بنجاح عبر ({provider}) للملف: {file_path}")
        return repaired_code.strip(), True
    else:
        print(f"⚠️ [AI Worker] تنفيذ تعافي طوارئ احتياطي...")
        modified = False
        img_pattern = r'(<img\s+[^>]*src=["']([^"']+)["'][^>]*>)'
        for full_tag, src in re.findall(img_pattern, content):
            if not src.startswith(("http://", "https://", "data:")) and not os.path.exists(src):
                fname = os.path.basename(src)
                new_tag = full_tag.replace(src, f"https://placehold.co/600x400?text=Missing:+{fname}")
                content = content.replace(full_tag, new_tag)
                modified = True
        if "<html" in content and "</html>" not in content:
            content += "\n</html>"
            modified = True
        return content, modified

def run_worker():
    print("🐝 [Full AI Worker] بدء جولة صيانة السرب الذكي...")
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

