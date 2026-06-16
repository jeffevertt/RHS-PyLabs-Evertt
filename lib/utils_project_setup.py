import os
import sys
import json

def run_lab_init():
    os.makedirs(".vscode", exist_ok=True)
    settings_path = os.path.join(".vscode", "settings.json")
    extensions_path = os.path.join(".vscode", "extensions.json")
    gitignore_path = os.path.join(".vscode", ".gitignore")

    anti_ai_settings = {
        "chat.disableAIFeatures": True,
        "editor.inlineSuggest.enabled": False
    }

    unwanted_extensions = {
        "unwantedRecommendations": [
            "github.copilot",
            "github.copilot-chat",
            "tabnine.tabnine-vscode",
            "amazon.qclient"
        ]
    }

    def write_and_lock(file_path, data, is_json=True):
        # Temporarily remove Read-Only flag if it exists to overwrite changes
        if os.path.exists(file_path):
            if sys.platform == "win32":
                os.system(f'attrib -r "{file_path}"')
            else:
                os.chmod(file_path, 0o644)
                
        # Write the mandatory configurations
        with open(file_path, "w") as f:
            if is_json:
                json.dump(data, f, indent=4)
            else:
                f.write(data)
            
        # Lock the file at the operating system level
        if sys.platform == "win32":
            os.system(f'attrib +r "{file_path}"')
        else:
            os.chmod(file_path, 0o444)

    # Execute the self-healing block for all three files
    write_and_lock(settings_path, anti_ai_settings)
    write_and_lock(extensions_path, unwanted_extensions)

    # Create the nested .gitignore that ignores everything inside this folder
    write_and_lock(gitignore_path, "*\n", is_json=False)