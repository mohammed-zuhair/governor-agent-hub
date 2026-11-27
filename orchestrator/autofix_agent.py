import os
from llm_router import call_llm

def main():
    target_file = "../sample_code.py"
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()

    system_prompt = "You are an expert Python developer. The following code has a syntax error. Fix the error and return ONLY the corrected Python code. No explanations, no markdown, just the raw code."
    user_prompt = f"Code:\n{content}"

    print(f"Analyzing {target_file} for auto-fix...")
    fixed_content, provider = call_llm(system_prompt, user_prompt)
    
    if fixed_content:
        # Clean up in case the LLM adds markdown
        fixed_content = fixed_content.replace("```python", "").replace("```", "").strip()
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(fixed_content + "\n")
        print("File updated locally by the agent.")
    else:
        print("Failed to get a fix from the LLM.")

if __name__ == "__main__":
    main()
