import json
import numpy as np
import pandas as pd

from services.calculate_KPD_service import CalculateKPDService
from services.air_resistance_service import AirResistanceService
from services.gear_ratio_service import GearRatioService
from services.power_and_torque import PowerAndTorqueService
from services.speed_car_service import SpeedCarService
from services.torque_on_wheel_service import TorqueOnWheelService
from services.turnovers_wheel_service import TurnoversWheelsService

# загружаем данные с файла конфига
file_json = open('source/config.json')
config = json.load(file_json)
frequency_turns_per_min = config['data']['frequency_turns_per_min']
# таблица с расчётом полного передаточного числа для каждой передачи
gear_ratio_service = GearRatioService(config['data']['gear_ratio']['hub_1'], config['data']['gear_ratio']['hub_2'],
                                      config['data']['gear_ratio']['hub_3'], config['data']['gear_ratio']['hub_4'],
                                      config['data']['gear_ratio']['hub_5'],
                                      config['data']['gear_ratio']['hub_reverse'],
                                      config['data']['gear_ratio']['transfer_case'],
                                      config['data']['gear_ratio']['on_board_gearbox'],
                                      config['data']['gear_ratio']['main_pair'])
gear_ratio_info = pd.DataFrame()
gear_ratio_info['parametrs'] = ['Передача 1', 'Передача 2', 'Передача 3', 'Передача 4', 'Передача 5', 'Передача R',
                                'Раздаточная коробка', 'Бортовой редуктор', 'Главная пара']
gear_ratio_info['gear_ratio'] = [gear_ratio_service.gear_ratio_hub1, gear_ratio_service.gear_ratio_hub2,
                                 gear_ratio_service.gear_ratio_hub3, gear_ratio_service.gear_ratio_hub4,
                                 gear_ratio_service.gear_ratio_hub5, gear_ratio_service.gear_ratio_reverse,
                                 gear_ratio_service.transfer_case, gear_ratio_service.on_board_gearbox,
                                 gear_ratio_service.main_pair]
gear_ratio_info['full_gear_ratio'] = [gear_ratio_service.full_gear_ratio_hub1, gear_ratio_service.full_gear_ratio_hub2,
                                      gear_ratio_service.full_gear_ratio_hub3, gear_ratio_service.full_gear_ratio_hub4,
                                      gear_ratio_service.full_gear_ratio_hub5,
                                      gear_ratio_service.full_gear_ratio_reverse, '-', '-', '-']

# формирование данных, где вычислются обороты колёс в минуту относительно кол-ва оборотов двигателя, номера передачи,
# данных о передаточных числах каждой скорости (таблица из ecxel №2)
turns_wheels_service = TurnoversWheelsService(gear_ratio_service.full_gear_ratio_hub1,
                                              gear_ratio_service.full_gear_ratio_hub2,
                                              gear_ratio_service.full_gear_ratio_hub3,
                                              gear_ratio_service.full_gear_ratio_hub4,
                                              gear_ratio_service.full_gear_ratio_hub5,
                                              gear_ratio_service.full_gear_ratio_reverse, list(frequency_turns_per_min))

turnovers_wheel = pd.DataFrame()
turnovers_wheel['frequency'] = frequency_turns_per_min
turnovers_wheel['hub1'] = turns_wheels_service.turnovers_wheels_hub1
turnovers_wheel['hub2'] = turns_wheels_service.turnovers_wheels_hub2
turnovers_wheel['hub3'] = turns_wheels_service.turnovers_wheels_hub3
turnovers_wheel['hub4'] = turns_wheels_service.turnovers_wheels_hub4
turnovers_wheel['hub5'] = turns_wheels_service.turnovers_wheels_hub5

# формирование данных, где вычисляется скорость автомобиля относительно кол-ва оборотов двигателя, номера передачи,
# данных о передаточных числах каждой скорости и параметрах колёс(таблица из ecxel №5)
wheel_info = config['data']['wheel_info']
speed_car_service = SpeedCarService(
    wheel_info['profile_width'],
    wheel_info['profile_height'],
    wheel_info['diameter'],
    turnovers_wheel
)

speed_car = pd.DataFrame()
speed_car['frequency'] = frequency_turns_per_min
speed_car['hub1'] = speed_car_service.speed_hub1
speed_car['hub2'] = speed_car_service.speed_hub2
speed_car['hub3'] = speed_car_service.speed_hub3
speed_car['hub4'] = speed_car_service.speed_hub4
speed_car['hub5'] = speed_car_service.speed_hub5

p = 1

# Рассчёт мощности и крутящего момента
power_and_torque_info = config['data']['engine_performance']['measurements']
power_and_torque_turns = [data['freq_turns_per_min'] for data in power_and_torque_info]
power_and_torque_hms = [data['Hm'] for data in power_and_torque_info]
power_and_torque_horse_powers = [data['horse_power'] for data in power_and_torque_info]
# ToDo Храмков 02.11: пока что данные берутся от конфига, но дальше ничего с ними не делается т.к. НЕПОНЯТНО! По идее должны использоваться в сервисе ниже (PowerAndTorqueService)

power_and_torque_data = PowerAndTorqueService(
    frequency_turns_per_min=list(frequency_turns_per_min)
)
power_and_torque = pd.DataFrame()
power_and_torque['frequency'] = power_and_torque_data.frequency_turns_per_min
power_and_torque['torques'] = power_and_torque_data.torques
power_and_torque['powers'] = power_and_torque_data.powers

# Рассчёт КПД трансмиссии
number_of_spur_gears = config['data']['number_of_spur_gears']
number_of_bevel_gears = config['data']['number_of_bevel_gears']
number_of_cardan_gears = config['data']['number_of_cardan_gears']

kpd = pd.DataFrame()
kpd_data = CalculateKPDService(
    number_of_spur_gears=number_of_spur_gears,
    number_of_bevel_gears=number_of_bevel_gears,
    number_of_cardan_gears=number_of_cardan_gears
)
kpd['number_of_spur_gears'] = kpd_data.number_of_spur_gears
kpd['number_of_bevel_gears'] = kpd_data.number_of_bevel_gears
kpd['number_of_cardan_gears'] = kpd_data.number_of_cardan_gears
kpd['KPD'] = kpd_data.KPD

# Таблица масс автомобиля
car_weight = config['data']['weights']['car_weight']
full_mass = config['data']['weights']['full_mass']
passenger_seats = config['data']['weights']['passenger_seats']

# Таблица габаритных размеров
air_resistance_service = AirResistanceService(
    config['data']['dimensions']['car_width'],
    config['data']['dimensions']['car_height'],
    config['data']['dimensions']['streamline_coefficient'],
    speed_car
)

dimensions = pd.DataFrame()
dimensions['car_width'] = ['габаритная ширина автомобиля', air_resistance_service.width]
dimensions['car_height'] = ['габаритная высота автомобиля', air_resistance_service.height]
dimensions['streamline_coefficient'] = ['площадь Миделева сечения', air_resistance_service.streamline_coefficient]
dimensions['midelev_cross_sectional_area'] = ['коэфициент обтекаемости',
                                              air_resistance_service.midelev_cross_sectional_area]

# таблица сопротивления воздуха
air_resistance = pd.DataFrame()
air_resistance['frequency'] = frequency_turns_per_min
air_resistance['hub1'] = air_resistance_service.air_resistance_hub1
air_resistance['hub2'] = air_resistance_service.air_resistance_hub2
air_resistance['hub3'] = air_resistance_service.air_resistance_hub3
air_resistance['hub4'] = air_resistance_service.air_resistance_hub4
air_resistance['hub5'] = air_resistance_service.air_resistance_hub5

#таблица крутящего момента на колесе
torque_on_wheel_service = TorqueOnWheelService(gear_ratio_info,power_and_torque, kpd)
torque_on_wheel = pd.DataFrame()
torque_on_wheel['frequency_turns_per_min'] = frequency_turns_per_min
torque_on_wheel['hub1'] = torque_on_wheel_service.torque_on_wheel_hub1
torque_on_wheel['hub2'] = torque_on_wheel_service.torque_on_wheel_hub2
torque_on_wheel['hub3'] = torque_on_wheel_service.torque_on_wheel_hub3
torque_on_wheel['hub4'] = torque_on_wheel_service.torque_on_wheel_hub4
torque_on_wheel['hub5'] = torque_on_wheel_service.torque_on_wheel_hub5

#таблица совмещенной мощьности на колесе для каждой передачи и сопротивление воздуха


