from .constants import HOME_POS


def make_state() -> dict:
    return {
        "emergency": "none",
        "phase": "idle",
        "last_action": "none",
        "last_message": "none",
        "fire_intensity": 0,
        "flood_level": 0,
        "materials_inside": 0,
        "materials_outside": 0,
        "material_tick": 0,
        "drone": {
            "x": HOME_POS[0],
            "y": HOME_POS[1],
            "target_x": HOME_POS[0],
            "target_y": HOME_POS[1],
            "status": "idle",
        },
        "metrics": {"water_cycles": 0, "evac_cycles": 0},
        "logs": [],
    }
