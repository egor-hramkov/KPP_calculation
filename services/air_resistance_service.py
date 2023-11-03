from dataclasses import dataclass, field

from pandas import DataFrame


@dataclass
class AirResistanceService:
    """Рассчёт габаритных размеров"""
    width: float
    height: float
    streamline_coefficient: float
    speed_car_data_frame: DataFrame

    def __post_init__(self):
        self.midelev_cross_sectional_area = self.width * self.height * 0.79
        self.turnovers_hub1 = self.turnovers_wheel_data_frame.iloc[:,
                              1].to_numpy()  # массив кол-ва оборотов колеса на 1 скорости
        self.turnovers_hub2 = self.turnovers_wheel_data_frame.iloc[:,
                              2].to_numpy()  # массив кол-ва оборотов колеса на 2 скорости
        self.turnovers_hub3 = self.turnovers_wheel_data_frame.iloc[:,
                              3].to_numpy()  # массив кол-ва оборотов колеса на 3 скорости
        self.turnovers_hub4 = self.turnovers_wheel_data_frame.iloc[:,
                              4].to_numpy()  # массив кол-ва оборотов колеса на 4 скорости
        self.turnovers_hub5 = self.turnovers_wheel_data_frame.iloc[:, 5].to_numpy()

