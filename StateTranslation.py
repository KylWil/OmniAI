from pyftg import (FrameData, GameData)
from pyftg.models.character_data import CharacterData

class StateTranslation():
    def __init__(self, frame_data: FrameData, game_data: GameData):
        self.char1_data = frame_data.character_data[0].to_dict()
        self.char2_data = frame_data.character_data[1].to_dict()
        self.frame_data = frame_data.to_dict()
        self.game_data = game_data.to_dict()
        self.state_array = []

    def norm_minmax(self, value, min_val, max_val):
        return (value - min_val) / (max_val - min_val)

    def norm_bool(self, value: bool):
        return float(value)

    def norm_onehot(self, value, num_classes):
        vec = [0] * num_classes
        vec[value] = 1.0
        return vec

    def process(self):
        pass

    def to_tensor(self):
        pass
    