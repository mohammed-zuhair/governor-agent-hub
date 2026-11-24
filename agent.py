import os
import asyncio
from playwright.async_api import async_playwright

async def audit_page(file_path):
    print(f"🧪 بدء فحص الملف: {file_path}")
    errors = []
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # التقاط أخطاء الـ Console والـ JavaScript 🚨
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda exc: errors.append(str(exc)))
        
        full_path = os.path.abspath(file_path)
        await page.goto(f"file://{full_path}")
        await page.wait_for_timeout(1000)
        
        await browser.close()
        
    if errors:
        print(f"❌ تم اكتشاف أخطاء في الصفحة: {errors}")
        return False
    else:
        print("✅ الصفحة سليمة 100% وخالية من الأخطاء!")
        return True

if __name__ == "__main__":
    print("🤖 محرك Playwright Audit يعمل الآن...")
    # تشغيل الفحص التلقائي على الصفحة الرئيسية 🌐
    success = asyncio.run(audit_page("index.html"))
    if not success:
        exit(1)  # إيقاف التمرير في حال وجود خطأ 🚨
