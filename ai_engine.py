import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Google Gemini (سلسلة التبديل التلقائي) ---
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        clean_key = gemini_key.strip().strip('"').strip("'")
        models_to_try = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-1.5-flash"]
        for model_name in models_to_try:
            try:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={clean_key}"
                headers = {"Content-Type": "application/json"}
                payload = {
                    "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
                }
                res = requests.post(url, json=payload, timeout=30)
                if res.status_code == 200:
                    text = res.json()['candidates'][0]['content']['parts'][0]['text']
                    return text, f"Google Gemini ({model_name})"
                else:
                    errors.append(f"Gemini [{model_name}]: HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Gemini [{model_name}] Exc: {str(e)}")
    else:
        errors.append("Gemini: المفتاح مفقود")

    # --- 2. تجربة Groq ---
    groq_key = os.environ.get("GROQ_API_KEY")
    if groq_key:
        try:
            clean_groq = groq_key.strip().strip('"').strip("'")
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {clean_groq}",
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
                errors.append(f"Groq [{res.status_code}]: {res.text[:100]}")
        except Exception as e:
            errors.append(f"Groq Exc: {str(e)}")
    else:
        errors.append("Groq: المفتاح مفقود")

    return None, "\n".join(errors)
