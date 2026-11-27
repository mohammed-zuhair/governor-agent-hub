import os
import requests
from groq import Groq
import google.generativeai as genai

def call_llm(system_prompt, user_prompt, json_mode=False):
    # 1. المحاولة الأولى: Groq
    try:
        print("Attempting Groq...")
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
            
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            **kwargs
        )
        return response.choices[0].message.content, "Groq"
    except Exception as e:
        print(f"Groq failed: {e}")
        
    # 2. المحاولة الثانية: DeepSeek (إذا كان المفتاح موجوداً)
    try:
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        if deepseek_key:
            print("Attempting DeepSeek...")
            headers = {"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"}
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            if json_mode:
                payload["response_format"] = {"type": "json_object"}
                
            res = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"], "DeepSeek"
            else:
                print(f"DeepSeek failed: {res.text}")
    except Exception as e:
        print(f"DeepSeek error: {e}")

    # 3. المحاولة الثالثة: Gemini (خط الدفاع الأخير)
    try:
        print("Attempting Gemini...")
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        json_instr = "Return ONLY a valid JSON object. No markdown." if json_mode else ""
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\n{json_instr}"
        
        response = model.generate_content(full_prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return text, "Gemini"
    except Exception as e:
        print(f"Gemini also failed: {e}")
        
    return None, "Failed"
EOFcat > orchestrator/llm_router.py << 'EOF'
import os
import requests
from groq import Groq
import google.generativeai as genai

def call_llm(system_prompt, user_prompt, json_mode=False):
    # 1. المحاولة الأولى: Groq
    try:
        print("Attempting Groq...")
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
            
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            model="llama-3.3-70b-versatile",
            **kwargs
        )
        return response.choices[0].message.content, "Groq"
    except Exception as e:
        print(f"Groq failed: {e}")
        
    # 2. المحاولة الثانية: DeepSeek (إذا كان المفتاح موجوداً)
    try:
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        if deepseek_key:
            print("Attempting DeepSeek...")
            headers = {"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"}
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            }
            if json_mode:
                payload["response_format"] = {"type": "json_object"}
                
            res = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"], "DeepSeek"
            else:
                print(f"DeepSeek failed: {res.text}")
    except Exception as e:
        print(f"DeepSeek error: {e}")

    # 3. المحاولة الثالثة: Gemini (خط الدفاع الأخير)
    try:
        print("Attempting Gemini...")
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        json_instr = "Return ONLY a valid JSON object. No markdown." if json_mode else ""
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\n{json_instr}"
        
        response = model.generate_content(full_prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return text, "Gemini"
    except Exception as e:
        print(f"Gemini also failed: {e}")
        
    return None, "Failed"
