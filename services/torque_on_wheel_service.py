from dataclasses import dataclass

from pandas import DataFrame


@dataclass
class TorqueOnWheelService:
    """ Сервис для формирования данных о крутящем момменте на колесе относиельно передачи и кол-ва оборотов двигателя"""
    gear_ratios_dataset: DataFrame
    power_and_torque_dataset: DataFrame
    kpd_dataset: DataFrame

    def __post_init__(self):
        self.full_gear_ratio_hub1 = self.gear_ratios_dataset['full_gear_ratio'][0]
        self.full_gear_ratio_hub2 = self.gear_ratios_dataset['full_gear_ratio'][1]
        self.full_gear_ratio_hub3 = self.gear_ratios_dataset['full_gear_ratio'][2]
        self.full_gear_ratio_hub4 = self.gear_ratios_dataset['full_gear_ratio'][3]
        self.full_gear_ratio_hub5 = self.gear_ratios_dataset['full_gear_ratio'][4]
        self.full_gear_ratio_reverse = self.gear_ratios_dataset['full_gear_ratio'][5]
        self.hm_per_turns_engine = self.power_and_torque_dataset['torques'].to_numpy()
        self.kpd_hub1 = self.kpd_dataset['KPD'][0]
        self.kpd_hub2 = self.kpd_dataset['KPD'][1]
        self.kpd_hub3 = self.kpd_dataset['KPD'][2]
        self.kpd_hub4 = self.kpd_dataset['KPD'][3]
        self.kpd_hub5 = self.kpd_dataset['KPD'][4]

    @property
    def torque_on_wheel_hub1(self):
        return self.__calculate_torque_on_wheel(self.full_gear_ratio_hub1, self.kpd_hub1)

    @property
    def torque_on_wheel_hub2(self):
        return self.__calculate_torque_on_wheel(self.full_gear_ratio_hub2, self.kpd_hub2)

    @property
    def torque_on_wheel_hub3(self):
        return self.__calculate_torque_on_wheel(self.full_gear_ratio_hub3, self.kpd_hub3)

    @property
    def torque_on_wheel_hub4(self):
        return self.__calculate_torque_on_wheel(self.full_gear_ratio_hub4, self.kpd_hub4)

    @property
    def torque_on_wheel_hub5(self):
        return self.__calculate_torque_on_wheel(self.full_gear_ratio_hub5, self.kpd_hub5)

    def __calculate_torque_on_wheel(self, full_gear_ratio_hub, kpd_hub):
        """Возвращает список крутящего момента на колесе для определённой передачи при определённом кол-ве оборотов двигателя"""
        torque_on_wheel = []
        for hm in self.hm_per_turns_engine:
            torque_on_wheel.append(hm * full_gear_ratio_hub * kpd_hub)
        return torque_on_wheel
