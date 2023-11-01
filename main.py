import json
import numpy as np
import pandas as pd
from speed_car_service import SpeedCarService
from turnovers_wheel_service import TurnoversWheelsService

#инициализация массива со значениями тех оборотов, с которыми придётся работать
frequency_turns_per_min = np.linspace(600, 4200, 19)

#загружаем данные с файла конфига
file_json = open('source/config.json')
config = json.load(file_json)

#формирование данных, где вычислются обороты колёс в минуту относительно кол-ва оборотов двигателя, номера передачи,
#данных о передаточных числах каждой скорости (таблица из ecxel №2)
gear_rations = config['data']['gear_ratio']

turns_wheels_service = TurnoversWheelsService(gear_rations['hub_1'], gear_rations['hub_2'], gear_rations['hub_3'], gear_rations['hub_4'],
                           gear_rations['hub_5'], gear_rations['hub_reverse'], gear_rations['transfer_case'],
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

#формирование данных, где вычисляется скорость автомобиля относительно кол-ва оборотов двигателя, номера передачи,
#данных о передаточных числах каждой скорости и параметрах колёс(таблица из ecxel №5)
wheel_info = config['data']['wheel_info']
speed_car_service = SpeedCarService(wheel_info['profile_width'], wheel_info['profile_height'], wheel_info['diameter'],
                    turnovers_wheel)

speed_car = pd.DataFrame()
speed_car['frequency'] = frequency_turns_per_min
speed_car['hub1'] = speed_car_service.speed_hub1
speed_car['hub2'] = speed_car_service.speed_hub2
speed_car['hub3'] = speed_car_service.speed_hub3
speed_car['hub4'] = speed_car_service.speed_hub4
speed_car['hub5'] = speed_car_service.speed_hub5
