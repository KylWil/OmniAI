import logging
import threading

from src.files.buffer import RolloutBuffer

log = logging.getLogger(__name__)

class Learner():
    def __init__(self, ppo, network, update_counter, 
                 round_counter, tb_writer, checkpoint_manager, cfg, encoder):
        self.ppo = ppo
        self.network = network
        self.update_counter = update_counter
        self.round_counter = round_counter
        self.tb_writer = tb_writer
        self.checkpoint_manager = checkpoint_manager
        self.cfg = cfg
        self.encoder = encoder

        self.buffer = RolloutBuffer()
        self.lock = threading.Lock()

    def submit(self, buffer):
        self.buffer.extend(buffer)

        if len(self.buffer) < self.cfg.n_steps:
            return

        with self.lock:
            learning_stats = self.ppo.update(self.network, self.buffer)

        self.update_counter += 1

        for key, value in learning_stats.items():
            self.tb_writer.add_scalar(key, value, self.update_counter)
        self.tb_writer.flush()

        self.buffer.clear()
        log.info("Network Updated")

        if self.update_counter % self.cfg.checkpoint_every == 0:
            self.checkpoint_manager.create_new_checkpoint(self.update_counter, self.round_counter, self.network, self.ppo.optimizer)
            log.info("Checkpoint %s saved", self.update_counter)

    def log_round(self, player_hp, opp_hp):
        if self.tb_writer is None:
            return
        
        self.round_counter += 1
        self.tb_writer.add_scalar("round/win", 1 if player_hp > opp_hp else 0, self.round_counter)
        self.tb_writer.add_scalar("round/hp_diff", player_hp - opp_hp, self.round_counter)
        self.tb_writer.flush()