import yaml

def get_system_prompt():
    with open("prompts.yaml", "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f)

    system_prompt = prompts['expert_assistant']
    return system_prompt