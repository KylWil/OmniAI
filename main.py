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
        games: Annotated[Optional[int], typer.Option(help="Number of Rounds")] = 1,
        savedata: Annotated[Optional[bool], typer.Option(help="Collect and Save Round Data")] = False,
        learn: Annotated[Optional[bool], typer.Option(help="Trains agent's network")] = False,
        deterministic: Annotated[Optional[bool], typer.Option(help="Agent uses determined best move")] = False,
        nocuda: Annotated[Optional[bool], typer.Option(help="Disables GPU training")] = False):
    
    """
    Entry point to launch system. Controls variables through launch parameters.
    """

    if learn and deterministic:
        raise ValueError("Cannot run with both the learn and deterministic parameters enabled")
    
    asyncio.run(run_session(a1, a2, games, savedata, learn, deterministic, nocuda))

if __name__ == '__main__':
    set_logging(log_level=DEBUG)
    app()