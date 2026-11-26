import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Google Gemini المباشرة والمضمونة ---
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    if gemini_key:
        models_to_try = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
        for model_name in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={gemini_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
                }
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    text = res.json()['candidates'][0]['content']['parts'][0]['text']
                    return text, f"Google Gemini ({model_name})"
                else:
                    errors.append(f"Gemini [{model_name}] HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Gemini [{model_name}] Exc: {str(e)}")
    else:
        errors.append("Gemini: المفتاح غير متوفر في البيئة")

    # --- 2. تجربة Groq (نماذج المحادثة النصية فقط) ---
    groq_key = os.environ.get("GROQ_API_KEY", "").strip().strip('"').strip("'")
    if groq_key and groq_key.startswith("gsk_"):
        groq_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "deepseek-r1-distill-llama-70b"]
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
                    errors.append(f"Groq [{g_model}] HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Groq [{g_model}] Exc: {str(e)}")
    else:
        errors.append("Groq: المفتاح غير صالح أو مفقود")

    return None, "\n".join(errors)
