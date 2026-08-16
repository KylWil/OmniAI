from src.vars.config import Config
from pathlib import Path
from src.files.StateEncoder import StateEncoder
from src.vars.dimensions import STATE_DIM
from src.vars.actions import ACTION_TABLE
from src.model.ActorCritic import ActorCritic
import torch
import logging

logger = logging.getLogger(__name__)

async def run_learn(
        a1: str,
        a2: str,
        agent_path: str,
        resume: str,):
    
    cfg = Config()
    Path(agent_path).mkdir(parents=True, exist_ok=True)

    encoder = StateEncoder(STATE_DIM)
    state_dim = encoder.get_state_dim
    n_actions = len(ACTION_TABLE)

    agent = ActorCritic(state_dim, n_actions)
    if resume:
        agent.load_state_dict(torch.load(resume))
        logger.info("resumed from %s", resume)

    ppo = PPO(agent, cfg)