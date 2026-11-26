import os
import requests

def load_env_file():
    pass

def get_best_groq_model(api_key):
    """جلب أحدث طراز متاح في Groq تلقائياً"""
    preferred_order = ["llama-3.3-70b-versatile", "deepseek-r1-distill-llama-70b", "llama-3.1-8b-instant"]
    try:
        url = "https://api.groq.com/openai/v1/models"
        headers = {"Authorization": f"Bearer {api_key}"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            available_models = [m.get('id') for m in res.json().get('data', []) if m.get('id')]
            for model in preferred_order:
                if model in available_models:
                    return model
            if available_models:
                return available_models[0]
    except Exception:
        pass
    return preferred_order[0]

def get_best_gemini_model(api_key):
    """جلب أحدث طراز متاح في Gemini ينسجم مع حسابك تلقائياً"""
    preferred_order = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-pro"]
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            models_list = res.json().get('models', [])
            supported = []
            for m in models_list:
                name = m.get('name', '').replace('models/', '')
                methods = m.get('supportedGenerationMethods', [])
                if 'generateContent' in methods:
                    supported.append(name)
            for model in preferred_order:
                if model in supported:
                    return model
            if supported:
                return supported[0]
    except Exception:
        pass
    return preferred_order[0]

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Groq بأحدث طراز متوفر ---
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if groq_key and groq_key.startswith("gsk_"):
        try:
            target_model = get_best_groq_model(groq_key)
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": target_model,
                "messages": [
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": prompt}
                ]
            }
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                text = res.json()['choices'][0]['message']['content']
                return text, f"Groq ({target_model})"
            else:
                errors.append(f"Groq [{target_model}] HTTP {res.status_code}: {res.text[:100]}")
        except Exception as e:
            errors.append(f"Groq Exc: {str(e)}")
    else:
        errors.append("Groq: المفتاح غير صالح أو مفقود")

    # --- 2. تجربة Gemini بأحدث طراز متوفر ---
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key:
        try:
            target_model = get_best_gemini_model(gemini_key)
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{target_model}:generateContent?key={gemini_key}"
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
            }
            res = requests.post(url, json=payload, timeout=30)
            if res.status_code == 200:
                text = res.json()['candidates'][0]['content']['parts'][0]['text']
                return text, f"Google Gemini ({target_model})"
            else:
                errors.append(f"Gemini [{target_model}] HTTP {res.status_code}: {res.text[:100]}")
        except Exception as e:
            errors.append(f"Gemini Exc: {str(e)}")
    else:
        errors.append("Gemini: المفتاح مفقود")

    return None, "\n".join(errors)
