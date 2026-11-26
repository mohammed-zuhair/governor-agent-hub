import os
import json
import yaml
from groq import Groq

def main():
    # 1. Load API Key from Environment
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY is not set.")
        return

    # 2. Load the Law
    law_path = "laws/law_001_json_syntax.yaml"
    with open(law_path, "r", encoding="utf-8") as f:
        law = yaml.safe_load(f)

    # 3. Read the target file (Testing on STATE.json)
    target_file = "state/STATE.json"
    with open(target_file, "r", encoding="utf-8") as f:
        file_content = f.read()

    # 4. Setup Groq Client
    client = Groq(api_key=api_key)

    # 5. Call the LLM
    print(f"Agent running Law: {law['name']} on {target_file}...")
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": law["check_logic"]},
            {"role": "user", "content": f"File: {target_file}\nContent:\n{file_content}"}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.1,
        response_format={"type": "json_object"} # Force JSON output
    )

    # 6. Print Result
    result = chat_completion.choices[0].message.content
    print("\n--- Agent Result ---")
    print(result)

if __name__ == "__main__":
    main()
