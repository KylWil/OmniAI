import torch
import torch.nn as nn

from src.vars.config import Config

class PPO:
    def __init__(self, agent: nn.Module, config: Config):
        self.agent = agent
        self.config = config
        self.optimizer = torch.optim.Adam(agent.parameters(), lr=config.lr)

    def update(self, agent, buffer):
        policy_loss_list = []
        value_loss_list = []
        entropy_list = []

        for epoch in range(self.config.k_epochs):
            for batch in buffer.get_minibatches(self.config.minibatch_size, agent.device):
                logprobs, values, entropy = agent.evaluate_actions(batch.states, batch.actions)

                ratio = torch.exp(logprobs - batch.old_logprobs)

                advantages = batch.advantages

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

                policy_loss_list.append(policy_loss.item())
                value_loss_list.append(value_loss.item())
                entropy_list.append(entropy_bonus.item())

        return {
            "policy_loss": (sum(policy_loss_list) / len(policy_loss_list)),
            "value_loss": (sum(value_loss_list) / len(value_loss_list)),
            "entropy": (sum(entropy_list) / len(entropy_list))
        }