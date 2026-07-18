import asyncio
import typer
from typing_extensions import Annotated, Optional
from pyftg.socket.aio.gateway import Gateway
from pyftg.utils.logging import DEBUG, set_logging

app = typer.Typer()

async def start_process(host: str, port: int, a1: str, a2: str):
    gateway = Gateway(host=host, port=port)
    gateway.load_agent([a1, a2])
    await gateway.start_ai()

@app.command()
def main(host: Annotated[Optional[str], typer.Option(help="DareFightingICE Host")] = "127.0.0.1",
        port: Annotated[Optional[int], typer.Option(help="DareFightingICE Port")] = 31415,
        a1: Annotated[Optional[str], typer.Option(help="Player 1 AI")] = None,
        a2: Annotated[Optional[str], typer.Option(help="Player 2 AI")] = None):
    asyncio.run(start_process(host=host, port=port, a1=a1, a2=a2))

if __name__ == '__main__':
    set_logging(log_level=DEBUG)
    app()