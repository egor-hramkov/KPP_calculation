import json
import numpy as np
import pandas as pd

from services.calculate_KPD_service import CalculateKPDService
from services.dimensions_service import DimensionsService
from services.power_and_torque import PowerAndTorqueService
from services.speed_car_service import SpeedCarService
from services.turnovers_wheel_service import TurnoversWheelsService

# инициализация массива со значениями тех оборотов, с которыми придётся работать
frequency_turns_per_min = np.linspace(600, 4200, 19)

# загружаем данные с файла конфига
file_json = open('source/config.json')
config = json.load(file_json)

# формирование данных, где вычислются обороты колёс в минуту относительно кол-ва оборотов двигателя, номера передачи,
# данных о передаточных числах каждой скорости (таблица из ecxel №2)
gear_rations = config['data']['gear_ratio']

turns_wheels_service = TurnoversWheelsService(gear_rations['hub_1'], gear_rations['hub_2'], gear_rations['hub_3'],
                                              gear_rations['hub_4'],
                                              gear_rations['hub_5'], gear_rations['hub_reverse'],
                                              gear_rations['transfer_case'],
                                              gear_rations['on_board_gearbox'],
                                              gear_rations['main_pair'],
                                              list(frequency_turns_per_min)
                                              )

turnovers_wheel = pd.DataFrame()
turnovers_wheel['frequency'] = frequency_turns_per_min
turnovers_wheel['hub1'] = turns_wheels_service.gear_ratio_hub1
turnovers_wheel['hub2'] = turns_wheels_service.gear_ratio_hub2
turnovers_wheel['hub3'] = turns_wheels_service.gear_ratio_hub3
turnovers_wheel['hub4'] = turns_wheels_service.gear_ratio_hub4
turnovers_wheel['hub5'] = turns_wheels_service.gear_ratio_hub5

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
dimensions_data = DimensionsService(
    config['data']['dimensions']['car_width'],
    config['data']['dimensions']['car_height'],
    config['data']['dimensions']['streamline_coefficient']
)

dimensions = pd.DataFrame()
dimensions['car_width'] = ['габаритная ширина автомобиля', dimensions_data.width]
dimensions['car_height'] = ['габаритная высота автомобиля', dimensions_data.height]
dimensions['streamline_coefficient'] = ['площадь Миделева сечения', dimensions_data.streamline_coefficient]
dimensions['midelev_cross_sectional_area'] = ['коэфициент обтекаемости', dimensions_data.midelev_cross_sectional_area]

a = 1
