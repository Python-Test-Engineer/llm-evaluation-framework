"""Based on Kody Simpson Deep Research https://www.youtube.com/watch?v=gFcAfU3V1Zo&t=6182s"""

from random import randint
import asyncio
from dotenv import load_dotenv, find_dotenv
from rich.console import Console
from rich.prompt import Prompt

from coordinator import ResearchCoordinator

load_dotenv(find_dotenv())

console = Console()


async def main() -> None:
    console.print("[bold cyan]Deep Research Tool[/bold cyan] - Console Edition")
    console.print("This tool performs in-depth research on any topic using AI agents.")

    # get the users query
    query = Prompt.ask("\n[bold]What would you like to research?[/bold]")
    report_name = "report_" + query.replace(" ", "_").lower()

    if not query.strip():
        console.print("[bold red]Error:[/bold red] Please provide a valid query.")
        return

    research_coordinator = ResearchCoordinator(query)
    report = await research_coordinator.research()
    if report:
        console.print(
            "\n[bold green]Research Report Generated Successfully![/bold green]"
        )
        console.print(report)
        # EVALS
        rnd = randint(1000, 9999)
        with open(
            f"./src/deep_research/outputs/{report_name}_{rnd}.md", "w", encoding="utf-8"
        ) as file:
            file.write(report)
    else:
        console.print(
            "[bold red]Error:[/bold red] No report generated. Please try again later."
        )


if __name__ == "__main__":
    asyncio.run(main())
