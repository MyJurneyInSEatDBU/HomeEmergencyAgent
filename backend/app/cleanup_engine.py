from .constants import HOME_POS
from .helpers import add_log, notify_owner, set_drone_target
def clear_material_tick(state: dict) -> None:
    state["material_tick"] += 1
    if state["material_tick"] < 2:
        return

    state["material_tick"] = 0
    if state["materials_inside"] > 0:
        state["materials_inside"] -= 1
        state["materials_outside"] += 1
        add_log(state, "Agent moved one material outside the affected zone")

    if state["materials_inside"] == 0:
        state["phase"] = "resolved"
        state["last_action"] = "area_cleared"
        add_log(state, "Cleanup complete. Emergency resolved.")
        notify_owner(state, "Emergency handled. Area cleared and home zone is safe.")
        state["emergency"] = "none"
        state["fire_intensity"] = 0
        state["flood_level"] = 0
        set_drone_target(state, HOME_POS[0], HOME_POS[1], "returning_home")
