from dataclasses import dataclass

from matplotlib import pyplot as plt
from pandas import DataFrame


@dataclass
class CoefficientTurnoversToFuelService:
    """Рассчитывает коэффициент влияния оборотов двигатея на расход топлива"""
    frequency_turns_per_min: list
    coefficient_influence_power_on_fuel_consumption_data: DataFrame
    total_force_wheel_ideal_conditions_data: DataFrame

    def __post_init__(self):
        self.coefficients = self.__calculate_coefficients()
        self.show_graphic()
        self.coefficient_influence_power_on_fuel_consumption_hub1=self.coefficient_influence_power_on_fuel_consumption_data['Передача 1']
        self.coefficient_influence_power_on_fuel_consumption_hub2=self.coefficient_influence_power_on_fuel_consumption_data['Передача 2']
        self.coefficient_influence_power_on_fuel_consumption_hub3=self.coefficient_influence_power_on_fuel_consumption_data['Передача 3']
        self.coefficient_influence_power_on_fuel_consumption_hub4=self.coefficient_influence_power_on_fuel_consumption_data['Передача 4']
        self.coefficient_influence_power_on_fuel_consumption_hub5=self.coefficient_influence_power_on_fuel_consumption_data['Передача 5']
        self.total_force_wheel_ideal_conditions_hub1=self.total_force_wheel_ideal_conditions_data['d']


    def __calculate_coefficients(self) -> list:
        coefficients = []
        for frequency in self.frequency_turns_per_min:
            coef = 1.25 - 0.99 * (frequency / self.frequency_turns_per_min[-1]) + 0.98 * \
                   (frequency / self.frequency_turns_per_min[-1]) ** 2 - 0.24 * (
                               frequency / self.frequency_turns_per_min[-1]) ** 3
            coefficients.append(coef)
        return coefficients

    def show_graphic(self):
        """График коэффициента влияния оборотов двигателя на расход топлива"""
        plt.xlabel("Частота, об/мин")
        plt.title('Коэффициент влияния оборотов двигателя на расход топлива')
        plt.plot(self.frequency_turns_per_min, self.coefficients)
        plt.legend()
        plt.grid(axis='y')
        plt.show()
