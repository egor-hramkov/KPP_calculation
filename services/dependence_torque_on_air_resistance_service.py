from dataclasses import dataclass

import numpy
from pandas import DataFrame


@dataclass
class DependenceOfTorqueOnAirResistanceService:
    km_per_hour_array: numpy.array
    dimensions_dataset: DataFrame
    speed_car_dataset: DataFrame
    polynom_dataset: DataFrame
    gear_ratio_dataset: DataFrame
    kpd_dataset: DataFrame

    def __post_init__(self):
        self.midelev_section = self.dimensions_dataset['midelev_cross_sectional_area'][1]
        self.coef_streamlining = self.dimensions_dataset['streamline_coefficient'][1]
        self.min_frequency_turns = self.speed_car_dataset['frequency'][0]
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
        self.full_gear_ratio_hub1 = self.gear_ratio_dataset['full_gear_ratio'][0]
        self.full_gear_ratio_hub2 = self.gear_ratio_dataset['full_gear_ratio'][1]
        self.full_gear_ratio_hub3 = self.gear_ratio_dataset['full_gear_ratio'][2]
        self.full_gear_ratio_hub4 = self.gear_ratio_dataset['full_gear_ratio'][3]
        self.full_gear_ratio_hub5 = self.gear_ratio_dataset['full_gear_ratio'][4]
        self.full_gear_ratio_reverse = self.gear_ratio_dataset['full_gear_ratio'][5]
        self.kpd_hub1 = self.kpd_dataset['KPD'][0]
        self.kpd_hub2 = self.kpd_dataset['KPD'][1]
        self.kpd_hub3 = self.kpd_dataset['KPD'][2]
        self.kpd_hub4 = self.kpd_dataset['KPD'][3]
        self.kpd_hub5 = self.kpd_dataset['KPD'][4]

    @property
    def air_resistance(self):
        return self.__calculate_air_resistance()

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
        return self.__calculate_torque_hub(self.turnovers_hub1,self.full_gear_ratio_hub1,self.kpd_hub1)

    @property
    def torque_hub2(self):
        return self.__calculate_torque_hub(self.turnovers_hub2,self.full_gear_ratio_hub2,self.kpd_hub2)

    @property
    def torque_hub3(self):
        return self.__calculate_torque_hub(self.turnovers_hub3,self.full_gear_ratio_hub3,self.kpd_hub3)

    @property
    def torque_hub4(self):
        return self.__calculate_torque_hub(self.turnovers_hub4,self.full_gear_ratio_hub4,self.kpd_hub4)

    @property
    def torque_hub5(self):
        return self.__calculate_torque_hub(self.turnovers_hub5,self.full_gear_ratio_hub5,self.kpd_hub5)

    def __calculate_air_resistance(self):
        air_resistance = []
        for speed in self.km_per_hour_array:
            air_resistance.append(0.5 * self.midelev_section * self.coef_streamlining * 1.22 * ((speed / 3.6) ** 2))
        return air_resistance

    def __calculate_turnovers_hub(self, min_speed, max_speed, min_speed_hub):
        turnovers_hub = []
        for speed in self.km_per_hour_array:
            if min_speed <= speed <= max_speed:
                turnovers_hub.append((self.min_frequency_turns / min_speed_hub) * speed)
            else:
                turnovers_hub.append('-')
        return turnovers_hub

    def __calculate_torque_hub(self, turnovers_hub_list, full_gear_ratio_hub, kpd_hub):
        torques = []
        for turnover in turnovers_hub_list:
            if turnover == '-':
                torques.append('-')
            else:
                torque = ((self.coef_moment_5 * (turnover ** 5)) + (self.coef_moment_4 * (turnover ** 4)) + (
                            self.coef_moment_3 * (turnover ** 3)) + (self.coef_moment_2 * (turnover ** 2)) + (
                                      self.coef_moment_1 * turnover) + self.coef_self) * full_gear_ratio_hub * kpd_hub
                torques.append(torque)
        return torques
