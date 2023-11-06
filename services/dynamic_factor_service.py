from dataclasses import dataclass

import numpy
from pandas import DataFrame


@dataclass
class DynamicFactor:
    km_per_hour_array: numpy.array
    speed_car_dataset: DataFrame
    polynom_dataset: DataFrame

    def __post_init__(self):
        self.min_frequency = self.speed_car_dataset['frequency'][0]
        self.min_speed_hub1 = self.speed_car_dataset['hub1'][0]
        self.min_speed_hub2 = self.speed_car_dataset['hub2'][0]
        self.min_speed_hub3 = self.speed_car_dataset['hub3'][0]
        self.min_speed_hub4 = self.speed_car_dataset['hub4'][0]
        self.min_speed_hub5 = self.speed_car_dataset['hub5'][0]
        self.coef_moment_5 = self.polynom_dataset['X/5'][0]
        self.coef_moment_4 = self.polynom_dataset['X/4'][0]
        self.coef_moment_3 = self.polynom_dataset['X/3'][0]
        self.coef_moment_2 = self.polynom_dataset['X/2'][0]
        self.coef_moment_1 = self.polynom_dataset['X'][0]
        self.coef_moment_1 = self.polynom_dataset['X'][0]
        self.coef_self = self.polynom_dataset['Собственный коэффициент'][0]