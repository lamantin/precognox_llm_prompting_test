from dataclasses import dataclass
from typing import Optional

@dataclass
class Word:
    id: int
    word: str
    target_meaning: str
    example_sentence: Optional[str] = None
