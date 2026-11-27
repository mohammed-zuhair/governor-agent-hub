import os
import requests
from groq import Groq
import google.generativeai as genai

def call_llm(system_prompt, user_prompt, json_mode=False):
    try:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            model="llama-3.3-70b-versatile",
            **kwargs
        )
        return response.choices[0].message.content, "Groq"
    except Exception as e:
        print(f"Groq failed: {e}")

    try:
        deepseek_key = os.environ.get("DEEPSEEK_API_KEY")
        if deepseek_key:
            headers = {"Authorization": f"Bearer {deepseek_key}", "Content-Type": "application/json"}
            payload = {"model": "deepseek-chat", "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}]}
            if json_mode: payload["response_format"] = {"type": "json_object"}
            res = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload)
            if res.status_code == 200: return res.json()["choices"][0]["message"]["content"], "DeepSeek"
    except Exception as e:
        print(f"DeepSeek error: {e}")

    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        json_instr = "Return ONLY a valid JSON object." if json_mode else ""
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\n{json_instr}"
        response = model.generate_content(full_prompt)
        text = response.text.replace("```json", "").replace("```", "").strip()
        return text, "Gemini"
    except Exception as e:
        print(f"Gemini failed: {e}")
    return None, "Failed"
