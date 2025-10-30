import json
from pathlib import Path
import requests

def call_openrouter(prompt: str, model: str, api_key: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]

def load_config():
    return json.loads(Path("config.json").read_text())

def load_policies():
    return Path("sample_policies.txt").read_text()

def main():
    cfg = load_config()
    policies = load_policies()
    prompt = (
        "You are a HIPAA compliance analyzer. "
        "Review the following organization policies and identify possible "
        "violations or missing safeguards under the HIPAA Security Rule. "
        "Return JSON with 'violations' and 'recommendations'.\n\n"
        f"Organization: {cfg['organization']}\n\n"
        f"Policies:\n{policies}"
    )
    response = call_openrouter(prompt, cfg["model"], cfg["openrouter_api_key"])
    Path("report.json").write_text(response)
    print("AI analysis saved to report.json")

if __name__ == "__main__":
    main()
