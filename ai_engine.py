import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Google Gemini (نماذج مستقرة رسمياً) ---
    raw_gemini = os.environ.get("GEMINI_API_KEY", "")
    gemini_key = raw_gemini.strip().strip('"').strip("'")
    if gemini_key:
        models = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
        for model in models:
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
                errors.append(f"Gemini [{model}] Exc: {str(e)[:80]}")
    else:
        errors.append("Gemini: المفتاح مفقود في البيئة")

    # --- 2. تجربة Groq ---
    raw_groq = os.environ.get("GROQ_API_KEY", "")
    groq_key = raw_groq.strip().strip('"').strip("'")
    if groq_key and groq_key.startswith("gsk_"):
        models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "deepseek-r1-distill-llama-70b"]
        for model in models:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                }
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    text = res.json()['choices'][0]['message']['content']
                    return text, f"Groq ({model})"
                else:
                    errors.append(f"Groq [{model}] HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Groq [{model}] Exc: {str(e)[:80]}")
    else:
        errors.append("Groq: المفتاح غير صالح أو مفقود")

    return None, "\n".join(errors)
