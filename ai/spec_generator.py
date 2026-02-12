import os
import json
import yaml
from openai import OpenAI
from pathlib import Path
# load test.env file variables
from dotenv import load_dotenv

test_env = Path("test.env")
load_dotenv(test_env)

# Safety check (recommended)
if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("OPENAI_API_KEY not found in environment")

SCHEMA = {
    "feature": "STRING",
    "scenario": "STRING",
    "flow": [
        {
            "steps": [
                {
                    "action": "navigate | click | fill | wait",
                    "target": "SEMANTIC_TARGET",
                    "value": "OPTIONAL"
                }
            ]
        },
        {
            "assertions": [
                {
                    "action": "expect",
                    "target": "SEMANTIC_TARGET",
                    "state": "visible | hidden | enabled | disabled",
                    "text": "OPTIONAL | not.empty"
                }
            ]
        }
    ]
}


AVAILABLE_TARGETS = [
    "HOME_PAGE",
    "LOGIN_PAGE",
    "USERNAME_INPUT",
    "PASSWORD_INPUT",
    "LOGIN_BUTTON",
    "FIRST_PRODUCT",
    "PRODUCT_DETAILS",
    "PRODUCT_NAME",
    "PRODUCT_PRICE"
]

client = OpenAI()

FEATURES_FILE = Path("features/features.yaml")
OUTPUT_FILE = Path("features/generated/valid_login.json")


def load_features() -> dict:
    with FEATURES_FILE.open() as f:
        data = yaml.safe_load(f)
    return data["features"]


def generate_spec(features: dict, output_file: Path):

    PROMPT_TEMPLATE = """
You are a senior test automation engineer.

Generate a Playwright automation specification in STRICT JSON.

CRITICAL RULES:
- NEVER generate CSS selectors
- NEVER generate URLs
- ONLY use semantic targets from the allowed list
- Output VALID JSON ONLY

Allowed Semantic Targets:
{targets}

JSON Schema:
{schema}

Application Features:
{features}

Generate ONE realistic user flow test scenario.
"""

    target_text = "\n".join(f"- {t}" for t in AVAILABLE_TARGETS)
    feature_text = json.dumps(features, indent=2)

    prompt = PROMPT_TEMPLATE.format(
        targets=target_text,
        schema=json.dumps(SCHEMA, indent=2),
        features=feature_text
    )

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):
        content = content.strip("`")
        content = content.replace("json", "", 1).strip()

    json.loads(content)

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(content)

    print(f"Spec written to {output_file}")


if __name__ == "__main__":
    features = load_features()
    # generate_spec(features, OUTPUT_FILE)

    for feature_name, feature_info in features.items():
        output_file = Path(f"features/generated/{feature_name.lower()}.json")
        generate_spec({feature_name: feature_info}, output_file)
