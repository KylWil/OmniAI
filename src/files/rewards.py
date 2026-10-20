class Reward():
    def __init__(self, player, player_max_hp, opp_max_hp):
        self.player = player
        self.previous_state = None
        self.player_max_hp = player_max_hp
        self.opp_max_hp = opp_max_hp

    def reset(self):
        self.previous_state = None

    def _snapshot(self, frame_data):
        player_agent = frame_data.get_character(self.player)
        opp_agent = frame_data.get_character(not self.player)

        return player_agent, opp_agent

    def compute(self, frame_data):
        player, opp = self._snapshot(frame_data)

        if self.previous_state is None:
            self.previous_state = [player, opp]
            return None

        prev_player = self.previous_state[0]
        prev_opp = self.previous_state[1]

        self.previous_state = [player, opp]

        taken = (player.hp - prev_player.hp) / self.player_max_hp
        dealt = (prev_opp.hp - opp.hp) / self.opp_max_hp

        return taken + dealt