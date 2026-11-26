import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Groq (بالمفتاح النظيف) ---
    groq_key = os.environ.get("GROQ_API_KEY", "").strip().strip('"').strip("'")
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
                errors.append(f"Groq HTTP {res.status_code}: {res.text[:100]}")
        except Exception as e:
            errors.append(f"Groq Exception: {e}")
    else:
        errors.append("Groq: المفتاح غير مكتمل أو لا يبدأ بـ gsk_")

    # --- 2. تجربة Google Gemini عبر SDK الرسمي ---
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            full_prompt = f"{system_instruction}\n\n{prompt}" if system_instruction else prompt
            response = model.generate_content(full_prompt)
            if response and response.text:
                return response.text, "Google Gemini (Official SDK)"
        except Exception as e:
            errors.append(f"Gemini SDK Exception: {e}")
    else:
        errors.append("Gemini: المفتاح مفقود")

    return None, "\n".join(errors)
