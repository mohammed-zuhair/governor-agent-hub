import os
import yaml
from llm_router import call_llm

def main():
    # Read the current laws to avoid duplicates
    laws_dir = "../laws"
    existing_laws = [f for f in os.listdir(laws_dir) if f.endswith('.yaml')]
    
    system_prompt = "You are the Chief Legislator of an AI Swarm. We need a new rule to improve the repository's code quality or security. Propose a new law in valid YAML format. It MUST have: id (string like 'law_new'), name (string), trigger (string: 'push' or 'cron'), scope (string like '**/*.py'), check_logic (a prompt for another AI to execute), and severity (string: 'info', 'warning', 'error'). Return ONLY the YAML text."
    user_prompt = f"We currently have these laws: {existing_laws}. Suggest a completely new, useful law."
    
    print("Legislator Agent is thinking of a new law...")
    new_law_yaml, provider = call_llm(system_prompt, user_prompt, json_mode=False)
    
    if new_law_yaml:
        # Clean up markdown
        new_law_yaml = new_law_yaml.replace("```yaml", "").replace("```", "").strip()
        
        # Save the proposed law
        os.makedirs("../laws_proposed", exist_ok=True)
        file_path = "../laws_proposed/law_proposed_by_ai.yaml"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_law_yaml)
        print(f"New law proposed and saved to {file_path} using {provider}.")
    else:
        print("Failed to generate a new law.")

if __name__ == "__main__":
    main()
