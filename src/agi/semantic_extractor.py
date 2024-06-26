from jinja2 import Environment, FileSystemLoader
import os
import json
from agi.config.settings import settings
from openai import OpenAI

RELATIONSHIP_TYPES = ["attribute", "type_of", "part_of", "leads_to", "uses", "connected_to", "related_to", "owns", "has", "can_be", "began", "finished"]

def semantic_extractor(input):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(script_dir))

    template = env.get_template("templates/semantic_extractor.j2")
    prompt = template.render(
        input=input,
        relationship_types=RELATIONSHIP_TYPES
    )

    client = OpenAI(
        base_url=settings.OPENAI_API_BASE,
        api_key=settings.OPENAI_API_KEY
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
