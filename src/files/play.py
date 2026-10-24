from src.files.omni_ai import OmniAI
from pyftg.socket.aio.gateway import Gateway
import os
import torch
from src.files.encoder import StateEncoder
from src.model.actor_critic import ActorCritic
from src.vars.dimensions import ACTION_DIM
from src.vars.dimensions import STATE_DIM
from src.files.checkpoint import CheckpointManager
import logging
from src.model.buffer import RolloutBuffer

log = logging.getLogger(__name__)

async def run_fight(p1: str, p2: str, game_num: int, savedata: bool, randomaction: bool, cuda=True):
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

    device = torch.device('cuda' if torch.cuda.is_available() and cuda else 'cpu')
    encoder = StateEncoder()
    network = ActorCritic(STATE_DIM, ACTION_DIM, device)
    checkpoint_manager = CheckpointManager(p1)
    checkpoint = checkpoint_manager.load_latest_checkpoint(device)

    if checkpoint is not None: network.load_state_dict(checkpoint["model"])
    else: log.info("Failed to load checkpoint. Playing with untrained network.")

    # Warms up GPU library to avoid action delays during play
    network.act(torch.zeros(STATE_DIM))

    omni_ai = OmniAI(savedata, randomaction, network, encoder)

    gateway.register_ai(p1, omni_ai)
    await gateway.run_game([character, character], [p1, p2], game_number=game_num)