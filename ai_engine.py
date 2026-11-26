import os
import requests

def load_env_file():
    pass

def call_ai(prompt, system_instruction=""):
    # --- 1. تجربة Groq أولاً ---
    groq_key = os.environ.get("GROQ_API_KEY", "").strip()
    if groq_key and groq_key.startswith("gsk_"):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {groq_key}",
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
                print(f"⚠️ Groq HTTP Error {res.status_code}: {res.text}")
        except Exception as e:
            print(f"⚠️ Groq Exc: {e}")

    # --- 2. تجربة Google Gemini عبر SDK الرسمي ---
    gemini_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            
            models_to_try = ["gemini-1.5-flash", "gemini-2.0-flash-exp", "gemini-1.5-pro"]
            for model_name in models_to_try:
                try:
                    model = genai.GenerativeModel(
                        model_name=model_name,
                        system_instruction=system_instruction if system_instruction else None
                    )
                    response = model.generate_content(prompt)
                    if response and response.text:
                        return response.text, f"Google Gemini ({model_name})"
                except Exception as inner_e:
                    print(f"⚠️ Gemini {model_name} failed: {inner_e}")
        except Exception as e:
            print(f"⚠️ Gemini SDK Exception: {e}")

    return None, "تعذر الحصول على استجابة من Groq أو Gemini"
