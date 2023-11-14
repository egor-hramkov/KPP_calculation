from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class InfluencePowerOnFuelConsumptionService:
    torque_on_wheel_dataset: DataFrame


    def __post_init__(self):
        return 1
