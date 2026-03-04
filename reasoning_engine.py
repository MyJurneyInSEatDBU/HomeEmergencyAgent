from __future__ import annotations

from mission_state import CargoInventory, MissionState


class ReasoningEngine:
    """Reasoning engine for the survival agent."""

    def __init__(self) -> None:
        self.daily_rates = {
            "oxygen": 3,
            "power": 4,
            "food": 2,
            "fuel": 5,
            "hull": 1,
        }

    def _clamp(self, value: float) -> int:
        return max(0, min(100, int(round(value))))

    def predict_failure_point(self, state: MissionState, max_days: int = 200):
        """Simulate future time-steps and return the first resource to hit zero."""
        sim = MissionState(
            oxygen=state.oxygen,
            power=state.power,
            food=state.food,
            fuel=state.fuel,
            hull=state.hull,
        )

        for day in range(1, max_days + 1):
            sim.oxygen -= self.daily_rates["oxygen"]
            sim.power -= self.daily_rates["power"]
            sim.food -= self.daily_rates["food"]
            sim.fuel -= self.daily_rates["fuel"]
            sim.hull -= self.daily_rates["hull"]

            if sim.oxygen <= 0:
                return ("Oxygen", day)
            if sim.power <= 0:
                return ("Power", day)
            if sim.food <= 0:
                return ("Food", day)
            if sim.fuel <= 0:
                return ("Fuel", day)
            if sim.hull <= 0:
                return ("Hull Integrity", day)

        return ("None", max_days)

    def estimate_survival_probability(self, state: MissionState, goal_days: int):
        """Rough probability score based on whether resources can last to the goal."""
        sim = MissionState(
            oxygen=state.oxygen,
            power=state.power,
            food=state.food,
            fuel=state.fuel,
            hull=state.hull,
        )

        for _ in range(goal_days):
            sim.oxygen -= self.daily_rates["oxygen"]
            sim.power -= self.daily_rates["power"]
            sim.food -= self.daily_rates["food"]
            sim.fuel -= self.daily_rates["fuel"]
            sim.hull -= self.daily_rates["hull"]

        if min(sim.oxygen, sim.power, sim.food, sim.fuel, sim.hull) <= 0:
            return 25

        floor = min(sim.oxygen, sim.power, sim.food, sim.fuel, sim.hull)
        return max(35, min(95, floor))

    def simulate_tick(
        self,
        state: MissionState,
        cargo: CargoInventory,
        speed: int,
        autopilot: bool,
    ):
        """Apply one simulation tick: drains, recharge, and optional drone actions."""
        events = []

        # Drain per tick (scaled from daily rates).
        factor = 0.1 * max(1, speed)
        state.oxygen -= self.daily_rates["oxygen"] * factor
        state.power -= self.daily_rates["power"] * factor
        state.food -= self.daily_rates["food"] * factor
        state.fuel -= self.daily_rates["fuel"] * factor
        state.hull -= self.daily_rates["hull"] * factor

        # Passive solar recharge.
        state.power += 2.0 * factor

        if state.power < 20:
            state.hull -= 0.5 * factor

        if autopilot:
            # Emergency power boost.
            if state.power < 30 and cargo.power_reserve > 0:
                amount = min(20, cargo.power_reserve, 100 - state.power)
                if amount > 0:
                    cargo.power_reserve -= amount
                    state.power += amount
                    events.append(f"Drone used power cell (+{amount}% Power)")

            # Resource top-offs if power is stable.
            if state.power >= 20:
                state, cargo, drop_events = self._deploy_supplies(state, cargo)
                events.extend(drop_events)

            # Hull repair if needed.
            if state.hull < 60 and cargo.hull_plates > 0 and state.power >= 30:
                amount = min(15, cargo.hull_plates, 100 - state.hull)
                if amount > 0:
                    cargo.hull_plates -= amount
                    state.hull += amount
                    state.power -= 5
                    events.append(f"Drone repaired hull (+{amount}% Hull)")

        # Clamp values to 0..100
        state.oxygen = self._clamp(state.oxygen)
        state.power = self._clamp(state.power)
        state.food = self._clamp(state.food)
        state.fuel = self._clamp(state.fuel)
        state.hull = self._clamp(state.hull)
        cargo.oxygen_reserve = self._clamp(cargo.oxygen_reserve)
        cargo.power_reserve = self._clamp(cargo.power_reserve)
        cargo.food_reserve = self._clamp(cargo.food_reserve)
        cargo.fuel_reserve = self._clamp(cargo.fuel_reserve)
        cargo.hull_plates = self._clamp(cargo.hull_plates)

        return state, cargo, events

    def _deploy_supplies(self, state: MissionState, cargo: CargoInventory):
        events = []

        if state.oxygen < 35 and cargo.oxygen_reserve > 0:
            amount = min(20, cargo.oxygen_reserve, 100 - state.oxygen)
            cargo.oxygen_reserve -= amount
            state.oxygen += amount
            state.power -= 3
            events.append(f"Drone deployed oxygen canister (+{amount}% O2)")

        if state.food < 35 and cargo.food_reserve > 0:
            amount = min(20, cargo.food_reserve, 100 - state.food)
            cargo.food_reserve -= amount
            state.food += amount
            state.power -= 3
            events.append(f"Drone deployed food pack (+{amount}% Food)")

        if state.fuel < 35 and cargo.fuel_reserve > 0:
            amount = min(20, cargo.fuel_reserve, 100 - state.fuel)
            cargo.fuel_reserve -= amount
            state.fuel += amount
            state.power -= 4
            events.append(f"Drone deployed fuel cell (+{amount}% Fuel)")

        return state, cargo, events

    def generate_strategy(
        self,
        state: MissionState,
        cargo: CargoInventory,
        goal_text: str,
        goal_days: int,
        autopilot: bool,
        last_events: list[str],
    ):
        """IF-THEN goal-based strategy generator."""
        actions = []

        if state.power < 20:
            actions.append(
                "Emergency: Shutdown science lab and reroute power to life support."
            )
        elif state.power < 40:
            actions.append("Reduce non-essential systems to conserve power.")

        if state.oxygen < 25:
            actions.append("Activate oxygen recycling and reduce crew activity.")
        elif state.oxygen < 50:
            actions.append("Optimize life-support cycles to preserve oxygen.")

        if state.food < 30:
            actions.append("Implement rationing protocol and shift to nutrient packs.")

        if state.fuel < 35:
            actions.append("Adjust trajectory to minimize fuel consumption.")

        if state.hull < 50:
            actions.append("Deploy repair drones and reduce external maneuvers.")

        if not actions:
            actions.append("Maintain current operations and monitor systems closely.")

        failure_resource, failure_day = self.predict_failure_point(state)
        survival = self.estimate_survival_probability(state, goal_days)

        summary = [
            f"Goal: {goal_text} (target: {goal_days} days)",
            f"Projected failure point: {failure_resource} in {failure_day} days",
            f"Estimated survival probability: {survival}%",
            f"Autonomous Drone: {'Active' if autopilot else 'Standby'}",
            "",
            "Cargo Reserves:",
            f"- Oxygen: {cargo.oxygen_reserve}%",
            f"- Power Cells: {cargo.power_reserve}%",
            f"- Food: {cargo.food_reserve}%",
            f"- Fuel: {cargo.fuel_reserve}%",
            f"- Hull Plates: {cargo.hull_plates}%",
            "",
            "Mission Command Strategy:",
        ]
        summary.extend([f"- {action}" for action in actions])

        if last_events:
            summary.append("")
            summary.append("Drone Actions (last tick):")
            summary.extend([f"- {event}" for event in last_events])

        return "\n".join(summary)
