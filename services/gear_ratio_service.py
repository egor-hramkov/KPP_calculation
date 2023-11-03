from dataclasses import dataclass


@dataclass
class GearRatioService:
    """Сервис по высчитыванию полного передаточного числа для каждой передачи"""
    gear_ratio_hub1: float
    gear_ratio_hub2: float
    gear_ratio_hub3: float
    gear_ratio_hub4: float
    gear_ratio_hub5: float
    gear_ratio_reverse: float
    transfer_case: float
    on_board_gearbox: float
    main_pair: float

    @property
    def full_gear_ratio_hub1(self):
        return self.gear_ratio_hub1 * self.main_pair

    @property
    def full_gear_ratio_hub2(self):
        return self.gear_ratio_hub2 * self.main_pair

    @property
    def full_gear_ratio_hub3(self):
        return self.gear_ratio_hub3 * self.main_pair

    @property
    def full_gear_ratio_hub4(self):
        return self.gear_ratio_hub4 * self.main_pair

    @property
    def full_gear_ratio_hub5(self):
        return self.gear_ratio_hub5 * self.main_pair

    @property
    def full_gear_ratio_reverse(self):
        return self.gear_ratio_reverse * self.main_pair
