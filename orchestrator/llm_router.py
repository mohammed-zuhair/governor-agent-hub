import os
from scalexi_llm import LLMProxy

# تهيئة الوكيل الموحد
llm = LLMProxy()

def call_llm(system_prompt, user_prompt, json_mode=False, model_name="groq/llama-3.3-70b-versatile"):
    """
    دالة موحدة لاستدعاء أي نموذج من أي مزود.
    يمكنك تغيير model_name إلى:
    - "deepseek/deepseek-chat"
    - "google/gemini-1.5-flash"
    - "xai/grok-beta"
    - "groq/llama-3.3-70b-versatile"
    """
    try:
        print(f"Routing to: {model_name}")
        response, exec_time, token_usage, cost = llm.ask_llm(
            model_name=model_name,
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            structured_output=json_mode # تفعيل JSON mode إذا لزم الأمر
        )
        
        # تنظيف المخرجات إذا كانت JSON
        if json_mode:
            response = response.replace("```json", "").replace("```", "").strip()
            
        return response, model_name
    except Exception as e:
        print(f"ScaleXI LLM failed: {e}")
        return None, "Failed"
