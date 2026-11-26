import os
import json
import urllib.request

def load_env_file():
    """تحميل ملف .env محلياً تلقائياً بدون الحاجة لمكتبات خارجية"""
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        os.environ[k.strip()] = v.strip()
        except Exception as e:
            print(f"⚠️ [AI Engine] تعذر تحميل ملف .env: {e}")

load_env_file()

def call_ai(prompt, system_instruction=""):
    """
    محرك الذكاء الاصطناعي السحابي الشامل والتنقل الآلي بين النماذج (Resilient Multi-Model Engine)
    """
    # 1️⃣ Google Gemini API
    gemini_key = os.getenv("GEMINI_API_KEY")
    if gemini_key:
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
            payload = {
                "contents": [{"parts": [{"text": f"{system_instruction}\n\n{prompt}"}]}]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                text = res['candidates'][0]['content']['parts'][0]['text']
                return text.strip(), "Google Gemini"
        except Exception as e:
            print(f"⚠️ [AI Engine] فشل Gemini: {e}")

    # 2️⃣ Groq API (Super Fast Llama 3.3 70B)
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            payload = {
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": system_instruction or "You are an expert autonomous software engineer."},
                    {"role": "user", "content": prompt}
                ]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {groq_key}"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                text = res['choices'][0]['message']['content']
                return text.strip(), "Groq Llama-3.3-70B"
        except Exception as e:
            print(f"⚠️ [AI Engine] فشل Groq: {e}")

    # 3️⃣ DeepSeek API
    deepseek_key = os.getenv("DEEPSEEK_API_KEY")
    if deepseek_key:
        try:
            url = "https://api.deepseek.com/v1/chat/completions"
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_instruction or "You are an expert autonomous software engineer."},
                    {"role": "user", "content": prompt}
                ]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {deepseek_key}"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                text = res['choices'][0]['message']['content']
                return text.strip(), "DeepSeek-V3"
        except Exception as e:
            print(f"⚠️ [AI Engine] فشل DeepSeek: {e}")

    # 4️⃣ OpenAI API
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key:
        try:
            url = "https://api.openai.com/v1/chat/completions"
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": system_instruction or "You are an expert autonomous software engineer."},
                    {"role": "user", "content": prompt}
                ]
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), 
                                         headers={"Content-Type": "application/json", "Authorization": f"Bearer {openai_key}"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                text = res['choices'][0]['message']['content']
                return text.strip(), "OpenAI GPT-4o-mini"
        except Exception as e:
            print(f"⚠️ [AI Engine] فشل OpenAI: {e}")

    return None, "No Active API Provider"
