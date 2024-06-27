import os

class Settings:
    def __init__(self):
        self.OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        self.NEO4J_URI = os.getenv("NEO4J_URI")
        self.NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
        self.NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
        self.TRUST = float(os.getenv("TRUST", 0.5))
        self.GULLIBLITY = float(os.getenv("GULLIBLITY", 0.3))
        self.CREATIVITY = float(os.getenv("CREATIVITY", 0.3))
        self.SUSCEPTIBILITY = float(os.getenv("SUSCEPTIBILITY", 0.3))

settings = Settings()

