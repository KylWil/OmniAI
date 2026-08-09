CHAR_PARAMS = [
    ("hp", "minmax", {"minval":0, "maxval":400}),
    ("energy", "minmax", {"minval":0, "maxval":300}),
    ("x", "minmax", {"minval":0, "maxval":960}),
    ("y", "minmax", {"minval":0, "maxval":640}),
    ("speed_x", "minmax", {"minval":-40, "maxval":40}),
    ("speed_y", "minmax", {"minval":-40, "maxval":40}),
    ("state", "onehot", {"num_classes":4}),
    ("front", "bool", {}),
    ("control", "bool", {}),
    ("remaining_frame", "minmax", {"minval":0, "maxval":100}),
    ("hit_confirm", "bool", {}),
]

ATTACK_PARAMS = [
    ("current_frame", "minmax", {"minval":0, "maxval":100}),
    ("speed_x", "minmax", {"minval":-15, "maxval":35}),
    ("speed_y", "minmax", {"minval":-25, "maxval":0}),
    ("impact_x", "minmax", {"minval":0, "maxval":20}),
    ("impact_y", "minmax", {"minval":-10, "maxval":0}),
    ("give_guard_recov", "minmax", {"minval":0, "maxval":18}),
    ("attack_type", "onehot", {"num_classes":5}),
    ("down_prop", "bool", {}),
    ("is_projectile", "bool", {}),
    ("is_live", "bool", {}),
]

HIT_AREA_PARAMS = [
    ("left", "minmax", {"minval":0, "maxval":960}),
    ("right", "minmax", {"minval":0, "maxval":960}),
    ("top", "minmax", {"minval":0, "maxval":640}),
    ("bottom", "minmax", {"minval":0, "maxval":640}),
]

GAME_PARAMS = [
    ("current_frame_number", "minmax", {"minval":0, "maxval":3600}),
]

CUSTOM_PARAMS = [
    ("action", "onehot", {"num_classes":8}),
]