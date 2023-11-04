from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class DependenceOfTorqueOnAirResistance:
    air_resistance_dataset:DataFrame


