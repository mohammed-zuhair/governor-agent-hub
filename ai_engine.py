import os
import requests
import google.generativeai as genai

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    errors = []

    # --- 1. تجربة Google Gemini عبر الاستكشاف الآلي (genai.list_models) ---
    raw_gemini_key = os.environ.get("GEMINI_API_KEY", "")
    gemini_key = raw_gemini_key.strip().strip('"').strip("'")
    if gemini_key:
        try:
            genai.configure(api_key=gemini_key)
            # استعلام مباشر لسيرفرات Google لجلب جميع النماذج المدعومة لمفتاحك
            valid_models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    valid_models.append(m.name)
            
            if valid_models:
                # استخدام أول نموذج فعال مكتشف تلقائياً
                selected_model = valid_models[0]
                model = genai.GenerativeModel(
                    model_name=selected_model,
                    system_instruction=system_instruction if system_instruction else None
                )
                response = model.generate_content(prompt)
                if response and response.text:
                    clean_name = selected_model.replace("models/", "")
                    return response.text, f"Google Gemini ({clean_name})"
            else:
                errors.append("Gemini: لم يتم العثور على نماذج تدعم توليد النصوص لهذا المفتاح")
        except Exception as e:
            errors.append(f"Gemini SDK Exception: {str(e)[:150]}")
    else:
        errors.append("Gemini: المفتاح مفقود في البيئة")

    # --- 2. تجربة Groq مع فحص المفتاح ---
    raw_groq_key = os.environ.get("GROQ_API_KEY", "")
    groq_key = raw_groq_key.strip().strip('"').strip("'")
    if groq_key and groq_key.startswith("gsk_"):
        groq_models = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768"]
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
                res = requests.post(url, json=payload, timeout=25)
                if res.status_code == 200:
                    text = res.json()['choices'][0]['message']['content']
                    return text, f"Groq ({g_model})"
                elif res.status_code == 401:
                    errors.append("Groq HTTP 401: المفتاح مرفوض من Groq (تأكد من إنشاء مفتاح جديد عبر console.groq.com/keys)")
                    break
                else:
                    errors.append(f"Groq [{g_model}] HTTP {res.status_code}")
            except Exception as e:
                errors.append(f"Groq Exception: {str(e)[:100]}")
    else:
        errors.append("Groq: المفتاح مفقود أو لا يبدأ بـ gsk_")

    return None, "\n".join(errors)
