import os
import requests

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
GH_PAT = os.environ.get("GH_PAT")
REPO = os.environ.get("GITHUB_REPOSITORY")

def send_msg(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": text})

def trigger_workflow(workflow_name, inputs=None):
    url = f"https://api.github.com/repos/{REPO}/actions/workflows/{workflow_name}/dispatches"
    headers = {"Authorization": f"Bearer {GH_PAT}", "Accept": "application/vnd.github+json"}
    payload = {"ref": "main"}
    if inputs:
        payload["inputs"] = inputs
    res = requests.post(url, headers=headers, json=payload)
    return res.status_code == 204

def main():
    print("Checking Telegram...")
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=-1"
    res = requests.get(url).json()
    
    if not res.get("ok") or not res.get("result"):
        return

    last_update = res["result"][0]
    
    if "message" in last_update and "text" in last_update["message"]:
        if str(last_update["message"]["chat"]["id"]) != str(CHAT_ID):
            return
            
        text = last_update["message"]["text"].strip()
        print(f"Message: {text}")
        
        if text == "/audit":
            send_msg("🚀 Deploying the Fleet...")
            if trigger_workflow("run-batch.yml"):
                send_msg("✅ Fleet deployed!")
                
        elif text == "/status":
            send_msg("🟢 Bot is online.\nCommands:\n/audit\n/build [idea]")
            
        elif text.startswith("/build "):
            idea = text.replace("/build ", "").strip()
            if not idea:
                send_msg("❌ Please provide an idea. Example: /build color picker")
                return
            send_msg(f"🏭 Building tool: {idea}...")
            if trigger_workflow("build-tool.yml", {"idea": idea}):
                send_msg("✅ Construction started! Check GitHub for the result.")
            else:
                send_msg("❌ Failed to trigger build.")
