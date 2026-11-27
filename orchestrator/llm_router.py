import os
import requests
import json

def call_llm(system_prompt, user_prompt, json_mode=False):
    # 1. المحاولة الأولى: Groq مباشرة عبر الرابط
    try:
        print("Attempting Groq (llama-3.1-8b-instant)...", flush=True)
        headers = {
            "Authorization": f"Bearer {os.environ.get('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        if json_mode:
            payload["response_format"] = {"type": "json_object"}

        res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        if res.status_code == 200:
            return res.json()["choices"][0]["message"]["content"], "Groq"
        else:
            print(f"❌ Groq failed: {res.status_code} - {res.text}", flush=True)
    except Exception as e:
        print(f"❌ Groq error: {e}", flush=True)

    # 2. المحاولة الثانية: Gemini مباشرة عبر الرابط
    try:
        print("Attempting Gemini (gemini-1.5-flash)...", flush=True)
        gemini_key = os.environ.get("GEMINI_API_KEY")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={gemini_key}"
        headers = {"Content-Type": "application/json"}
        
        full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
        if json_mode:
            full_prompt += "\n\nReturn ONLY a valid JSON object. No markdown."

        payload = {"contents": [{"parts": [{"text": full_prompt}]}]}
        
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            text = res.json()["candidates"][0]["content"]["parts"][0]["text"]
            text = text.replace("```json", "").replace("```", "").strip()
            return text, "Gemini"
        else:
            print(f"❌ Gemini failed: {res.status_code} - {res.text}", flush=True)
    except Exception as e:
        print(f"❌ Gemini error: {e}", flush=True)

    return None, "Failed"     
