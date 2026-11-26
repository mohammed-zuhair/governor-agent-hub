import os
import requests
import google.generativeai as genai

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تشغيل نموذج DeepSeek-R1 عبر Groq API ---
    raw_groq_key = os.environ.get("GROQ_API_KEY", "")
    groq_key = raw_groq_key.strip().strip('"').strip("'")
    if groq_key and groq_key.startswith("gsk_"):
        deepseek_models = ["deepseek-r1-distill-llama-70b", "llama-3.3-70b-versatile"]
        for model_name in deepseek_models:
            try:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": model_name,
                    "messages": [
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": prompt}
                    ]
                }
                res = requests.post(url, json=payload, timeout=60)
                if res.status_code == 200:
                    text = res.json()['choices'][0]['message']['content']
                    return text, f"DeepSeek ({model_name})"
                else:
                    errors.append(f"Groq [{model_name}] HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Groq [{model_name}] Exc: {str(e)[:100]}")

    # --- 2. البديل الاحتياطي: Google Gemini عبر الاستكشاف الآلي ---
    raw_gemini_key = os.environ.get("GEMINI_API_KEY", "")
    gemini_key = raw_gemini_key.strip().strip('"').strip("'")
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            valid_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            if valid_models:
                selected_model = valid_models[0]
                model = genai.GenerativeModel(
                    model_name=selected_model,
                    system_instruction=system_instruction if system_instruction else None
                )
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text, f"Google Gemini ({selected_model.replace('models/', '')})"
        except Exception as e:
            errors.append(f"Gemini Exception: {str(e)[:100]}")

    return None, "\n".join(errors)
