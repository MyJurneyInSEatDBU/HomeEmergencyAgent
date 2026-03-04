from .cleanup_engine import clear_material_tick
from .constants import CLEAR_POS, FIRE_POS
from .drone_engine import drone_arrived
from .helpers import add_log, notify_owner, set_drone_target


def simulate_fire(state: dict) -> None:
    if state["phase"] == "detected":
        state["phase"] = "drone_to_fire"
        state["last_action"] = "drone_dispatched"
        state["last_message"] = "Fire detected. Agent dispatched."
        set_drone_target(state, FIRE_POS[0], FIRE_POS[1], "moving_to_fire")
        add_log(state, "Agent dispatched to fire location")
        return

    if state["phase"] == "drone_to_fire" and drone_arrived(state):
        state["phase"] = "deploying_water"
        state["last_action"] = "water_deployed"
        state["drone"]["status"] = "spraying_water"
        add_log(state, "Drone reached fire zone. Water suppression started")
        notify_owner(state, "Fire response active: water suppression has started.")
        return
    if state["phase"] == "deploying_water":
        state["fire_intensity"] = max(0, state["fire_intensity"] - 18)
        state["metrics"]["water_cycles"] += 1
        if state["fire_intensity"] == 0:
            state["phase"] = "clearing_materials"
            state["last_action"] = "fire_suppressed"
            state["drone"]["status"] = "post_fire_scan"
            set_drone_target(state, CLEAR_POS[0], CLEAR_POS[1], "clearing_zone")
            add_log(state, "Fire suppressed. Starting material evacuation")
            notify_owner(state, "Fire suppressed. Agent is evacuating affected materials.")
        return

    if state["phase"] == "clearing_materials":
        clear_material_tick(state)
