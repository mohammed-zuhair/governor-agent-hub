import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    # --- 1. تجربة Groq بمفتاحك المحدث ---
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if groq_key and groq_key.startswith("gsk_"):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ]
            }
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                text = res.json()['choices'][0]['message']['content']
                return text, "Groq (Llama-3.3)"
            else:
                print(f"Groq HTTP Error: {res.status_code}")
        except Exception as e:
            print(f"Groq Exception: {e}")

    # --- 2. تجربة Google Gemini عبر المكتبة الرسمية ---
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(f"{system_instruction}\n\n{prompt}")
            if response and response.text:
                return response.text, "Google Gemini"
        except Exception as e:
            print(f"Gemini SDK Exception: {e}")

    return None, "تعذر الحصول على استجابة"
