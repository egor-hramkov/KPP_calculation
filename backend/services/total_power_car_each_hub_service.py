from dataclasses import dataclass

import numpy
from pandas import DataFrame


@dataclass
class TotalPowerCarEachHubService:
    frequency_turns_per_min: numpy.array
    torque_on_wheel_dataset: DataFrame
    total_force_resistance_movement_dataset: DataFrame

    def __post_init__(self):
        self.torque_on_wheel_hub1 = self.torque_on_wheel_dataset['Передача 1']
        self.torque_on_wheel_hub2 = self.torque_on_wheel_dataset['Передача 2']
        self.torque_on_wheel_hub3 = self.torque_on_wheel_dataset['Передача 3']
        self.torque_on_wheel_hub4 = self.torque_on_wheel_dataset['Передача 4']
        self.torque_on_wheel_hub5 = self.torque_on_wheel_dataset['Передача 5']
        self.total_force_resistance_movement_hub1 = self.total_force_resistance_movement_dataset['1 передача']
        self.total_force_resistance_movement_hub2 = self.total_force_resistance_movement_dataset['2 передача']
        self.total_force_resistance_movement_hub3 = self.total_force_resistance_movement_dataset['3 передача']
        self.total_force_resistance_movement_hub4 = self.total_force_resistance_movement_dataset['4 передача']
        self.total_force_resistance_movement_hub5 = self.total_force_resistance_movement_dataset['5 передача']

    @property
    def total_power_car_each_hub1(self):
        return self.__calculate_total_power_car_each_hub(self.torque_on_wheel_hub1,
                                                         self.total_force_resistance_movement_hub1)

    @property
    def total_power_car_each_hub2(self):
        return self.__calculate_total_power_car_each_hub(self.torque_on_wheel_hub2,
                                                         self.total_force_resistance_movement_hub3)

    @property
    def total_power_car_each_hub3(self):
        return self.__calculate_total_power_car_each_hub(self.torque_on_wheel_hub3,
                                                         self.total_force_resistance_movement_hub3)

    @property
    def total_power_car_each_hub4(self):
        return self.__calculate_total_power_car_each_hub(self.torque_on_wheel_hub4,
                                                         self.total_force_resistance_movement_hub4)

    @property
    def total_power_car_each_hub5(self):
        return self.__calculate_total_power_car_each_hub(self.torque_on_wheel_hub5,
                                                         self.total_force_resistance_movement_hub5)

    def __calculate_total_power_car_each_hub(self, torque_on_wheel_hub, total_force_resistance_movement_hub):
        totals = []
        for torque_on_wheel, total_force_resistance_movement in zip(torque_on_wheel_hub,
                                                                    total_force_resistance_movement_hub):
            totals.append(torque_on_wheel - total_force_resistance_movement)
        return totals
