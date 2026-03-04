from dataclasses import dataclass


@dataclass
class MissionState:
    oxygen: int
    power: int
    food: int
    fuel: int
    hull: int


@dataclass
class CargoInventory:
    oxygen_reserve: int
    power_reserve: int
    food_reserve: int
    fuel_reserve: int
    hull_plates: int
