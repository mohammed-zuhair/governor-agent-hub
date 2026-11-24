import os
import json
import re

MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def repair_html_file(file_path, error_details):
    if not os.path.exists(file_path):
        return False
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    modified = False
    
    # 🛠️ 1. مهارة إصلاح السكربتات والتنظيف الوقائي (JS Error)
    if "console.error" in content:
        content = content.replace("console.error", "// console.error")
        modified = True
        print(f"🛠️ [Worker] تم تحويل السكربت المسبب للخطأ إلى تعليق في: {file_path}")

    # 🔗 2. مهارة معالجة الصور المفقودة (Asset Resolver)
    img_pattern = r'(<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>)'
    img_matches = re.findall(img_pattern, content)
    for full_img_tag, img_src in img_matches:
        if not img_src.startswith(("http://", "https://", "data:")) and not os.path.exists(img_src):
            commented_tag = f"<!-- {full_img_tag} (تعطيل وقائي: الصورة مفقودة) -->"
            content = content.replace(full_img_tag, commented_tag)
            modified = True
            print(f"🛠️ [Worker] تم تعليق وسم الصورة المفقودة في: {file_path}")

    # 🎨 3. مهارة معالجة ملفات التنسيق المفقودة (CSS Resolver)
    link_pattern = r'(<link\s+[^>]*href=["\']([^"\']+\.css)["\'][^>]*>)'
    css_matches = re.findall(link_pattern, content)
    for full_link_tag, css_href in css_matches:
        if not css_href.startswith(("http://", "https://", "//")) and not os.path.exists(css_href):
            commented_link = f"<!-- {full_link_tag} (تعطيل وقائي: ملف CSS مفقود) -->"
            content = content.replace(full_link_tag, commented_link)
            modified = True
            print(f"🛠️ [Worker] تم تعليق رابط CSS المفقود في: {file_path}")

    # 🏷️ 4. مهارة تصحيح إغلاق الوسوم الهيكلية (HTML Structure Fixer)
    if "<html" in content and "</html>" not in content:
        content += "\n</html>"
        modified = True
        print(f"🛠️ [Worker] تم إغلاق وسم </html> المفقود في: {file_path}")

    if modified:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
        
    return False

def run_worker():
    print("🐝 [وكيل التنفيذ Worker] بدء عملية الصيانة والإصلاح الذاتي...")
    memory = load_memory()
    history = memory.get("history", [])
    
    if not history:
        print("ℹ️ لا توجد سجلات أخطاء في الذاكرة.")
        return

    last_run = history[-1]
    if last_run.get("status") == "FAIL":
        errors = last_run.get("errors", {})
        for file_path, error_info in errors.items():
            print(f"🛠️ جاري فحص وإصلاح الملف: {file_path}")
            repaired = repair_html_file(file_path, error_info)
            if repaired:
                print(f"✅ تم إصلاح {file_path} بنجاح!")
    else:
        print("✨ لا توجد أخطاء تتطلب التدخل.")

if __name__ == "__main__":
    run_worker()
