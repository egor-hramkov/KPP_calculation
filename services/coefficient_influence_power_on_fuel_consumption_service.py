from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class CoefficientInfluencePowerOnFuelConsumptionService:
    torque_on_wheel_dataset:DataFrame
    air_resistance_dataset:DataFrame


    def __post_init__(self):
        self.frequency_array = self.torque_on_wheel_dataset['frequency_turns_per_min'].to_numpy()
        self.torque_on_wheel_hub1 = self.torque_on_wheel_dataset['hub1'].to_numpy()
        self.torque_on_wheel_hub2 = self.torque_on_wheel_dataset['hub2'].to_numpy()
        self.torque_on_wheel_hub3 = self.torque_on_wheel_dataset['hub3'].to_numpy()
        self.torque_on_wheel_hub4 = self.torque_on_wheel_dataset['hub4'].to_numpy()
        self.torque_on_wheel_hub5 = self.torque_on_wheel_dataset['hub5'].to_numpy()
        self.air_resistance_hub1 = self.air_resistance_dataset['hub1'].to_numpy()
        self.air_resistance_hub2 = self.air_resistance_dataset['hub2'].to_numpy()
        self.air_resistance_hub3 = self.air_resistance_dataset['hub3'].to_numpy()
        self.air_resistance_hub4 = self.air_resistance_dataset['hub4'].to_numpy()
        self.air_resistance_hub5 = self.air_resistance_dataset['hub5'].to_numpy()

    @property
    def coefs_hub1(self):
        return self.__calculate_coefs_hub(self.torque_on_wheel_hub1, self.air_resistance_hub1)

    @property
    def coefs_hub2(self):
        return self.__calculate_coefs_hub(self.torque_on_wheel_hub2, self.air_resistance_hub2)

    @property
    def coefs_hub3(self):
        return self.__calculate_coefs_hub(self.torque_on_wheel_hub3, self.air_resistance_hub3)

    @property
    def coefs_hub4(self):
        return self.__calculate_coefs_hub(self.torque_on_wheel_hub4, self.air_resistance_hub4)

    @property
    def coefs_hub5(self):
        return self.__calculate_coefs_hub(self.torque_on_wheel_hub5, self.air_resistance_hub5)

    def __calculate_coefs_hub(self, torque_on_wheel_hub, air_resistance_hub):
        coefs = []
        for torque, air_resistance in zip(torque_on_wheel_hub, air_resistance_hub):
            coef = 3.27-8.22*(air_resistance/torque)+9.13*((air_resistance/torque)**2)-3.18*((air_resistance/torque)**3)
            coefs.append(coef)
        return coefs
