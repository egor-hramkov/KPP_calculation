from dataclasses import dataclass

from matplotlib import pyplot as plt


@dataclass
class CoefficientTurnoversToFuelService:
    """Рассчитывает коэффициент влияния оборотов двигатея на расход топлива"""
    frequency_turns_per_min: list

    def __post_init__(self):
        self.coefficients = self.__calculate_coefficients()
        self.show_graphic()

    def __calculate_coefficients(self) -> list:
        coefficients = []
        for frequency in self.frequency_turns_per_min:
            coef = 1.25 - 0.99 * (frequency / self.frequency_turns_per_min[-1]) + 0.98 * \
                (frequency / self.frequency_turns_per_min[-1]) ** 2 - 0.24 * (frequency / self.frequency_turns_per_min[-1]) ** 3
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
