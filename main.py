import asyncio
import typer
from typing_extensions import Annotated, Optional
from pyftg.utils.logging import DEBUG, set_logging
from src.files.play import run_fight
from src.files.learn import run_learn

app = typer.Typer()


@app.command()
def learn(
        a1: Annotated[Optional[str], typer.Option(help="Player 1 AI")] = "OmniAI",
        a2: Annotated[Optional[str], typer.Option(help="Player 2 AI")] = "MctsAi23i",
        agent_path: Annotated[Optional[str], typer.Option(help="Trained agent directory")] = "src/agents"):
    """
    Learning cycle entry. Uses neural network for action and backpropogates error to update policy.
    """
    asyncio.run(run_learn(a1, a2, agent_path))

@app.command()
def play(
        a1: Annotated[Optional[str], typer.Option(help="Player 1 AI")] = "OmniAI",
        a2: Annotated[Optional[str], typer.Option(help="Player 2 AI")] = "MctsAi23i",
        savedata: Annotated[Optional[bool], typer.Option(help="Collect and Save Round Data")] = False,
        games: Annotated[Optional[int], typer.Option(help="Number of Rounds")] = 1,
        randomaction: Annotated[Optional[bool], typer.Option(help="Sets a1 to perform randomized actions")] = False):
    """
    Play cycle entry. Uses neural network for action but does not calculate error or update policy.
    """
    asyncio.run(run_fight(a1, a2, games, savedata, randomaction))

if __name__ == '__main__':
    set_logging(log_level=DEBUG)
    app()