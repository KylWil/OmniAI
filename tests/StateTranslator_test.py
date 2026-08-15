from src.files.StateTranslator import StateTranslator

from pyftg.models.hit_area import HitArea
from pyftg.models.attack_data import AttackData
from pyftg.models.character_data import CharacterData
from pyftg.models.frame_data import FrameData


hit_dummy = HitArea.from_dict(
    {
        "left": 301,
        "right": 320,
        "top": 50,
        "bottom": 30,
    }
)

attack_dummy = AttackData.from_dict(
    {
        "setting_hit_area": hit_dummy.to_dict(),
        "setting_speed_x": 0,
        "setting_speed_y": 0,
        "current_hit_area": hit_dummy.to_dict(),
        "current_frame": 50,
        "player_number": 1,
        "speed_x": -14,
        "speed_y": -12,
        "start_up": 5,
        "active": 2,
        "hit_damage": 10,
        "guard_damage": 5,
        "start_add_energy": 0,
        "hit_add_energy": 0,
        "guard_add_energy": 0,
        "give_energy": 0,
        "impact_x": 10,
        "impact_y": -5,
        "give_guard_recov": 0,
        "attack_type": 3,
        "down_prop": True,
        "is_projectile": False,
        "is_live": False,
        "empty_flag": True,
        "identifier": "pawnch",
    }
)

char_dummy = CharacterData.from_dict(
    {
        "player_number": 0,
        "hp": 1,
        "energy": 300,
        "x": 20,
        "y": 600,
        "left": 1,
        "right": 2,
        "top": 3,
        "bottom": 4,
        "speed_x": 0,
        "speed_y": -20,
        "state": 2,
        "action": 15,
        "front": True,
        "control": False,
        "attack_data": attack_dummy.to_dict(),
        "remaining_frame": 50,
        "hit_confirm": True,
        "graphic_size_x": 20,
        "graphic_size_y": 20,
        "graphic_adjust_x": 0,
        "hit_count": 0,
        "last_hit_frame": 5,
        "projectile_attack": [],
    }
)

frame_dummy = FrameData.from_dict(
    {
        "character_data": [char_dummy.to_dict(), char_dummy.to_dict()],
        "current_frame_number": 2391,
        "current_round": 2,
        "projectile_data": [],
        "empty_flag": False,
        "front": [False, False],
    }
)

test_translation = StateTranslator(frame_data=frame_dummy)
test_translation.process()
final_state = test_translation.to_tensor()

print(final_state)
print(len(final_state))