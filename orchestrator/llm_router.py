import os
import json
from groq import Groq
import google.generativeai as genai

def call_llm(system_prompt, user_prompt):
    # المحاولة الأولى: Groq
    try:
        print("Attempting Groq (openai/gpt-oss-120b)...")
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="openai/gpt-oss-120b",
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content, "Groq"
    except Exception as e:
        print(f"Groq failed: {e}")
        print("Falling back to Gemini...")

    # المحاولة الثانية: Gemini (Failover)
    try:
        gemini_key = os.environ.get("GEMINI_API_KEY")
        if not gemini_key:
            raise Exception("GEMINI_API_KEY is missing.")
        
        genai.configure(api_key=gemini_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\nReturn ONLY a valid JSON object. No markdown formatting."
        response = model.generate_content(full_prompt)
        
        # تنظيف النص من علامات الماركداون إذا وجدت
        text = response.text.replace("```json", "").replace("```", "").strip()
        return text, "Gemini"
    except Exception as e:
        print(f"Gemini also failed: {e}")
        return None, "Failed"
