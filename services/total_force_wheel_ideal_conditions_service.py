from dataclasses import dataclass

import numpy
from pandas import DataFrame


@dataclass
class TotalForceWheelIdealConditionsService:
    km_per_hour_array: numpy.array
    rolling_resistance_dataset:DataFrame
    speed_car_dataset:DataFrame
    polynom_dataset: DataFrame
    dependence_torque_on_air_resistance_dataset:DataFrame

    def __post_init__(self):
        self.rolling_resistance_array=self.rolling_resistance_dataset['1.Хорошее состояние сухого асфальта'].to_numpy()
        self.min_frequency = self.speed_car_dataset['frequency'][0]
        self.min_speed_hub1= self.speed_car_dataset['hub1'][0]
        self.min_speed_hub2= self.speed_car_dataset['hub2'][0]
        self.min_speed_hub3= self.speed_car_dataset['hub3'][0]
        self.min_speed_hub4= self.speed_car_dataset['hub4'][0]
        self.min_speed_hub5= self.speed_car_dataset['hub5'][0]
        self.frequency_array = self.speed_car_dataset['frequency'].to_numpy()
        self.speed_hub1_array=self.speed_car_dataset['hub1'].to_numpy()
        self.speed_hub2_array=self.speed_car_dataset['hub2'].to_numpy()
        self.speed_hub3_array=self.speed_car_dataset['hub3'].to_numpy()
        self.speed_hub4_array=self.speed_car_dataset['hub4'].to_numpy()
        self.speed_hub5_array=self.speed_car_dataset['hub5'].to_numpy()
        self.coef_moment_5 = self.polynom_dataset['X/5'][0]
        self.coef_moment_4 = self.polynom_dataset['X/4'][0]
        self.coef_moment_3 = self.polynom_dataset['X/3'][0]
        self.coef_moment_2 = self.polynom_dataset['X/2'][0]
        self.coef_moment_1 = self.polynom_dataset['X'][0]
        self.coef_moment_1 = self.polynom_dataset['X'][0]
        self.air_resistance_array = self.dependence_torque_on_air_resistance_dataset['Сопротивление воздуха'].to_numpy()
        self.coef_self = self.polynom_dataset['Собственный коэффициент'][0]



    @property
    def turnovers_hub1(self):
        return self.__calculate_turnovers_hub(1,30,self.min_speed_hub1)

    @property
    def turnovers_hub2(self):
        return self.__calculate_turnovers_hub(10,55,self.min_speed_hub2)

    @property
    def turnovers_hub3(self):
        return self.__calculate_turnovers_hub(15,90,self.min_speed_hub3)

    @property
    def turnovers_hub4(self):
        return self.__calculate_turnovers_hub(20,125,self.min_speed_hub4)

    @property
    def turnovers_hub5(self):
        return self.__calculate_turnovers_hub(25,150,self.min_speed_hub5)

    @property
    def force_on_wheel_hub1(self):
        return self.__calculate_force_on_wheel(self.turnovers_hub1)

    @property
    def force_on_wheel_hub2(self):
        return self.__calculate_force_on_wheel(self.turnovers_hub2)

    @property
    def force_on_wheel_hub3(self):
        return self.__calculate_force_on_wheel(self.turnovers_hub3)

    @property
    def force_on_wheel_hub4(self):
        return self.__calculate_force_on_wheel(self.turnovers_hub4)

    @property
    def force_on_wheel_hub5(self):
        return self.__calculate_force_on_wheel(self.turnovers_hub5)





    def __calculate_turnovers_hub(self, min_speed, max_speed, min_speed_hub):
        turnovers=[]
        for speed in self.km_per_hour_array:
            if min_speed <= speed <= max_speed:
                turnovers.append((self.min_frequency/min_speed_hub)*speed)
            else:
                turnovers.append('-')
        return turnovers

    def __calculate_force_on_wheel(self, turnovers_hub):
        force_on_wheel=[]
        for turnovers in turnovers_hub:
            if turnovers=='-':
                force_on_wheel.append('-')
            else:
                force=(self.coef_moment_5*(turnovers**5)+self.coef_moment_4*(turnovers**4)+self.coef_moment_3*(turnovers**3)+self.coef_moment_2*(turnovers**2)+self.coef_moment_1*turnovers+self.coef_self)
                force_on_wheel.append(force)
        return force_on_wheel