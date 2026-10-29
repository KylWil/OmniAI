from pathlib import Path
import torch

class CheckpointManager():
    def __init__(self, agent_name):
        self.agent_name = agent_name
        self.agents_folder = Path(__file__).resolve().parent.parent / "agents" / agent_name

    def _checkpoint_number(self, path):
        return int(path.stem.split("_")[1])

    def load_latest_checkpoint(self, device):
        checkpoints = list(self.agents_folder.glob("ckpt_*.pt"))
        if not checkpoints:
            return None

        latest = max(checkpoints, key=self._checkpoint_number)
        return torch.load(latest, map_location=device)

    def create_new_checkpoint(self, count, network, optimizer):
        self.agents_folder.mkdir(parents=True, exist_ok=True)
        save_dict = {
            "network": network.state_dict(),
            "optimizer": optimizer.state_dict(),
            "count": count
        }

        f = self.agents_folder / f"ckpt_{count}.pt"
        torch.save(save_dict, f)