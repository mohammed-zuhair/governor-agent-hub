import os
import sys
import yaml
from llm_router import call_llm

def main():
    # 1. Get law file from command line argument
    law_filename = sys.argv[1] if len(sys.argv) > 1 else "law_001_json_syntax.yaml"
    law_path = f"../laws/{law_filename}"
    
    with open(law_path, "r", encoding="utf-8") as f:
        law = yaml.safe_load(f)

    # 2. Determine target file based on scope (simple logic for now)
    if "json" in law["scope"]:
        target_file = "../state/STATE.json"
    elif "yaml" in law["scope"]:
        target_file = f"../laws/{law_filename}"
    elif "md" in law["scope"]:
        target_file = "../README.md"
    else:
        target_file = "../README.md"

    with open(target_file, "r", encoding="utf-8") as f:
        file_content = f.read()

    # 3. Prepare Prompts
    system_prompt = law["check_logic"]
    user_prompt = f"File: {target_file}\nContent:\n{file_content}"

    # 4. Call the Router
    print(f"Agent running Law: {law['name']} on {target_file}...")
    result, provider = call_llm(system_prompt, user_prompt)

    # 5. Print Result
    print(f"\n--- Result for {law['id']} ---")
    print(f"Provider Used: {provider}")
    print(result)

if __name__ == "__main__":
    main()
