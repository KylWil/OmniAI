from pathlib import Path

class Config:
    def __init__(self):
        self.character_one = "GARNET"
        self.character_two = "GARNET"

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
                    raise AttributeError(f"{key} is an invalid config attribute.")

                if key == "character_one" or key == "character_two":
                    if not self.valid_characters.__contains__(val):
                        raise AttributeError(f"{val} is not a valid character. Check config settings.")

                try:
                    converted = type(getattr(self, key))(val)
                except ValueError:
                    raise TypeError(f"Could not convert {val} to {type(getattr(self, key))}.")

                setattr(self, key, converted)