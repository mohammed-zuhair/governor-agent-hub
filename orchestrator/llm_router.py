import os
from litellm import completion

def call_llm(system_prompt, user_prompt, json_mode=False, model_name="groq/llama-3.3-70b-versatile"):
    try:
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        kwargs = {}
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
            
        print(f"Calling {model_name}...")
        response = completion(
            model=model_name,
            messages=messages,
            **kwargs
        )
        
        content = response.choices[0].message.content
        if json_mode:
            content = content.replace("```json", "").replace("```", "").strip()
            
        return content, model_name
    except Exception as e:
        print(f"LLM failed for {model_name}: {e}")
        
        # خطة الطوارئ: إذا فشل Groq، انتقل فوراً إلى Gemini
        if "groq" in model_name:
            print("Falling back to Gemini...")
            return call_llm(system_prompt, user_prompt, json_mode, "gemini/gemini-1.5-flash")
            
        return None, "Failed"
