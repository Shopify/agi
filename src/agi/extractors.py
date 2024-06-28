from jinja2 import Environment, FileSystemLoader
import os
import json
from agi.config.settings import settings
from openai import OpenAI


def chat_completion(prompt, temperature=0.7):
    client = OpenAI(base_url=settings.OPENAI_API_BASE, api_key=settings.OPENAI_API_KEY)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=temperature,
        response_format={"type": "json_object"},
        model="gpt-4o"
    )

    return json.loads(chat_completion.choices[0].message.content)


def load_template(template):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env = Environment(loader=FileSystemLoader(script_dir))
    return env.get_template(f"templates/{template}.j2")


def semantic_extractor(input):
    relationship_types = [
        "attribute",
        "type_of",
        "part_of",
        "leads_to",
        "uses",
        "connected_to",
        "related_to",
        "owns",
        "has",
        "can_be",
        "began",
        "finished",
    ]
    template = load_template("semantic_extractor")
    prompt = template.render(input=input, relationship_types=relationship_types)

    return chat_completion(prompt=prompt, temperature=settings.CREATIVITY)


def interaction_classifier(input):
    template = load_template("interaction_classifier")
    prompt = template.render(input=input)

    return chat_completion(prompt=prompt, temperature=0)


def determine_consistency(existing_relationships, new_relationship):
    template = load_template("determine_consistency")
    prompt = template.render(
        existing_relationships=existing_relationships,
        new_relationship=new_relationship
    )

    return chat_completion(prompt=prompt, temperature=0)


def answer_question_with_context(question, concept_map):
    template = load_template("answer_question_with_context")
    prompt = template.render(
        question=question,
        concept_map=concept_map
    )

    return chat_completion(prompt=prompt, temperature=0)


def identify_missing_context(question, concept_map):
    template = load_template("identify_missing_context")
    prompt = template.render(
        question=question,
        concept_map=concept_map
    )

    return chat_completion(prompt=prompt, temperature=0.5)
