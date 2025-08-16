# temp_test_base.py
from backend.services.ai.base import AIProvider
class Dummy(AIProvider):
    def generate(self, prompt: str): return "ok"
print(Dummy().generate("test"))