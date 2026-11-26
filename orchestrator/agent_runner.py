import os
import yaml
from llm_router import call_llm

def main():
    # 1. Load the Law
    law_path = "laws/law_001_json_syntax.yaml"
    with open(law_path, "r", encoding="utf-8") as f:
        law = yaml.safe_load(f)

    # 2. Read the target file
    target_file = "state/STATE.json"
    with open(target_file, "r", encoding="utf-8") as f:
        file_content = f.read()

    # 3. Prepare Prompts
    system_prompt = law["check_logic"]
    user_prompt = f"File: {target_file}\nContent:\n{file_content}"

    # 4. Call the Router
    print(f"Agent running Law: {law['name']} on {target_file}...")
    result, provider = call_llm(system_prompt, user_prompt)

    # 5. Print Result
    print("\n--- Agent Result ---")
    print(f"Provider Used: {provider}")
    print(result)

if __name__ == "__main__":
    main()
