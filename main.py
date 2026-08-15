import asyncio
import typer
from typing_extensions import Annotated, Optional
from pyftg.utils.logging import DEBUG, set_logging
from src.files.play import run_fight

app = typer.Typer()


@app.command()
def learn(host: Annotated[Optional[str], typer.Option(help="DareFightingICE Host")] = "127.0.0.1",
        port: Annotated[Optional[int], typer.Option(help="DareFightingICE Port")] = 31415,
        a1: Annotated[Optional[str], typer.Option(help="Player 1 AI")] = None,
        a2: Annotated[Optional[str], typer.Option(help="Player 2 AI")] = None):
    """
    Learning cycle entry. Uses neural network for action and backpropogates error to update policy.
    """
    pass

@app.command()
def play(host: Annotated[Optional[str], typer.Option(help="DareFightingICE Host")] = "127.0.0.1",
        port: Annotated[Optional[int], typer.Option(help="DareFightingICE Port")] = 31415,
        a1: Annotated[Optional[str], typer.Option(help="Player 1 AI")] = None,
        a2: Annotated[Optional[str], typer.Option(help="Player 2 AI")] = None,
        savedata: Annotated[Optional[bool], typer.Option(help="Collect and Save Round Data")] = False,
        games: Annotated[Optional[int], typer.Option(help="Number of Rounds")] = 1):
    """
    Play cycle entry. Uses neural network for action but does not calculate error or update policy.
    """
    asyncio.run(run_fight(a1, a2, games, savedata))

if __name__ == '__main__':
    set_logging(log_level=DEBUG)
    app()