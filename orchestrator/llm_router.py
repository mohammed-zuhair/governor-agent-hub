import os
import requests
from groq import Groq
import google.generativeai as genai

def call_llm(system_prompt, user_prompt, json_mode=False):
    # 1. Groq
    try:
        print("Attempting Groq...", flush=True)
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = client.chat.completions.create(
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            model="openai/gpt-oss-120b",
            **kwargs
        )
        return response.choices[0].message.content, "Groq"
    except Exception as e:
        print(f"❌ Groq failed: {e}", flush=True)

    # 2. Gemini
    try:
        print("Attempting Gemini...", flush=True)
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        generation_config = genai.GenerationConfig(
            response_mime_type="application/json" if json_mode else "text/plain"
        )
        
        full_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
        response = model.generate_content(full_prompt, generation_config=generation_config)
        
        text = response.text.replace("```json", "").replace("```", "").strip()
        return text, "Gemini"
    except Exception as e:
        print(f"❌ Gemini failed: {e}", flush=True)
        
    return None, "Failed"
