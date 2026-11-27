import os
import json
import datetime

def main():
    results_dir = "../state/results"
    state_file = "../state/STATE.json"
    
    with open(state_file, "r", encoding="utf-8") as f:
        state = json.load(f)
    
    state["last_batch_run"] = datetime.datetime.now().isoformat()
    
    if os.path.exists(results_dir):
        for filename in os.listdir(results_dir):
            if filename.endswith(".json"):
                with open(os.path.join(results_dir, filename), "r", encoding="utf-8") as f:
                    data = json.load(f)
                    law_id = filename.replace(".json", "")
                    state["laws"][law_id] = data
                    
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    print("State aggregated successfully.")

if __name__ == "__main__":
    main()
