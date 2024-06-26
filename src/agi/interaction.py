from jinja2 import Environment, FileSystemLoader
import os
import json
from agi.config.settings import settings
from openai import OpenAI

class Interaction:
    def __init__(self, message, trust_level=settings.TRUST_LEVEL):
        self.message = message
        self.trust_level = trust_level

    def chat(self, trust_level=0.1):
        pass
        