from .constants import HOME_POS
from .helpers import add_log, notify_owner, set_drone_target


def detect(state: dict, emergency: str) -> dict:
    emergency = emergency.lower()
    if emergency not in {"none", "fire", "flood"}:
        return {"status": "unknown_emergency"}

    if emergency == "none":
        state["emergency"] = "none"
        state["phase"] = "idle"
        state["fire_intensity"] = 0
        state["flood_level"] = 0
        state["materials_inside"] = 0
        state["materials_outside"] = 0
        state["last_action"] = "cleared_by_operator"
        state["last_message"] = "Operator cleared emergency."
        set_drone_target(state, HOME_POS[0], HOME_POS[1], "returning_home")
        add_log(state, "Emergency cleared by operator")
        notify_owner(state, "Emergency status set to none. Monitoring only.")
        return {"status": "none_detected"}

    state["emergency"] = emergency
    state["phase"] = "detected"
    state["last_action"] = "detected"
    state["materials_inside"] = 6
    state["materials_outside"] = 0
    state["material_tick"] = 0

    if emergency == "fire":
        state["fire_intensity"] = 100
        state["flood_level"] = 0
        add_log(state, "Emergency detected: FIRE")
    else:
        state["fire_intensity"] = 0
        state["flood_level"] = 100
        add_log(state, "Emergency detected: FLOOD")

    notify_owner(state, f"{emergency.upper()} detected. Autonomous response started.")
    return {"status": f"{emergency}_detected"}
