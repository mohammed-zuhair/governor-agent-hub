import os
import requests

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Groq بالمفتاح التأكيدي ---
    raw_groq = os.environ.get("GROQ_API_KEY", "")
    groq_key = raw_groq.strip().strip('"').strip("'")
    if groq_key:
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
                errors.append(f"Groq Exc: {e}")
    else:
        errors.append("Groq Key Missing")

    # --- 2. تجربة Google Gemini احتياطياً ---
    raw_gemini = os.environ.get("GEMINI_API_KEY", "")
    gemini_key = raw_gemini.strip().strip('"').strip("'")
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
            }
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                text = res.json()['candidates'][0]['content']['parts'][0]['text']
                return text, "Google Gemini"
            else:
                errors.append(f"Gemini HTTP {res.status_code}")
        except Exception as e:
            errors.append(f"Gemini Exc: {e}")
    else:
        errors.append("Gemini Key Missing")

    return None, "\n".join(errors)
