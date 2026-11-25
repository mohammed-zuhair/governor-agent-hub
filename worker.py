import os
import json
import re

MEMORY_FILE = "memory.json"
RULES_FILE = "rules.json"

def load_json(filepath, default):
    """تحميل ملفات JSON بأمان تام مع حماية من الأخطاء"""
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ [Worker Load Error] تعذر قراءة {filepath}: {e}")
            return default
    return default

def ai_repair_code(file_path, content, error_info, rules):
    """🧠 محرك الذكاء الاصطناعي للإصلاح والتكيف الذكي"""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ℹ️ [AI Worker] لم يتم العثور على GEMINI_API_KEY، استخدام المهارات النمطية الاحتياطية.")
        return None, False

    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        prompt = f"""
أنت وكيل برمجي خبير ومسؤول عن التعافي الذاتي للويب.
قم بتحليل الملف التالي والخطأ المرتبط به، واختيار أفضل استراتيجية للإصلاح:

📄 **مسار الملف**: {file_path}
🚨 **الأخطاء المرصودة**: {json.dumps(error_info, ensure_ascii=False)}
📜 **قواعد النظام**: {json.dumps(rules, ensure_ascii=False)}

💻 **كود الملف الحالي**:
```html
{content}
```

📋 **التعليمات**:
1. إذا كان الخطأ بسيطاً ومحدداً، قم بإصلاحه جراحياً مباشرة.
2. إذا كان الخطأ رئيساً أو غير آمن للتعديل المباشر، قم بتحصين الكود المعطوب بـ try...catch أو إدراج fallback آمن.
3. أرجع الكود المكتمل المعدل فقط دون أي نصوص شارحة خارج الكود.
"""
        response = model.generate_content(prompt)
        repaired_code = response.text.strip()
        
        # تنظيف وسوم Fences إن وجدت
        if repaired_code.startswith("```html"):
            repaired_code = repaired_code[7:]
        elif repaired_code.startswith("```"):
            repaired_code = repaired_code[3:]
        if repaired_code.endswith("```"):
            repaired_code = repaired_code[:-3]
            
        return repaired_code.strip(), True
    except Exception as e:
        print(f"⚠️ [AI Worker Error] تعذر تنفيذ الإصلاح بالذكاء الاصطناعي: {e}")
        return None, False

def apply_pattern_skills(file_path, content, pattern_rules):
    """🛠️ المهارات النمطية الثابتة الاحتياطية (Images, CSS, JS, HTML)"""
    modified = False

    # 1. 📜 مهارة تحصين أخطاء JS
    if "console.error" in content:
        content = content.replace("console.error", "// [Active Repair] console.error")
        modified = True
        print(f"🛠️ [Pattern Skill] تم تحصين أخطاء JS في: {file_path}")

    # 2. 🖼️ مهارة الصور المفقودة التكيفية
    img_pattern = r'(<img\s+[^>]*src=["']([^"']+)["'][^>]*>)'
    img_matches = re.findall(img_pattern, content)
    for full_img_tag, img_src in img_matches:
        if not img_src.startswith(("http://", "https://", "data:")) and not os.path.exists(img_src):
            file_name = os.path.basename(img_src)
            placeholder_url = f"https://placehold.co/600x400?text=Missing:+{file_name}"
            new_img_tag = full_img_tag.replace(img_src, placeholder_url)
            content = content.replace(full_img_tag, new_img_tag)
            modified = True
            print(f"🖼️ [Pattern Skill] تم استبدال الصورة المفقودة ({file_name}) برابط بديل في: {file_path}")

    # 3. 🎨 مهارة CSS البديل
    link_pattern = r'(<link\s+[^>]*href=["']([^"']+\.css)["'][^>]*>)'
    css_matches = re.findall(link_pattern, content)
    for full_link_tag, css_href in css_matches:
        if not css_href.startswith(("http://", "https://", "//")) and not os.path.exists(css_href):
            fallback_style = f"<!-- [CSS Fallback Applied for {css_href}] -->\n<style>body{{font-family:sans-serif;}}</style>"
            content = content.replace(full_link_tag, fallback_style)
            modified = True
            print(f"🎨 [Pattern Skill] تم تطبيق تنسيق طوارئ لـ CSS المفقود في: {file_path}")

    # 4. 🏷️ مهارة إصلاح وسم HTML
    if "<html" in content and "</html>" not in content:
        content += "\n</html>"
        modified = True
        print(f"🏷️ [Pattern Skill] تم إغلاق وسم </html> المفقود في: {file_path}")

    return content, modified

def repair_file(file_path, error_info, rules):
    """إدارة عملية الإصلاح: البدء بالذكاء الاصطناعي ثم المهارات النمطية احتياطياً"""
    if not os.path.exists(file_path):
        return False
        
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 🧠 المحاولة الأولى: إصلاح الذكاء الاصطناعي
        ai_content, ai_success = ai_repair_code(file_path, content, error_info, rules)
        
        if ai_success and ai_content:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(ai_content)
            print(f"✨ [AI Worker] تم إصلاح الملف بنجاح عبر الذكاء الاصطناعي: {file_path}")
            return True

        # 🛠️ المحاولة الثانية: المهارات النمطية الاحتياطية
        pattern_rules = rules.get("pattern_rules", [])
        updated_content, pattern_success = apply_pattern_skills(file_path, content, pattern_rules)
        
        if pattern_success:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            return True

    except Exception as e:
        print(f"❌ [Worker Repair Error] حدث خطأ أثناء محاولة إصلاح {file_path}: {e}")
        
    return False

def run_worker():
    print("🐝 [Worker] بدء عملية الصيانة والتعافي التكيفي...")
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
            print(f"🛠️ جاري إصلاح وتكييف الملف: {file_path}")
            repair_file(file_path, error_info, rules)
    else:
        print("✨ لا توجد أخطاء تتطلب التدخل.")

if __name__ == "__main__":
    run_worker()

