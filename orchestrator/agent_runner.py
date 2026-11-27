import os
import sys
import yaml
import json
import glob
import requests
from llm_router import call_llm

def send_telegram(msg):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        requests.post(url, json={"chat_id": chat_id, "text": msg}, timeout=10)

def main():
    law_filename = sys.argv[1] if len(sys.argv) > 1 else "law_001_json_syntax.yaml"
    law_path = f"../laws/{law_filename}"
    
    with open(law_path, "r", encoding="utf-8") as f:
        law = yaml.safe_load(f)

    # اختيار الملف المستهدف بناءً على النطاق (Scope) بشكل ذكي
    scope = law.get("scope", "")
    if "json" in scope: 
        target_file = "../state/STATE.json"
    elif "yaml" in scope: 
        target_file = f"../laws/{law_filename}"
    elif "md" in scope: 
        target_file = "../README.md"
    elif "py" in scope:
        py_files = glob.glob("../orchestrator/*.py")
        target_file = py_files[0] if py_files else "../README.md"
    else: 
        target_file = "../README.md"

    with open(target_file, "r", encoding="utf-8") as f:
        file_content = f.read()

    print(f"Agent running Law: {law['name']} on {target_file}...")
    result, provider = call_llm(law["check_logic"], f"File: {target_file}\nContent:\n{file_content}", json_mode=True)

    # حفظ النتيجة في مجلد state
    os.makedirs("../state/results", exist_ok=True)
    result_data = {"law": law['name'], "provider": provider, "result": result}
    
    with open(f"../state/results/{law['id']}.json", "w", encoding="utf-8") as f:
        json.dump(result_data, f, indent=2)

    send_telegram(f"🤖 Agent Report\nLaw: {law['name']}\nProvider: {provider}\nResult:\n{result}")

if __name__ == "__main__":
    main()
