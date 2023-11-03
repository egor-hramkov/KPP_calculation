from dataclasses import dataclass


@dataclass
class TurnoversWheelsService:
    full_gear_ratio_hub1: float
    full_gear_ratio_hub2: float
    full_gear_ratio_hub3: float
    full_gear_ratio_hub4: float
    full_gear_ratio_hub5: float
    full_gear_ratio_reverse: float
    frequency_turns_per_min: list

    @property
    def turnovers_wheels_hub1(self):
        return self.__calculate_turnovers_wheels_array(self.full_gear_ratio_hub1)

    @property
    def turnovers_wheels_hub2(self):
        return self.__calculate_turnovers_wheels_array(self.full_gear_ratio_hub2)

    @property
    def turnovers_wheels_hub3(self):
        return self.__calculate_turnovers_wheels_array(self.full_gear_ratio_hub3)

    @property
    def turnovers_wheels_hub4(self):
        return self.__calculate_turnovers_wheels_array(self.full_gear_ratio_hub4)

    @property
    def turnovers_wheels_hub5(self):
        return self.__calculate_turnovers_wheels_array(self.full_gear_ratio_hub5)

    @property
    def turnovers_wheels_reverse(self):
        return self.__calculate_turnovers_wheels_array(self.full_gear_ratio_reverse)

    def __calculate_turnovers_wheels_array(self, full_gear_ratio: float):
        """"Возвращает массив оборотов колеса в минуту относительно частоты оборотов двигателя и номера передачи"""
        gear_ratio_array = []
        for frequency in self.frequency_turns_per_min:
            gear_ratio = frequency / full_gear_ratio
            gear_ratio_array.append(gear_ratio)
        return gear_ratio_array
