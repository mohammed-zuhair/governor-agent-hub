import os
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GH_PAT = os.environ.get("GH_PAT")
REPO = os.environ.get("GITHUB_REPOSITORY")

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def trigger_workflow(workflow_name):
    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{workflow_name}/dispatches"
    headers = {"Authorization": f"Bearer {GH_PAT}", "Accept": "application/vnd.github+json"}
    res = requests.post(url, headers=headers, json={"ref": "main"})
    return res.status_code == 204

def main():
    print("Checking Telegram for commands...")
    # offset=-1 ensures we only get the absolute latest message
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1"
    res = requests.get(url).json()
    
    if not res.get("ok") or not res.get("result"):
        print("No new messages found in Telegram API response.")
        return

    last_update = res["result"][0]
    
    if "message" in last_update and "text" in last_update["message"]:
        msg_chat_id = str(last_update["message"]["chat"]["id"])
        if msg_chat_id != str(CHAT_ID):
            print(f"Unauthorized Chat ID: {msg_chat_id}")
            return
            
        text = last_update["message"]["text"].strip()
        print(f"Message received: {text}")
        
        if text == "/audit":
            send_msg("🚀 Command received: Deploying the Fleet...")
            if trigger_workflow("run-batch.yml"):
                send_msg("✅ Fleet deployed successfully! Reports will arrive soon.")
            else:
                send_msg("❌ Failed to deploy fleet. Check GH_PAT secret.")
                
        elif text == "/status":
            send_msg("🟢 Swarm Alert Bot is online and listening.")
            send_msg("Available commands:\n/audit - Run all agents\n/status - Check bot health")
        else:
            print(f"Unknown command: {text}. Ignoring.")
    else:
        print("Latest update does not contain a text message.")

if __name__ == "__main__":
    main()
