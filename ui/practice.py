from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

from ai.github_teacher import evaluate

console = Console()

def run_practice(deck, persona: str):
    for w in deck:
        console.clear()

        title = f"[bold]{w.word}[/bold]"
        subtitle = f"[dim]{w.example_sentence}[/dim]" if getattr(w, "example_sentence", None) else ""
        console.print(Panel.fit(f"{title}\n{subtitle}".strip()))

        answer = Prompt.ask("Your explanation")
        console.print("\n[dim]Evaluating...[/dim]\n")

        try:
            result = evaluate(w.word, w.target_meaning, answer, persona)
            verdict = str(result.get("verdict", "")).upper()

            feedback_lines = result.get("feedback", [])
            if isinstance(feedback_lines, list):
                feedback_text = "\n".join(f"- {x}" for x in feedback_lines)
            else:
                feedback_text = str(feedback_lines)

            improved = result.get("improved_answer", "")
            persona_line = result.get("persona_line") or ""

            body = Text()
            body.append(f"{verdict}\n", style="bold")
            if feedback_text:
                body.append(feedback_text + "\n\n")
            body.append(f"Improved: {improved}")
            if persona_line.strip():
                body.append("\n\n" + persona_line)

            console.print(Panel(body, title="Feedback"))
        except Exception as e:
            console.print(Panel.fit(f"[red]AI error:[/red] {e}\n\nYou can continue anyway.", title="Error"))

        Prompt.ask("Press Enter to continue", default="")
