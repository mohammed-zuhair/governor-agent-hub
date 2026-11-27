import os
from groq import Groq
import google.generativeai as genai

def call_llm(system_prompt, user_prompt, json_mode=False):
    # المحاولة الأولى: Groq
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
            model="openai/gpt-oss-120b",
            **kwargs
        )
        return response.choices[0].message.content, "Groq"
    except Exception as e:
        print(f"Groq failed: {e}")
        print("Falling back to Gemini...")

    # المحاولة الثانية: Gemini
    try:
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        json_instr = "Return ONLY a valid JSON object. No markdown formatting." if json_mode else "Return ONLY raw code. No markdown formatting."
        full_prompt = f"{system_prompt}\n\n{user_prompt}\n\n{json_instr}"
        
        response = model.generate_content(full_prompt)
        text = response.text.replace("```html", "").replace("```json", "").replace("```", "").strip()
        return text, "Gemini"
    except Exception as e:
        print(f"Gemini also failed: {e}")
        return None, "Failed"
