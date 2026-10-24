import torch

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

    def __len__(self):
        return len(self.states)