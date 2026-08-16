from dataclasses import dataclass

@dataclass
class Config:
    n_steps: int = 4096
    checkpoint_every: int = 10
    eval_every: int = 10

    # PPO optimization
    lr: float = 3e-4
    gamma: float = 0.99
    lam: float = 0.95
    clip: float = 0.2
    k_epochs: int = 4            
    minibatch_size: int = 256
    entropy_coef: float = 0.01
    value_coef: float = 0.5
    max_grad_norm: float = 0.5