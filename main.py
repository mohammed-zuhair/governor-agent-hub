import os
import json
from ai_engine import call_ai
from notifier import send_telegram_message

def run_triple_agent_swarm():
    print("🚀 بدء تشغيل السرب الثلاثي الموحد (DeepSeek + Groq + Gemini)...")
    task_prompt = "قم بفحص وتطوير مشروع governor-agent-hub وزيادة استقراره."
    if os.path.exists("roadmap.md"):
        with open("roadmap.md", "r", encoding="utf-8") as f:
            task_prompt = f.read()

    print("🧠 [المرحلة 1] DeepSeek يضع المخطط المعماري...")
    plan, provider1 = call_ai(f"المهمة:\n{task_prompt}", "أنت المعمار البرمجي الرئيسي. اكتب خطة تنفيذ برمجية دقيقة.")
    if not plan:
        plan = task_prompt

    print("⚡ [المرحلة 2] Groq يكتب الكود...")
    code_output, provider2 = call_ai(f"المهمة والمخطط:\n{plan}", "أنت المطور السريع. اكتب الأكواد والحلول البرمجية.")

    print("🔍 [المرحلة 3] Gemini يراجع الكود ويعد التقرير...")
    final_report, provider3 = call_ai(f"المخطط:\n{plan}\n\nالكود:\n{code_output}\n\nراجع الكود كاملاً واكتب تقريراً مفصلاً.", "أنت مراجع الجودة والتكامل.")

    if final_report:
        with open("EVOLUTION_PLAN.md", "w", encoding="utf-8") as f:
            f.write(f"# 🤝 تقرير السرب الثلاثي الموحد\n\n- التخطيط: {provider1}\n- التنفيذ: {provider2}\n- المراجعة: {provider3}\n\n## النتيجة:\n{final_report}")

        telegram_msg = f"🤝 *تكامل السرب الثلاثي ({provider1} ➔ {provider2} ➔ {provider3}):*\n\n{final_report[:500]}...\n\n📄 التفاصيل الكاملة في EVOLUTION_PLAN.md"
        send_telegram_message(telegram_msg)
        print("✅ تم بنجاح تشغيل السرب وإرسال التقرير النهائي!")

if __name__ == "__main__":
    run_triple_agent_swarm()
