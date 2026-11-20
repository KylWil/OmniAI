import logging

from pathlib import Path

log = logging.getLogger(__name__)

class Config:
    def __init__(self):
        self.character_one = "GARNET"
        self.character_two = "GARNET"

        self.round_end_scale=1.0
        self.win_scale=1.0
        self.loss_scale=1.0

        self.n_steps = 2048
        self.checkpoint_every = 10    
        self.minibatch_size = 256
        self.k_epochs = 4

        self.lr = 3e-4
        self.gamma = 0.99
        self.lam = 0.95
        self.clip = 0.2
        self.entropy_coef = 0.01
        self.value_coef = 0.5
        self.max_grad_norm = 0.5

        self.valid_characters = ["GARNET", "ZEN", "LUD", "NEZ"]

        self.config_path = Path(__file__).parent.parent.parent / "config.cfg"
        self._load_config()

    def _load_config(self):
        with open(self.config_path, "r", encoding="utf-8") as file:
            for line in file:
                if (line.strip().startswith("#")) or not line.rstrip():
                    continue

                var_line = line.rstrip().split("=", 1)

                key = var_line[0].strip()
                val = var_line[1].strip().strip("\"'")

                if not hasattr(self, key):
                    log.info(f"{key} is an invalid config attribute.") 
                    continue

                if key == "character_one" or key == "character_two":
                    if not self.valid_characters.__contains__(val):
                        log.info(f"{val} is not a valid character. Defaulting to {getattr(self, key)}")
                        continue

                if key == "round_end_scale" or key == "win_scale" or key == "loss_scale":
                    try:
                        if float(val) < 0 or float(val) > 2:
                            log.info(f"{key} only accepts values within 0-2 inclusive. Defaulting to {getattr(self, key)}")
                            continue
                    except ValueError:
                        pass    

                try:
                    converted = type(getattr(self, key))(val)
                except ValueError:
                    log.info(f"Could not convert {val} to {type(getattr(self, key))}. Defauling to {getattr(self, key)}")
                    continue

                setattr(self, key, converted)