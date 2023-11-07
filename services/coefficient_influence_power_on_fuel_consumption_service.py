from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class CoefficientInfluencePowerOnFuelConsumptionService:
    torque_on_wheel_dataset:DataFrame