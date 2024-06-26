from jinja2 import Environment, FileSystemLoader
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

def extract_concepts(input):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(script_dir))

    dbt_config_template = env.get_template("templates/extract_concepts.j2")
    prompt = dbt_config_template.render(input=input)

    client = OpenAI(
        base_url=os.getenv("OPENAI_API_BASE"),
        api_key=os.getenv("OPENAI_API_KEY")
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        response_format={ "type": "json_object" },
        model="gpt-4o",
    )

    return json.loads(chat_completion.choices[0].message.content)
