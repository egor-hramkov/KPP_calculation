from dataclasses import dataclass

from matplotlib import pyplot as plt
from pandas import DataFrame


@dataclass
class FuelConsumptionService:
    """Сервис по расчёту расхода топлива автомобиля"""
    influence_turnovers_of_fuel_consumption_dataset: DataFrame
    influence_power_on_fuel_consumption_dataset: DataFrame
    air_resistance_dataset: DataFrame
    frequency_turns_per_min: list

    def __post_init__(self):
        self.frequency_array = self.influence_turnovers_of_fuel_consumption_dataset['Частота об/м'].to_numpy()
        self.coefs_tutnoverse_on_fuel = self.influence_turnovers_of_fuel_consumption_dataset['Коэффиценты'].to_numpy()
        self.coefs_power_on_fuel_hub1 = self.influence_power_on_fuel_consumption_dataset['Передача 1'].to_numpy()
        self.coefs_power_on_fuel_hub2 = self.influence_power_on_fuel_consumption_dataset['Передача 2'].to_numpy()
        self.coefs_power_on_fuel_hub3 = self.influence_power_on_fuel_consumption_dataset['Передача 3'].to_numpy()
        self.coefs_power_on_fuel_hub4 = self.influence_power_on_fuel_consumption_dataset['Передача 4'].to_numpy()
        self.coefs_power_on_fuel_hub5 = self.influence_power_on_fuel_consumption_dataset['Передача 5'].to_numpy()
        self.air_resistance_hub1 = self.air_resistance_dataset['Передача 1'].to_numpy()
        self.air_resistance_hub2 = self.air_resistance_dataset['Передача 2'].to_numpy()
        self.air_resistance_hub3 = self.air_resistance_dataset['Передача 3'].to_numpy()
        self.air_resistance_hub4 = self.air_resistance_dataset['Передача 4'].to_numpy()
        self.air_resistance_hub5 = self.air_resistance_dataset['Передача 5'].to_numpy()
        self.show_graphic()

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

    def __calculate_fuel_consumption_hub(self, coefs_power_on_fuel_hub, air_resistance_hub):
        consumptions = []
        for coef_turnoverse, coef_power, air_resistance in zip(self.coefs_tutnoverse_on_fuel, coefs_power_on_fuel_hub,
                                                               air_resistance_hub):
            consumptions.append(coef_power * 270 / (36000 * 0.73) * air_resistance)
        return consumptions

    def show_graphic(self):
        """Отрисовывает график расхода топлива автомобиля"""
        plt.xlabel("Частота, об/мин")
        plt.title('Расход топлива автомобиля')
        plt.plot(self.frequency_turns_per_min, self.fuel_consumption_hub1, label='1 передача')
        plt.plot(self.frequency_turns_per_min, self.fuel_consumption_hub2, label='2 передача')
        plt.plot(self.frequency_turns_per_min, self.fuel_consumption_hub3, label='3 передача')
        plt.plot(self.frequency_turns_per_min, self.fuel_consumption_hub4, label='4 передача')
        plt.plot(self.frequency_turns_per_min, self.fuel_consumption_hub5, label='5 передача')
        plt.legend()
        plt.grid(axis='y')
        plt.show()
