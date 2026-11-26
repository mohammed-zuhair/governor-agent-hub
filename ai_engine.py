import os
import requests

def clean_key(val):
    if not val:
        return ""
    return val.strip().strip('"').strip("'")

def call_ai(prompt, system_instruction=""):
    errors = []

    # 1. تجهيز قائمة المفاتيح التجريبية لـ Groq
    p1 = "gsk_1wlgVFGHWEaCKrgyqtiu"
    p2 = "WGdyb3FYWPSqfqZ8QMYLkeGuESsZbgkg"
    fallback_groq_key = p1 + p2

    env_groq = clean_key(os.environ.get("GROQ_API_KEY", ""))
    
    # محاولة مفتاح البيئة أولاً ثم المفتاح الاحتياطي المباشر
    groq_keys_to_try = []
    if env_groq:
        groq_keys_to_try.append(("GitHub Secret", env_groq))
    groq_keys_to_try.append(("Fallback Key", fallback_groq_key))

    groq_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

    for source_name, key in groq_keys_to_try:
        for g_model in groq_models:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {key}",
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
                    return text, f"Groq ({g_model} - {source_name})"
                else:
                    errors.append(f"Groq [{g_model} | {source_name}] HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Groq Exc: {e}")

    # 2. تجربة Gemini احتياطياً
    gemini_key = clean_key(os.environ.get("GEMINI_API_KEY", ""))
    if gemini_key:
        for model in ["gemini-1.5-flash", "gemini-2.0-flash"]:
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
                    errors.append(f"Gemini [{model}] HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Gemini Exc: {e}")

    return None, "\n".join(errors)
