# src/agent/ppo.py
import torch
import torch.nn as nn

from src.vars.config import Config


class PPO:
    def __init__(self, agent: nn.Module, config: Config):
        self.agent = agent
        self.config = config
        self.optimizer = torch.optim.Adam(agent.parameters(), lr=config.lr)

    def update(self, agent, buffer):
        for epoch in range(self.config.k_epochs):
            for batch in buffer.get_minibatches(self.config.minibatch_size):
                logprobs, values, entropy = agent.evaluate_actions(batch.states, batch.actions)

                ratio = torch.exp(logprobs - batch.old_logprobs)

                advantages = batch.advantages
                advantages = (advantages - advantages.mean()) / (advantages.std() + 1e-8)

                surr1 = ratio * advantages
                surr2 = torch.clamp(ratio, 1 - self.config.clip, 1 + self.config.clip) * advantages
                policy_loss = -torch.min(surr1, surr2).mean()

                value_loss = nn.functional.mse_loss(values, batch.returns)

                entropy_bonus = entropy.mean()

                loss = (
                    policy_loss
                    + self.config.value_coef * value_loss
                    - self.config.entropy_coef * entropy_bonus
                )

                self.optimizer.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(agent.parameters(), self.config.max_grad_norm)
                self.optimizer.step()