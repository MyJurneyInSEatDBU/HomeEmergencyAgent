from datetime import datetime
def add_log(state: dict, message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    state["logs"].insert(0, f"[{timestamp}] {message}")
    state["logs"] = state["logs"][:70]
def set_drone_target(state: dict, x: float, y: float, status: str) -> None:
    state["drone"]["target_x"] = x
    state["drone"]["target_y"] = y
    state["drone"]["status"] = status
def notify_owner(state: dict, message: str) -> None:
    state["last_message"] = message
    add_log(state, f"Owner notified (simulation): {message}")
