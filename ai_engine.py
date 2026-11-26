import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Google Gemini ---
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if gemini_key:
        try:
            clean_key = gemini_key.strip().strip('"').strip("'")
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={clean_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
            }
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                text = res.json()['candidates'][0]['content']['parts'][0]['text']
                return text, "Google Gemini"
            else:
                errors.append(f"Gemini [{res.status_code}]: {res.text[:150]}")
        except Exception as e:
            errors.append(f"Gemini Exc: {str(e)}")
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
                errors.append(f"Groq [{res.status_code}]: {res.text[:150]}")
        except Exception as e:
            errors.append(f"Groq Exc: {str(e)}")
    else:
        errors.append("Groq: المفتاح مفقود")

    return None, "\n".join(errors)
