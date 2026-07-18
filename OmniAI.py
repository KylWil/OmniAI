from pyftg import (AIInterface, GameData, FrameData, ScreenData, 
                   AudioData, Key, RoundResult, CommandCenter)
import logging

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
        pass

    def get_information(self, frame_data: FrameData, is_control: bool):
        pass

    def get_screen_data(self, screen_data: ScreenData):
        """
        Unneeded for parameter-based learning.
        """
        pass

    def get_audio_data(self, audio_data: AudioData):
        """
        Unneeded for parameter-based learning.
        """
        pass

    def processing(self):
        pass

    def input(self) -> Key:
        pass

    def round_end(self, round_result: RoundResult):
        log.info("End of Round: %s", round_result)

    def game_end(self):
        log.info("End of Game")

    def close(self):
        pass