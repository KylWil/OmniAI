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
from src.vars.config import Config
from src.model.buffer import RolloutBuffer
from src.model.ppo import PPO
from pathlib import Path
from torch.utils import tensorboard

log = logging.getLogger(__name__)

async def run_session(
                    p1: str,
                    p2: str, 
                    games: int, 
                    savedata: bool, 
                    randomaction: bool,
                    learn: bool=False, 
                    cuda=True,
                    character="GARNET"):
    """
    Builds connection and gameplay information and runs a match.
    Requires DareFightingICE to be ran in pyftg mode.

    Args:
    p1: Name of player 1 agent
    p2: Name of player 2 agent
    game_num: Number of matches to play
    savedata: Flag for exporting match information for player 1 to a CSV
    randomaction: Instructs the agent to use random actions
    learn: Flags the system to train the agent
    cuda: Use GPU for training
    character: Character to train the agent on
    """

    host = os.environ.get("SERVER_HOST", "127.0.0.1")
    port = 31415
    gateway = Gateway(host, port)

    device = torch.device('cuda' if torch.cuda.is_available() and cuda else 'cpu')
    encoder = StateEncoder()
    network = ActorCritic(STATE_DIM, ACTION_DIM, device)
    checkpoint_manager = CheckpointManager(p1)
    checkpoint = checkpoint_manager.load_latest_checkpoint(device)

    if checkpoint is not None: network.load_state_dict(checkpoint["network"])
    else: log.info("No checkpoint found, using untrained network.")

    # Warms up GPU library to avoid action delays during play
    network.act(torch.zeros(STATE_DIM))

    if checkpoint:
        update_counter = checkpoint.get("count", 0)
        round_counter = checkpoint.get("rounds", 0)
    else:
        update_counter = 0
        round_counter = 0
    
    buffer = None
    ppo = None
    cfg = None
    tb_writer = None

    if learn:
        cfg = Config()
        buffer = RolloutBuffer()
        ppo = PPO(network, cfg)
        if checkpoint is not None:
            ppo.optimizer.load_state_dict(checkpoint["optimizer"])

        runs_folder = Path(__file__).resolve().parent.parent / "runs"
        runs_folder.mkdir(exist_ok=True, parents=True)
        tb_writer = tensorboard.SummaryWriter(runs_folder)


    omni_ai = OmniAI(savedata, randomaction, network, encoder, update_counter, round_counter,
                     checkpoint_manager, tb_writer=tb_writer, buffer=buffer, ppo=ppo, cfg=cfg)

    gateway.register_ai(p1, omni_ai)
    await gateway.run_game([character, character], [p1, p2], game_number=games)