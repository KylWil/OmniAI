import asyncio
import typer
from typing_extensions import Annotated, Optional
from pyftg.utils.logging import DEBUG, set_logging
from src.files.session import run_session

app = typer.Typer()

@app.command()
def start(
        a1: Annotated[Optional[str], typer.Option(help="Player 1 AI")] = "OmniAI",
        a2: Annotated[Optional[str], typer.Option(help="Player 2 AI")] = "MctsAi23i",
        savedata: Annotated[Optional[bool], typer.Option(help="Collect and Save Round Data")] = False,
        games: Annotated[Optional[int], typer.Option(help="Number of Rounds")] = 1,
        randomaction: Annotated[Optional[bool], typer.Option(help="Sets a1 to perform randomized actions")] = False,
        learn: Annotated[Optional[bool], typer.Option(help="Trains agent's network")] = False):
    """
    Entry point to launch system. Controls variables through launch parameters.
    """
    asyncio.run(run_session(a1, a2, games, savedata, randomaction, learn))

if __name__ == '__main__':
    set_logging(log_level=DEBUG)
    app()