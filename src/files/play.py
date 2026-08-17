from src.files.OmniAI import OmniAI
from pyftg.socket.aio.gateway import Gateway
import os

async def run_fight(p1: str, p2: str, game_num: int, savedata: bool):
    """
    Builds connection and gameplay information and runs a match.
    Requires DareFightingICE to be ran in pyftg mode.

    Args:
    p1: Name of player 1 agent
    p2: Name of player 2 agent
    game_num: Number of matches to play
    savedata: Flag for exporting match information for player 1 to a CSV
    """
    character = "GARNET"
    host = os.environ.get("SERVER_HOST", "127.0.0.1")
    port = 31415
    gateway = Gateway(host, port)
    omni_ai = OmniAI(savedata)
    gateway.register_ai(p1, omni_ai)
    await gateway.run_game([character, character], [p1, p2], game_number=game_num)