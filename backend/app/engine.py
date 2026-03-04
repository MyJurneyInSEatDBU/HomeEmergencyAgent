from .drone_engine import update_drone_position
from .fire_engine import simulate_fire
from .flood_engine import simulate_flood


def simulate_step(state: dict) -> None:
    update_drone_position(state)

    if state["emergency"] == "none":
        return

    if state["emergency"] == "fire":
        simulate_fire(state)
    elif state["emergency"] == "flood":
        simulate_flood(state)
