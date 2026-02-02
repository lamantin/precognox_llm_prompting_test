import json
from typing import List
from domain.word import Word

class DeckRepository:
    def load(self, path: str) -> List[Word]:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return [Word(**item) for item in data]
