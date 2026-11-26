import os
import re
import requests

def load_env_file():
    pass

def clean_api_key(key):
    """تطهير المفتاح كاملاً من أي مسافات مخفية أو رموز Unicode ناتجة عن نسخ الجوال"""
    if not key:
        return ""
    # احتفاظ فقط بالحروف والأرقام والشرطات الصحيحة
    return re.sub(r'[^a-zA-Z0-9_-]', '', key)

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Groq بالمفتاح المطهر ---
    raw_groq = os.environ.get("GROQ_API_KEY", "")
    groq_key = clean_api_key(raw_groq)

    if groq_key and groq_key.startswith("gsk_"):
        groq_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        for g_model in groq_models:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": g_model,
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                }
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    text = res.json()['choices'][0]['message']['content']
                    return text, f"Groq ({g_model})"
                else:
                    errors.append(f"Groq [{g_model}] HTTP {res.status_code}: {res.text[:120]}")
            except Exception as e:
                errors.append(f"Groq Exc: {e}")
    else:
        errors.append(f"Groq Key Invalid (Length: {len(groq_key)})")

    # --- 2. تجربة Google Gemini بالمفتاح المطهر ---
    raw_gemini = os.environ.get("GEMINI_API_KEY", "")
    gemini_key = clean_api_key(raw_gemini)

    if gemini_key:
        gemini_models = ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro"]
        for model in gemini_models:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
                }
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    text = res.json()['candidates'][0]['content']['parts'][0]['text']
                    return text, f"Google Gemini ({model})"
                else:
                    errors.append(f"Gemini [{model}] HTTP {res.status_code}: {res.text[:120]}")
            except Exception as e:
                errors.append(f"Gemini Exc: {e}")
    else:
        errors.append("Gemini Key Missing")

    return None, "\n\n".join(errors)
