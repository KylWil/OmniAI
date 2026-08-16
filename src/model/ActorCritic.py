import torch.nn as nn
import torch
from torch.distributions import Categorical

class ActorCritic(nn.Module):
    def __init__(self, state_dim: int, n_actions: int, hidden: int = 256):
        super().__init__()
        self.trunk = nn.Sequential(
            nn.Linear(state_dim, hidden), nn.Tanh(),
            nn.Linear(hidden, hidden), nn.Tanh(),
        )
        self.actor = nn.Linear(hidden, n_actions)
        self.critic = nn.Linear(hidden, 1)

    def forward(self, x: torch.Tensor):
        h = self.trunk(x)
        logits = self.actor(h)
        value = self.critic(h).squeeze(-1)
        return logits, value

    @torch.no_grad()
    def act(self, state, deterministic: bool = False):
        x = torch.as_tensor(state, dtype=torch.float32).unsqueeze(0)
        logits, value = self.forward(x)
        dist = Categorical(logits=logits)
        action = logits.argmax(dim=-1) if deterministic else dist.sample()
        logprob = dist.log_prob(action)
        return action.item(), logprob.squeeze(0), value.squeeze(0)

    @torch.no_grad()
    def critic_value(self, state):
        x = torch.as_tensor(state, dtype=torch.float32).unsqueeze(0)
        nil, value = self.forward(x)
        return value.squeeze(0)

    def evaluate_actions(self, states: torch.Tensor, actions: torch.Tensor):
        logits, values = self.forward(states)
        dist = Categorical(logits=logits)
        logprobs = dist.log_prob(actions)
        entropy = dist.entropy()
        return logprobs, values, entropy
