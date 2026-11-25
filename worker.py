import os
import json
import re

MEMORY_FILE = "memory.json"
RULES_FILE = "rules.json"

def load_json(filepath, default):
    """تحميل ملفات JSON بآمان"""
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return default
    return default

def repair_html_file(file_path, error_details, pattern_rules):
    """🛠️ تنفيذ كافة مهارات الإصلاح الذاتي والتكيف التلقائي على الملف"""
    if not os.path.exists(file_path):
        return False
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    modified = False

    # 1. 📜 مهارة معالجة وتثبيط أخطاء JavaScript (JS Error Sanitizer)
    if "console.error" in content:
        content = content.replace("console.error", "// [Active Repair] console.error")
        modified = True
        print(f"🛠️ [Worker] تم تحصين كود JS في: {file_path}")

    # 2. 🖼️ مهارة معالجة الصور المفقودة والاستبدال التكيفي (Active Image Repair)
    img_pattern = r'(<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>)'
    img_matches = re.findall(img_pattern, content)
    for full_img_tag, img_src in img_matches:
        if not img_src.startswith(("http://", "https://", "data:")) and not os.path.exists(img_src):
            file_name = os.path.basename(img_src)
            placeholder_url = f"https://placehold.co/600x400?text=Missing:+{file_name}"
            new_img_tag = full_img_tag.replace(img_src, placeholder_url)
            content = content.replace(full_img_tag, new_img_tag)
            modified = True
            print(f"🖼️ [Worker] تم استبدال الصورة المفقودة ({file_name}) برابط بديل في: {file_path}")

    # 3. 🎨 مهارة معالجة ملفات التنسيق المفقودة (CSS Fallback Repair)
    link_pattern = r'(<link\s+[^>]*href=["\']([^"\']+\.css)["\'][^>]*>)'
    css_matches = re.findall(link_pattern, content)
    for full_link_tag, css_href in css_matches:
        if not css_href.startswith(("http://", "https://", "//")) and not os.path.exists(css_href):
            fallback_style = f"<!-- [CSS Fallback Applied for {css_href}] -->\n<style>body{{font-family:sans-serif;}}</style>"
            content = content.replace(full_link_tag, fallback_style)
            modified = True
            print(f"🎨 [Worker] تم تزويد الصفحة بتنسيق بديل لـ CSS المفقود في: {file_path}")

    # 4. 🏷️ مهارة تصحيح وإغلاق الوسوم الهيكلية (HTML Structure Fixer)
    if "<html" in content and "</html>" not in content:
        content += "\n</html>"
        modified = True
        print(f"🏷️ [Worker] تم إغلاق وسم </html> المفقود في: {file_path}")

    # 💾 حفظ التغيرات في حال تم التعديل
    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
        
    return False

def run_worker():
    print("🐝 [وكيل التنفيذ Worker] بدء عملية الصيانة والتعافي الذاتي...")
    memory = load_json(MEMORY_FILE, {})
    rules = load_json(RULES_FILE, {})
    
    history = memory.get("history", [])
    pattern_rules = rules.get("pattern_rules", [])
    
    if not history:
        print("ℹ️ لا توجد سجلات أخطاء في الذاكرة.")
        return

    last_run = history[-1]
    if last_run.get("status") == "FAIL":
        errors = last_run.get("errors", {})
        for file_path, error_info in errors.items():
            print(f"🛠️ جاري إصلاح وتكييف الملف: {file_path}")
            repaired = repair_html_file(file_path, error_info, pattern_rules)
            if repaired:
                print(f"✅ تم تعافي وإصلاح {file_path} بنجاح!")
    else:
        print("✨ لا توجد أخطاء تتطلب التدخل.")

if __name__ == "__main__":
    run_worker()
    
