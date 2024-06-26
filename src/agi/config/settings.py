import os
import yaml

class Settings:
    def __init__(self):
        self.OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.NEO4J_URI = os.getenv("NEO4J_URI")
        self.NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
        self.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
        self.RELATIONSHIP_TYPES = self. _get_relationship_types()
        self.TRUST_LEVEL = float(os.getenv("TRUST_LEVEL", 0.5))

    def _get_relationship_types(self):
        base_dir = os.path.dirname(__file__)
        relationship_types_path = os.path.join(base_dir, '..', 'relationship_types.yml')
        with open(relationship_types_path, 'r') as file:
            return yaml.safe_load(file)

settings = Settings()

