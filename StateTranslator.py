from pyftg import (FrameData, GameData)
from pyftg.models.character_data import CharacterData
import parameters as param
import torch

class StateTranslator():
    def __init__(self, frame_data: FrameData):
        self.char1_data = frame_data.character_data[0].to_dict()
        self.char2_data = frame_data.character_data[1].to_dict()
        self.frame_data = frame_data.to_dict()
        self.state_array = []

    def _norm_minmax(self, value, minval, maxval):
        return (value - minval) / (maxval - minval)

    def _norm_bool(self, value: bool):
        return float(value)

    def _norm_onehot(self, value, num_classes):
        vec = [0] * num_classes
        vec[value] = 1.0
        return vec

    def _normalize_data(self, data, schema):
        params = []
        for field, method, kwargs in schema:
            value = data[field]
            if method == "minmax":
                params.append(self._norm_minmax(value, **kwargs))
            elif method == "bool":
                params.append(self._norm_bool(value))
            elif method == "onehot":
                params.extend(self._norm_onehot(value, **kwargs))
        self.state_array.extend(params)

    def process(self):
        # Character 1 State
        attack_dict = self.char1_data["attack_data"]
        self._normalize_data(self.char1_data, param.CHAR_PARAMS)
        self._normalize_data(attack_dict, param.ATTACK_PARAMS)
        self._normalize_data(attack_dict["current_hit_area"], param.HIT_AREA_PARAMS)

        # Character 2 State
        attack_dict = self.char2_data["attack_data"]
        self._normalize_data(self.char2_data, param.CHAR_PARAMS)
        self._normalize_data(attack_dict, param.ATTACK_PARAMS)
        self._normalize_data(attack_dict["current_hit_area"], param.HIT_AREA_PARAMS)

        # Game State
        self._normalize_data(self.frame_data, param.GAME_PARAMS)

    def to_tensor(self):
        return torch.tensor(self.state_array, dtype=torch.float32)
    