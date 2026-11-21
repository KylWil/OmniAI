import torch

from src.vars import state_parameters as param

class StateEncoder():
    """
    Encodes state values from a frame. Values controlled by parameters.py
    file variables. Flat values are normalized on a 0 to 1 scale. 
    Boolean values are normalized to 0 and 1. Categorical values are
    appended as a binary list with at most one 1 value.
    """
    def __init__(self):
        pass

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
        return params

    def encode(self, frame_data):
        """
        Normalizes the game state values. Changing the order or content of this class
        WILL disable training of an existing model. Updates should be only made for new models.
        """
        # Do not change order or content of normalization if you intend to continue training of an existing model.

        char1_data = frame_data.character_data[0].to_dict()
        char2_data = frame_data.character_data[1].to_dict()
        frame_data = frame_data.to_dict()
        state_array = []

        # Character 1 State
        attack_dict = char1_data["attack_data"]
        state_array.extend(self._normalize_data(char1_data, param.CHAR_PARAMS))
        state_array.extend(self._normalize_data(attack_dict, param.ATTACK_PARAMS))
        state_array.extend(self._normalize_data(attack_dict["current_hit_area"], param.HIT_AREA_PARAMS))

        # Character 2 State
        attack_dict = char2_data["attack_data"]
        state_array.extend(self._normalize_data(char2_data, param.CHAR_PARAMS))
        state_array.extend(self._normalize_data(attack_dict, param.ATTACK_PARAMS))
        state_array.extend(self._normalize_data(attack_dict["current_hit_area"], param.HIT_AREA_PARAMS))

        # Game State
        state_array.extend(self._normalize_data(frame_data, param.GAME_PARAMS))

        return torch.tensor(state_array, dtype=torch.float32)