import os
import sys
import yaml
import requests
from llm_router import call_llm

def send_telegram(msg):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram secrets missing. Skipping notification.")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": msg}
    try:
        requests.post(url, json=payload, timeout=10)
        print("Telegram notification sent!")
    except Exception as e:
        print(f"Failed to send Telegram message: {e}")

def main():
    law_filename = sys.argv[1] if len(sys.argv) > 1 else "law_001_json_syntax.yaml"
    law_path = f"../laws/{law_filename}"
    
    with open(law_path, "r", encoding="utf-8") as f:
        law = yaml.safe_load(f)

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

    system_prompt = law["check_logic"]
    user_prompt = f"File: {target_file}\nContent:\n{file_content}"

    print(f"Agent running Law: {law['name']} on {target_file}...")
    result, provider = call_llm(system_prompt, user_prompt)

    print(f"\n--- Result for {law['id']} ---")
    print(f"Provider Used: {provider}")
    print(result)

    # Send report to Telegram
    telegram_msg = f"🤖 Agent Report\nLaw: {law['name']}\nProvider: {provider}\nResult:\n{result}"
    send_telegram(telegram_msg)

if __name__ == "__main__":
    main()
