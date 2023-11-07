from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class FuelConsumptionService:
    """Сервис по расчёту расхода топлива автомобиля"""
    influence_turnovers_of_fuel_consumption_dataset:DataFrame
    influence_power_on_fuel_consumption_dataset:DataFrame
    air_resistance_dataset:DataFrame


    def __post_init__(self):
        self.frequency_array =self.influence_turnovers_of_fuel_consumption_dataset['Частота об/м'].to_numpy()
        self.coefs_tutnoverse_on_fuel=self.influence_turnovers_of_fuel_consumption_dataset['Коэффиценты'].to_numpy()
        self.coefs_power_on_fuel_hub1=self.influence_power_on_fuel_consumption_dataset['Передача 1'].to_numpy()
        self.coefs_power_on_fuel_hub2=self.influence_power_on_fuel_consumption_dataset['Передача 2'].to_numpy()
        self.coefs_power_on_fuel_hub3=self.influence_power_on_fuel_consumption_dataset['Передача 3'].to_numpy()
        self.coefs_power_on_fuel_hub4=self.influence_power_on_fuel_consumption_dataset['Передача 4'].to_numpy()
        self.coefs_power_on_fuel_hub5=self.influence_power_on_fuel_consumption_dataset['Передача 5'].to_numpy()
        self.air_resistance_hub1=self.air_resistance_dataset['hub1'].to_numpy()
        self.air_resistance_hub2=self.air_resistance_dataset['hub2'].to_numpy()
        self.air_resistance_hub3=self.air_resistance_dataset['hub3'].to_numpy()
        self.air_resistance_hub4=self.air_resistance_dataset['hub4'].to_numpy()
        self.air_resistance_hub5=self.air_resistance_dataset['hub5'].to_numpy()

    @property
    def fuel_consumption_hub1(self):
        return self.__calculate_fuel_consumption_hub(self.coefs_power_on_fuel_hub1, self.air_resistance_hub1)

    @property
    def fuel_consumption_hub2(self):
        return self.__calculate_fuel_consumption_hub(self.coefs_power_on_fuel_hub2, self.air_resistance_hub2)

    @property
    def fuel_consumption_hub3(self):
        return self.__calculate_fuel_consumption_hub(self.coefs_power_on_fuel_hub3, self.air_resistance_hub3)

    @property
    def fuel_consumption_hub4(self):
        return self.__calculate_fuel_consumption_hub(self.coefs_power_on_fuel_hub4, self.air_resistance_hub4)

    @property
    def fuel_consumption_hub5(self):
        return self.__calculate_fuel_consumption_hub(self.coefs_power_on_fuel_hub5, self.air_resistance_hub5)

    def __calculate_fuel_consumption_hub(self,coefs_power_on_fuel_hub, air_resistance_hub):
        consumptions=[]
        for coef_turnoverse, coef_power, air_resistance in zip(self.coefs_tutnoverse_on_fuel, coefs_power_on_fuel_hub, air_resistance_hub):
            consumptions.append(coef_power*270/(36000*0.73)*air_resistance)
        return consumptions
