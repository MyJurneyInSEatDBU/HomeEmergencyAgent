import math
def update_drone_position(state: dict) -> None:
    dx = state["drone"]["target_x"] - state["drone"]["x"]
    dy = state["drone"]["target_y"] - state["drone"]["y"]
    distance = math.sqrt((dx * dx) + (dy * dy))

    if distance < 0.5:
        state["drone"]["x"] = state["drone"]["target_x"]
        state["drone"]["y"] = state["drone"]["target_y"]
        if state["phase"] in {"idle", "resolved"}:
            state["drone"]["status"] = "idle"
        return

    speed = 12.0
    ratio = min(1.0, speed / distance)
    state["drone"]["x"] += dx * ratio
    state["drone"]["y"] += dy * ratio


def drone_arrived(state: dict) -> bool:
    return (
        abs(state["drone"]["x"] - state["drone"]["target_x"]) < 1.0
        and abs(state["drone"]["y"] - state["drone"]["target_y"]) < 1.0
    )
