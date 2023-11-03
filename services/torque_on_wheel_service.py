from pandas import DataFrame


@dataclass
class TorqueOnWheelService:
    power_and_torque_data_set: DataFrame

