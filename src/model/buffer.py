import torch
from dataclasses import dataclass

@dataclass
class Batch:
    states: torch.Tensor
    actions: torch.Tensor
    old_logprobs: torch.Tensor
    advantages: torch.Tensor
    returns: torch.Tensor

class RolloutBuffer():
    def __init__(self):
        self.clear()

    def clear(self):
        self.states = []
        self.actions = []
        self.logprobs = []
        self.values = []
        self.rewards = []
        self.dones = []
        self.advantages = []
        self.returns = []

    def add(self, state, action, logprob, value):
        self.states.append(state)
        self.actions.append(action)
        self.logprobs.append(logprob.item())
        self.values.append(value.item())
        self.rewards.append(None)
        self.dones.append(None)

    def set_reward(self, reward, done):
        self.rewards[-1] = reward
        self.dones[-1] = done

    def compute_gae(self, gamma, lam):
        assert self.dones[-1]

        self.advantages = [0] * len(self)
        self.returns = [0] * len(self)
        gae = 0

        for i in range(len(self) - 1, -1, -1):
            next_value = 0 if self.dones[i] else self.values[i+1]
            delta = self.rewards[i] + gamma * next_value - self.values[i]
            gae = delta + gamma * lam * (0 if self.dones[i] else gae)
            self.advantages[i] = gae
            self.returns[i] = self.advantages[i] + self.values[i]

    def get_minibatches(self, minibatch_size, device):
        states = torch.stack(self.states).to(device)
        actions = torch.tensor(self.actions, dtype=torch.long, device=device)
        logprobs = torch.tensor(self.logprobs, dtype=torch.float32, device=device)
        advantages = torch.tensor(self.advantages, dtype=torch.float32, device=device)
        advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)
        returns = torch.tensor(self.returns, dtype=torch.float32, device=device)

        n = len(self)

        indices = torch.randperm(n, device=device)

        for i in range(0, n, minibatch_size):
            b = indices[i:i + minibatch_size]
            yield Batch(
                states=states[b],
                actions=actions[b],
                old_logprobs=logprobs[b],
                advantages=advantages[b],
                returns=returns[b]
            )


    def __len__(self):
        return len(self.states)