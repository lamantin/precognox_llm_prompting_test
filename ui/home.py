from rich.console import Console
from rich.prompt import Prompt
from storage.deck_repository import DeckRepository
from ui.practice import run_practice

console = Console()

def show_home():
    console.clear()
    console.print("[bold cyan]Word Practice App (GitHub Models — o4-mini)[/bold cyan]\n")

    persona = Prompt.ask(
        "Choose persona",
        choices=["neutral", "funny", "professor"],
        default="neutral",
    )

    deck = DeckRepository().load("data/deck.json")
    run_practice(deck, persona)
