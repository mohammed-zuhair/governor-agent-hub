import os
import requests

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Gemini REST API ---
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
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
    else:
        errors.append("Gemini Key Missing")

    # --- 2. تجربة Groq REST API ---
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if groq_key:
        for model in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]:
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
                errors.append(f"Groq Exc: {e}")
    else:
        errors.append("Groq Key Missing")

    return None, "\n".join(errors)
