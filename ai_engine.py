import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. فحص وقراءة مفتاح Groq ---
    raw_groq = os.environ.get("GROQ_API_KEY", "").strip().strip('"').strip("'")
    key_snippet = raw_groq[:8] + "..." if raw_groq else "مفقود"

    if raw_groq:
        groq_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
        for g_model in groq_models:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {raw_groq}",
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
                    errors.append(f"Groq [{g_model}] HTTP {res.status_code} (المفتاح المقروء: `{key_snippet}`)")
            except Exception as e:
                errors.append(f"Groq Exc: {e}")
    else:
        errors.append("Groq Key Missing")

    # --- 2. تجربة Gemini احتياطياً ---
    raw_gemini = os.environ.get("GEMINI_API_KEY", "").strip().strip('"').strip("'")
    if raw_gemini:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={raw_gemini}"
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
