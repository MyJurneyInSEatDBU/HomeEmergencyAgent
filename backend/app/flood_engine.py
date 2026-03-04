from .cleanup_engine import clear_material_tick
from .constants import CLEAR_POS, FLOOD_POS
from .drone_engine import drone_arrived
from .helpers import add_log, notify_owner, set_drone_target
def simulate_flood(state: dict) -> None:
    if state["phase"] == "detected":
        state["phase"] = "drone_to_flood"
        state["last_action"] = "drone_dispatched"
        state["last_message"] = "Flood detected. Evacuation route check started."
        set_drone_target(state, FLOOD_POS[0], FLOOD_POS[1], "moving_to_flood")
        add_log(state, "Agent dispatched to flood location")
        return

    if state["phase"] == "drone_to_flood" and drone_arrived(state):
        state["phase"] = "evacuating"
        state["last_action"] = "evacuation_started"
        state["drone"]["status"] = "guiding_evacuation"
        add_log(state, "Flood zone reached. Evacuation and routing started")
        notify_owner(state, "Flood response active: evacuation routing started.")
        return

    if state["phase"] == "evacuating":
        state["flood_level"] = max(0, state["flood_level"] - 14)
        state["metrics"]["evac_cycles"] += 1
        if state["flood_level"] <= 30:
            state["phase"] = "clearing_materials"
            state["last_action"] = "stabilized_flood_zone"
            set_drone_target(state, CLEAR_POS[0], CLEAR_POS[1], "clearing_zone")
            add_log(state, "Flood stabilized. Starting material evacuation")
            notify_owner(state, "Flood level stabilized. Agent is clearing affected materials.")
        return

    if state["phase"] == "clearing_materials":
        clear_material_tick(state)
