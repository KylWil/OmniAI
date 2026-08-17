from pyftg import (AIInterface, GameData, FrameData, ScreenData, 
                   AudioData, Key, RoundResult, CommandCenter,)
from src.files.DataCenter import DataCenter
import logging
import random

log = logging.getLogger(__name__)

class OmniAI(AIInterface):
    """
    Primary bridge between DareFightingICE client and learning environment.
    Called by pyftg's Gateway class every frame to get updated state information and
    deliver a response.

    Args:
    AIInterface: Interface class being inherited from pyftg
    """
    def __init__(self, savedata):
        super().__init__()
        self.blind = True
        self.savedata = savedata

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

        if self.savedata:
            date = self.dc.export_data()
            log.info("Successfully saved data for round on: %s", date)

    def game_end(self):
        log.info("End of Game")

    def close(self):
        pass