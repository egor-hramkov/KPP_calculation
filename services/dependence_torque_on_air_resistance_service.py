from dataclasses import dataclass

import numpy
from pandas import DataFrame


@dataclass
class DependenceOfTorqueOnAirResistanceService:
    km_per_hour_array: numpy.array
    dimensions_dataset: DataFrame
    speed_car_dataset: DataFrame
    polynom_dataset: DataFrame

    def __post_init__(self):
        self.midelev_section=self.dimensions_dataset['midelev_cross_sectional_area'][1]
        self.coef_streamlining=self.dimensions_dataset['streamline_coefficient'][1]
        self.min_frequency_turns = self.speed_car_dataset['frequency'][0]
        self.min_speed_hub1 = self.speed_car_dataset['hub1'][0]
        self.min_speed_hub2 = self.speed_car_dataset['hub2'][0]
        self.min_speed_hub3 = self.speed_car_dataset['hub3'][0]
        self.min_speed_hub4 = self.speed_car_dataset['hub4'][0]
        self.min_speed_hub5 = self.speed_car_dataset['hub5'][0]

    @property
    def air_resistance(self):
        self.__calculate_air_resistance()

    @property
    def turnovers_hub1(self):
        return self.__calculate_turnovers_hub(1,30, self.min_speed_hub1)

    @property
    def turnovers_hub2(self):
        return self.__calculate_turnovers_hub(1, 30, self.min_speed_hub2)

    @property
    def turnovers_hub3(self):
        return self.__calculate_turnovers_hub(1, 30, self.min_speed_hub3)

    @property
    def turnovers_hub4(self):
        return self.__calculate_turnovers_hub(1, 30, self.min_speed_hub4)

    @property
    def turnovers_hub5(self):
        return self.__calculate_turnovers_hub(1, 30, self.min_speed_hub5)



    def __calculate_air_resistance(self):
        air_resistance=[]
        for speed in self.km_per_hour_array:
            air_resistance.append(0.5*self.midelev_section*self.coef_streamlining*1.22*((speed/3.6)**2))
        return air_resistance

    def __calculate_turnovers_hub(self, min_speed, max_speed, min_speed_hub):
        turnovers_hub=[]
        for speed in self.km_per_hour_array:
            if min_speed <= speed <= max_speed:
                turnovers_hub.append((self.min_frequency_turns/min_speed_hub)*speed)
            else:
                turnovers_hub.append('-')
        return turnovers_hub
