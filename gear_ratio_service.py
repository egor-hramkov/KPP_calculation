from dataclasses import dataclass


@dataclass
class GearRatioService:
    hub1: float
    hub2: float
    hub3: float
    hub4: float
    hub5: float
    hub_reverse: float
    transfer_case: float
    on_board_gearbox: float
    main_pair: float
    frequency_turns_per_min: list

    @property
    def gear_ratio_hub1(self):
        return self.__make_gear_ratio_array(self.hub1)

    @property
    def gear_ratio_hub2(self):
        return self.__make_gear_ratio_array(self.hub2)

    @property
    def gear_ratio_hub3(self):
        return self.__make_gear_ratio_array(self.hub3)

    @property
    def gear_ratio_hub4(self):
        return self.__make_gear_ratio_array(self.hub4)

    @property
    def gear_ratio_hub5(self):
        return self.__make_gear_ratio_array(self.hub5)

    @property
    def gear_ratio_hub_reverse(self):
        return self.__make_gear_ratio_array(self.hub_reverse)

    def __make_gear_ratio_array(self, hub: float):
        gear_ratio_array = []
        for frequency in self.frequency_turns_per_min:
            gear_ratio = frequency / (hub * self.transfer_case * self.on_board_gearbox * self.main_pair)
            gear_ratio_array.append(gear_ratio)
        return gear_ratio_array
