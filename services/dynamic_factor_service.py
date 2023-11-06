from dataclasses import dataclass

import numpy
from pandas import DataFrame


@dataclass
class DynamicFactorService:
    km_per_hour_array: numpy.array
    speed_car_dataset: DataFrame
    polynom_dataset: DataFrame
    wheel_info_dataset:DataFrame
    dependence_torque_on_air_resistance_dataset:DataFrame


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
        self.dynamic_radius = self.wheel_info_dataset['Ширина профиля'][3]

    @property
    def turnovers_hub1(self):
        return self.__calculate_turnovers_hub(1, 30, self.min_speed_hub1)

    @property
    def turnovers_hub2(self):
        return self.__calculate_turnovers_hub(10, 55, self.min_speed_hub2)

    @property
    def turnovers_hub3(self):
        return self.__calculate_turnovers_hub(15, 90, self.min_speed_hub3)

    @property
    def turnovers_hub4(self):
        return self.__calculate_turnovers_hub(20, 130, self.min_speed_hub4)

    @property
    def turnovers_hub5(self):
        return self.__calculate_turnovers_hub(25, 150, self.min_speed_hub5)

    @property
    def torque_hub1(self):
        return 1

    @property
    def torque_hub1(self):
        return 1

    @property
    def torque_hub1(self):
        return 1

    @property
    def torque_hub1(self):
        return 1

    @property
    def torque_hub1(self):
        return 1
    def __calculate_turnovers_hub(self, min_speed, max_speed, min_speed_hub):
        turnovers=[]
        for speed in self.km_per_hour_array:
            if min_speed<=speed<=max_speed:
                turnovers.append((self.min_frequency/min_speed_hub)*speed)
            else:
                turnovers.append('-')