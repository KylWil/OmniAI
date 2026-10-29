from pyftg import (AIInterface, GameData, FrameData, ScreenData, 
                   AudioData, Key, RoundResult, CommandCenter,)
from src.files.data_center import DataCenter
from src.vars.actions import ACTIONS
import logging
import random
from src.files.rewards import Reward

log = logging.getLogger(__name__)

class OmniAI(AIInterface):
    """
    Primary bridge between DareFightingICE client and learning environment.
    Called by pyftg's Gateway class every frame to get updated state information and
    deliver a response.

    Args:
    AIInterface: Interface class being inherited from pyftg
    """
    def __init__(self, savedata, randomaction, network, encoder,
                  update_counter, round_counter, checkpoint_manager, tb_writer=None, buffer=None, ppo=None, cfg=None):
        super().__init__()
        self.blind = True
        self.savedata = savedata
        self.randomaction = randomaction
        self.network = network
        self.encoder = encoder
        self.update_counter = update_counter
        self.round_counter = round_counter
        self.checkpoint_manager = checkpoint_manager
        self.buffer = buffer
        self.ppo = ppo
        self.cfg = cfg
        self.tb_writer = tb_writer

    def name(self) -> str:
        return self.__class__.__name__

    def is_blind(self) -> bool:
        return self.blind

    def initialize(self, game_data: GameData, player_number: bool):
        log.info("%s Starting..", self.name())
        self.cc = CommandCenter()
        self.dc = DataCenter()
        self.game_data = game_data
        self.key = Key()
        self.player_num = player_number

        if player_number:
            self.player_index = 0
            self.opp_index = 1
        else:
            self.player_index = 1
            self.opp_index = 0

        player_max_hp = game_data.max_hps[self.player_index]
        opp_max_hp = game_data.max_hps[self.opp_index]

        self.reward = Reward(self.player_num, player_max_hp, opp_max_hp)
        log.info("Saving Data: %s", self.savedata)

    def get_non_delay_frame_data(self, frame_data: FrameData):
        self.nd_frame_data = frame_data

    def get_information(self, frame_data: FrameData, is_control: bool):
        self.frame_data = frame_data
        self.cc.set_frame_data(frame_data, self.player_num)
        self.is_control = is_control

    def get_screen_data(self, screen_data: ScreenData):
        pass

    def get_audio_data(self, audio_data: AudioData):
        pass

    def processing(self):
        if self.frame_data.empty_flag or self.frame_data.current_frame_number <= 0:
            return

        if self.savedata:
            self.dc.add_char_data(char_data = self.frame_data.get_character(True))

        self.encoder.load(self.frame_data)
        self.encoder.process()
        state = self.encoder.to_tensor()

        if self.cc.get_skill_flag():
            self.key = self.cc.get_skill_key()
        else:
            self.key.empty()
            self.cc.skill_cancel()

            reward = self.reward.compute(self.frame_data)

            if self.buffer is not None and reward is not None:
                self.buffer.set_reward(reward, False)

            index, logprob, value = self.network.act(state=state)

            if self.buffer is not None:
                self.buffer.add(state, index, logprob, value)

            if reward:
                log.info("reward: %.3f", reward)

            self.cc.command_call(ACTIONS[index])

    def input(self) -> Key:
        return self.key

    def round_end(self, round_result: RoundResult):
        round_end_reward = self.reward.compute_round_end(round_result)
        if round_end_reward is not None:
            if self.buffer is not None:
                self.buffer.set_reward(round_end_reward, True)
            log.info("Round end reward: %s", round_end_reward)

        if self.tb_writer is not None:
            self.round_counter += 1
            player_hp = round_result.remaining_hps[self.player_index]
            opp_hp = round_result.remaining_hps[self.opp_index]

            self.tb_writer.add_scalar("round/win", 1 if player_hp > opp_hp else 0, self.round_counter)
            self.tb_writer.add_scalar("round/hp_diff", player_hp - opp_hp, self.round_counter)
            self.tb_writer.flush()

        if self.ppo is not None and len(self.buffer) >= self.cfg.n_steps:
            self.buffer.compute_gae(self.cfg.gamma, self.cfg.lam)
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
            
                
        self.reward.reset()
        log.info("End of Round: %s", round_result)

        if self.savedata:
            date = self.dc.export_data()
            log.info("Successfully saved data for round on: %s", date)

    def game_end(self):
        log.info("End of Game")

    def close(self):
        pass