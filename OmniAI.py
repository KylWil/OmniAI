from pyftg import (AIInterface, GameData, FrameData, ScreenData, 
                   AudioData, Key, RoundResult, CommandCenter)
import logging
import random

log = logging.getLogger(__name__)

class OmniAI(AIInterface):
    def __init__(self):
        super().__init__()
        self.blind = True

    def name(self) -> str:
        return self.__class__.__name__

    def is_blind(self) -> bool:
        return self.blind

    def initialize(self, game_data: GameData, player_number: bool):
        log.info("%s Starting..", self.name())
        self.cc = CommandCenter()
        self.key = Key()
        self.player_num = player_number

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

        if self.cc.get_skill_flag():
            self.key = self.cc.get_skill_key()
        else:
            self.key.empty()
            self.cc.skill_cancel()

            rand = random.uniform(0, 1)

            if (rand < 0.5):
                self.cc.command_call("B")
            else:
                self.cc.command_call("JUMP")

    def input(self) -> Key:
        return self.key

    def round_end(self, round_result: RoundResult):
        log.info("End of Round: %s", round_result)

    def game_end(self):
        log.info("End of Game")

    def close(self):
        """
        Runs at the end of AIController run loop
        """
        pass