import asyncio
import logging
import os
from pathlib import Path

import numpy as np
import torch
from pyftg.socket.aio.gateway import Gateway
from torch.utils import tensorboard

from src.files.client_manager import ClientManager
from src.files.data_center import DataCenter
from src.files.learner import Learner
from src.files.encoder import StateEncoder
from src.files.omni_ai import OmniAI
from src.model.ppo.actor_critic import ActorCritic
from src.model.ppo.buffer import RolloutBuffer
from src.model.ppo.checkpoint import CheckpointManager
from src.model.ppo.ppo import PPO
from src.vars.actions import ACTIONS_DIM
from src.vars.config import Config
from src.vars.state_parameters import STATE_DIM

log = logging.getLogger(__name__)

async def run_session(
                    p1: str,
                    p2: str, 
                    games: int, 
                    exportcsv: bool,
                    agent_name: str,
                    learn: bool=False,
                    deterministic: bool=False,
                    nocuda=False,
                    clients=1,):
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

    agent_folder = Path(__file__).parent.parent.parent / "agents" / agent_name
    data_center = DataCenter(agent_folder)

    cfg = Config()

    host = os.environ.get("SERVER_HOST", "127.0.0.1")

    port_base = 31400
    port_range = list(range(clients))
    ports = [x + port_base for x in port_range]

    gateways = []
    encoders = []
    buffers = []

    for port in ports:
        gateways.append(Gateway(host, port))
        encoders.append(StateEncoder())
        if learn:
            buffers.append(RolloutBuffer())
        else:
            buffers.append(None)

    device = torch.device('cuda' if torch.cuda.is_available() and not nocuda else 'cpu')
    network = ActorCritic(STATE_DIM, ACTIONS_DIM, device)
    checkpoint_manager = CheckpointManager(agent_folder)
    checkpoint = checkpoint_manager.load_latest_checkpoint(device)

    log_dir = agent_folder / "client_logs"
    log_dir.mkdir(exist_ok=True, parents=True)

    c_manager = ClientManager(learn, log_dir, "127.0.0.1")

    if checkpoint is not None:
        network.load_state_dict(checkpoint["network"])
        log.info("Checkpoint %s loaded", checkpoint["count"])

    else:
        log.info("No checkpoint found, using untrained network.")

    # Warms up GPU library to avoid action delays during play
    network.act(torch.zeros(STATE_DIM))

    if checkpoint:
        update_counter = checkpoint.get("count", 0)
        round_counter = checkpoint.get("rounds", 0)
    else:
        update_counter = 0
        round_counter = 0
    
    ppo = None
    tb_writer = None


    if learn:
        ppo = PPO(network, cfg)
        if checkpoint is not None:
            ppo.optimizer.load_state_dict(checkpoint["optimizer"])

        runs_folder = agent_folder / "tensorboard"
        runs_folder.mkdir(exist_ok=True, parents=True)
        tb_writer = tensorboard.SummaryWriter(runs_folder)

    learner = Learner(ppo, network, update_counter, round_counter, tb_writer,
                      checkpoint_manager, cfg)

    ai_controllers = []

    for i in range(len(gateways)):
        ai_controllers.append(OmniAI(learner, encoders[i], buffers[i], exportcsv, deterministic, data_center))

    for i in range(len(gateways)):
        gateways[i].register_ai(p1, ai_controllers[i])

    try:
        c_manager.launch_clients(ports)

        corouts = []

        for gateway in gateways:
            corouts.append(gateway.run_game([cfg.character_one, cfg.character_two], [p1, p2], game_number=games))

        await asyncio.gather(*corouts)

    finally:
        c_manager.close_clients()