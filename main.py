import json
import pandas as pd
from pandas import DataFrame

from services.calculate_KPD_service import CalculateKPDService
from services.air_resistance_service import AirResistanceService
from services.coefficient_of_influence_of_power_on_fuel_consumption_service import CoefficientsInfluence
from services.dependence_torque_on_air_resistance_service import DependenceOfTorqueOnAirResistanceService
from services.dynamic_factor_service import DynamicFactorService
from services.gear_ratio_service import GearRatioService
from services.power_and_torque import PowerAndTorqueService
from services.rolling_resistance_service import RollingResistanceService
from services.speed_car_service import SpeedCarService
from services.torque_on_wheel_service import TorqueOnWheelService
from services.total_force_wheel_ideal_conditions_service import TotalForceWheelIdealConditionsService
from services.total_resistance_force_movement_service import TotalResistanceForceMovementService
from services.turnovers_wheel_service import TurnoversWheelsService

# загружаем данные с файла конфига
from utils.json_helper import JSONHelper

file_json = open('source/config.json')
config = json.load(file_json)
frequency_turns_per_min = config['data']['frequency_turns_per_min']
all_dataframes: list[DataFrame] = []

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
gear_ratio_info.name = 'gear_ratio'
all_dataframes.append(gear_ratio_info)

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
turnovers_wheel.name = 'turnovers_wheel'
all_dataframes.append(turnovers_wheel)

#таблица размерности шин
width_wheel = config['data']['wheel_info']['profile_width']
height_wheel = config['data']['wheel_info']['profile_height']
diameter_wheel = config['data']['wheel_info']['diameter']
wheel_info_table = pd.DataFrame()
wheel_info_table['Параметр'] = ['Размер колес','Номинальный радиус (м)','Статический радиус','Динамический радиус']
nom_radius=0.0254*(diameter_wheel/2)+(width_wheel/1000)*(height_wheel/100)
if height_wheel >= 90:
     tire_crumpling_ratio = 0.8
elif height_wheel <= 50:
    tire_crumpling_ratio = 0.85
else:
    tire_crumpling_ratio = 0.814285714
stat_radius = 0.0254*(diameter_wheel/2)+(width_wheel/1000)*(height_wheel/100)*tire_crumpling_ratio
dynamic_radius = nom_radius - ((nom_radius-stat_radius)/3)
wheel_info_table['Ширина профиля']=[width_wheel, nom_radius, stat_radius, dynamic_radius]
wheel_info_table['Профиль шины']=[height_wheel, '-', '-', '-']
wheel_info_table['Диаметр шины']=[diameter_wheel, '-','-','-']
wheel_info_table.name='wheel_info_table'
all_dataframes.append(wheel_info_table)






# формирование данных, где вычисляется скорость автомобиля относительно кол-ва оборотов двигателя, номера передачи,
# данных о передаточных числах каждой скорости и параметрах колёс(таблица из ecxel №5)
wheel_info = config['data']['wheel_info']
speed_car_service = SpeedCarService(
    wheel_info['profile_width'],
    wheel_info['profile_height'],
    wheel_info['diameter'],
    turnovers_wheel,
    frequency_turns_per_min
)

speed_car = pd.DataFrame()
speed_car['frequency'] = frequency_turns_per_min
speed_car['hub1'] = speed_car_service.speed_hub1
speed_car['hub2'] = speed_car_service.speed_hub2
speed_car['hub3'] = speed_car_service.speed_hub3
speed_car['hub4'] = speed_car_service.speed_hub4
speed_car['hub5'] = speed_car_service.speed_hub5
speed_car.name = 'speed_car'
all_dataframes.append(speed_car)

# Рассчёт мощности и крутящего момента
power_and_torque_info = config['data']['engine_performance']['measurements']
power_and_torque_turns = [data['freq_turns_per_min'] for data in power_and_torque_info]
power_and_torque_hms = [data['Hm'] for data in power_and_torque_info]
power_and_torque_horse_powers = [data['horse_power'] for data in power_and_torque_info]
# ToDo Храмков 02.11: пока что данные берутся от конфига, но дальше ничего с ними не делается т.к. НЕПОНЯТНО! По идее должны использоваться в сервисе ниже (PowerAndTorqueService)

# таблица коэффициентов полинома
coefficient_polynom = pd.DataFrame()
coefficient_polynom['Данные'] = ['Коэффициент момент', 'Коэффициент мощность']
coefficient_polynom['X/5'] = [0.0, 0.0]
coefficient_polynom['X/4'] = [6.5177394e-13, -1.7511371e-13]
coefficient_polynom['X/3'] = [-1.035910648521e-08, -1.97857344017e-09]
coefficient_polynom['X/2'] = [0.00003447582159142, 0.0000155372640980185]
coefficient_polynom['X'] = [-0.010124117314029, 0.00599106601989137]
coefficient_polynom['Собственный коэффициент'] = [175.14493655691, 7.45996575251171]
# ToDo Храмков ГРАФИКИ С ПОЛИНОМАМИ ТОЖЕ ФИГНЯ КАКАЯ ТО - обсудить
coefficient_polynom.name = 'coefficient_polynom'
all_dataframes.append(coefficient_polynom)

power_and_torque_data = PowerAndTorqueService(
    frequency_turns_per_min=list(frequency_turns_per_min)
)
power_and_torque = pd.DataFrame()
power_and_torque['frequency'] = power_and_torque_data.frequency_turns_per_min
power_and_torque['torques'] = power_and_torque_data.torques
power_and_torque['powers'] = power_and_torque_data.powers

power_and_torque.name = 'power_and_torque'
all_dataframes.append(power_and_torque)

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
kpd['число цилиндр. Передач'] = kpd_data.number_of_spur_gears
kpd['число конических передач'] = kpd_data.number_of_bevel_gears
kpd['число крестовин кардана'] = kpd_data.number_of_cardan_gears
kpd['КПД'] = kpd_data.KPD

kpd.name = 'kpd'
all_dataframes.append(kpd)

# Таблица габаритных размеров
air_resistance_service = AirResistanceService(
    config['data']['dimensions']['car_width'],
    config['data']['dimensions']['car_height'],
    config['data']['dimensions']['streamline_coefficient'],
    speed_car,
    frequency_turns_per_min
)

dimensions = pd.DataFrame()
dimensions['car_width'] = ['габаритная ширина автомобиля', air_resistance_service.width]
dimensions['car_height'] = ['габаритная высота автомобиля', air_resistance_service.height]
dimensions['streamline_coefficient'] = ['коэфициент обтекаемости', air_resistance_service.streamline_coefficient]
dimensions['midelev_cross_sectional_area'] = ['площадь Миделева сечения',
                                              air_resistance_service.midelev_cross_sectional_area]

dimensions.name = 'dimensions'
all_dataframes.append(dimensions)

# таблица сопротивления воздуха
air_resistance = pd.DataFrame()
air_resistance['frequency'] = frequency_turns_per_min
air_resistance['hub1'] = air_resistance_service.air_resistance_hub1
air_resistance['hub2'] = air_resistance_service.air_resistance_hub2
air_resistance['hub3'] = air_resistance_service.air_resistance_hub3
air_resistance['hub4'] = air_resistance_service.air_resistance_hub4
air_resistance['hub5'] = air_resistance_service.air_resistance_hub5


air_resistance.name = 'air_resistance'
all_dataframes.append(air_resistance)

# таблица крутящего момента на колесе
torque_on_wheel_service = TorqueOnWheelService(gear_ratio_info, power_and_torque, kpd, frequency_turns_per_min)
torque_on_wheel = pd.DataFrame()
torque_on_wheel['frequency_turns_per_min'] = frequency_turns_per_min
torque_on_wheel['hub1'] = torque_on_wheel_service.torque_on_wheel_hub1
torque_on_wheel['hub2'] = torque_on_wheel_service.torque_on_wheel_hub2
torque_on_wheel['hub3'] = torque_on_wheel_service.torque_on_wheel_hub3
torque_on_wheel['hub4'] = torque_on_wheel_service.torque_on_wheel_hub4
torque_on_wheel['hub5'] = torque_on_wheel_service.torque_on_wheel_hub5

torque_on_wheel.name = 'torque_on_wheel'
all_dataframes.append(torque_on_wheel)

# таблица совмещенной мощьности на колесе для каждой передачи и сопротивление воздуха
km_per_hour = config['data']['km_per_hour']
dependence_torque_on_air_resistance_service = DependenceOfTorqueOnAirResistanceService(km_per_hour, dimensions,
                                                                                       speed_car,
                                                                                       coefficient_polynom,
                                                                                       gear_ratio_info,
                                                                                       kpd)
dependence_torque_on_air_resistance = pd.DataFrame()
dependence_torque_on_air_resistance['Км/ч'] = km_per_hour
dependence_torque_on_air_resistance[
    'Сопротивление воздуха'] = dependence_torque_on_air_resistance_service.air_resistance
dependence_torque_on_air_resistance['Обороты 1 передачи'] = dependence_torque_on_air_resistance_service.turnovers_hub1
dependence_torque_on_air_resistance['Крутящий момент 1'] = dependence_torque_on_air_resistance_service.torque_hub1
dependence_torque_on_air_resistance['Обороты 2 передачи'] = dependence_torque_on_air_resistance_service.turnovers_hub2
dependence_torque_on_air_resistance['Крутящий момент 2'] = dependence_torque_on_air_resistance_service.torque_hub2
dependence_torque_on_air_resistance['Обороты 3 передачи'] = dependence_torque_on_air_resistance_service.turnovers_hub3
dependence_torque_on_air_resistance['Крутящий момент 3'] = dependence_torque_on_air_resistance_service.torque_hub3
dependence_torque_on_air_resistance['Обороты 4 передачи'] = dependence_torque_on_air_resistance_service.turnovers_hub4
dependence_torque_on_air_resistance['Крутящий момент 4'] = dependence_torque_on_air_resistance_service.torque_hub4
dependence_torque_on_air_resistance['Обороты 5 передачи'] = dependence_torque_on_air_resistance_service.turnovers_hub5
dependence_torque_on_air_resistance['Крутящий момент 5'] = dependence_torque_on_air_resistance_service.torque_hub5

dependence_torque_on_air_resistance.name = 'dependence_torque_on_air_resistance'
all_dataframes.append(dependence_torque_on_air_resistance)

# таблица масс автомобиля
car_weight = config['data']['weights']['car_weight']
full_mass = config['data']['weights']['full_mass']
passenger_seats = config['data']['weights']['passenger_seats']
mass_table = pd.DataFrame()
mass_table['Масса автомобиля'] = [car_weight]
mass_table['Снаряжённая масса'] = [car_weight + 70]
mass_table['Полная масса'] = [full_mass]
mass_table['Масса полезного груза'] = [full_mass - (car_weight + 70) - (70 * (passenger_seats - 1))]
mass_table['Число посадочных мест'] = [passenger_seats]

mass_table.name = 'mass_table'
all_dataframes.append(mass_table)

# таблица коэффициент сопротивления кочению колеса
coefficient_rolling_resistance_wheel = pd.DataFrame()
coefficient_rolling_resistance_wheel['Погодные условия'] = ['1.Хорошее состояние сухого асфальта',
                                                            '2.Удовлетворительное состояние сухого асфальта',
                                                            '3.Обледенелелая асфальтная дорога',
                                                            '4.Гравийая укатаная дорога',
                                                            '5.Хорошее состояние булыжника',
                                                            '6.Удовлетворительное состояние булыжника',
                                                            '7.Сухая укатанная грунтовая дорога',
                                                            '8.Мокрая укатанная грунтовая дорога']
coefficient_rolling_resistance_wheel['Минимум'] = [0.008, 0.015, 0.015, 0.02, 0.025, 0.035, 0.025, 0.05]
coefficient_rolling_resistance_wheel['Максимум'] = [0.015, 0.03, 0.02, 0.025, 0.03, 0.05, 0.035, 0.15]

coefficient_rolling_resistance_wheel.name = 'coefficient_rolling_resistance_wheel'
all_dataframes.append(coefficient_rolling_resistance_wheel)

# табл коэффициента влияния скорости в км/ч
coefficient_influence_speed = pd.DataFrame()
coefficient_influence_speed['Тип автомобиля'] = ['Легковой', 'Грузовой']
coefficient_influence_speed['Км/час минимум'] = [0.00004, 0.00002]
coefficient_influence_speed['Км/час максимум'] = [0.00005, 0.00003]
coefficient_influence_speed['М/с минимум'] = [0.00051, 0.00026]
coefficient_influence_speed['М/с максимум'] = [0.00065, 0.00039]

coefficient_influence_speed.name = 'coefficient_influence_speed'
all_dataframes.append(coefficient_influence_speed)

# таблица коэффициент сопротивления качению
rolling_resistance_service = RollingResistanceService(km_per_hour, coefficient_rolling_resistance_wheel, mass_table,
                                                      coefficient_influence_speed)
rolling_resistance = pd.DataFrame()
rolling_resistance['Км/ч'] = km_per_hour
rolling_resistance['1.Хорошее состояние сухого асфальта'] = rolling_resistance_service.coef_rolling_resistance_type1
rolling_resistance[
    '2.Удовлетворительное состояние сухого асфальта'] = rolling_resistance_service.coef_rolling_resistance_type2
rolling_resistance['3.Обледенелелая асфальтная дорога'] = rolling_resistance_service.coef_rolling_resistance_type3
rolling_resistance['4.Гравийая укатаная дорога'] = rolling_resistance_service.coef_rolling_resistance_type4
rolling_resistance['5.Хорошее состояние булыжника'] = rolling_resistance_service.coef_rolling_resistance_type5
rolling_resistance[
    '6.Удовлетворительное состояние булыжника'] = rolling_resistance_service.coef_rolling_resistance_type6
rolling_resistance['7.Сухая укатанная грунтовая дорога'] = rolling_resistance_service.coef_rolling_resistance_type7
rolling_resistance['8.Мокрая укатанная грунтовая дорога'] = rolling_resistance_service.coef_rolling_resistance_type8

rolling_resistance.name = 'rolling_resistance'
all_dataframes.append(rolling_resistance)


# таблица суммарной силы сопротивлению движения
total_resistance_force_movement_service = TotalResistanceForceMovementService([-20,-15,-10,-5,0,5,10,15,20], full_mass)
total_resistance_force_movement = pd.DataFrame()
total_resistance_force_movement['Угол %'] = total_resistance_force_movement_service.angle_array
total_resistance_force_movement['Сила подъёма'] = total_resistance_force_movement_service.lifting_force
total_resistance_force_movement.name='total_resistance_force_movement'
all_dataframes.append(total_resistance_force_movement)


#суммарная сила на колесе в идиальных условиях
total_force_wheel_ideal_conditions_service = TotalForceWheelIdealConditionsService(km_per_hour, rolling_resistance, speed_car, coefficient_polynom,dependence_torque_on_air_resistance, gear_ratio_info,kpd)
total_force_wheel_ideal_conditions = pd.DataFrame()
total_force_wheel_ideal_conditions['Км/ч'] = total_force_wheel_ideal_conditions_service.km_per_hour_array
total_force_wheel_ideal_conditions['Сумма сопротивления'] = total_force_wheel_ideal_conditions_service.air_resistance_array
total_force_wheel_ideal_conditions['Обороты 1 передача'] = total_force_wheel_ideal_conditions_service.turnovers_hub1
total_force_wheel_ideal_conditions['Крутящий момент 1 передача'] = total_force_wheel_ideal_conditions_service.force_on_wheel_hub1
total_force_wheel_ideal_conditions['Обороты 2 передача'] = total_force_wheel_ideal_conditions_service.turnovers_hub2
total_force_wheel_ideal_conditions['Крутящий момент 2 передача'] = total_force_wheel_ideal_conditions_service.force_on_wheel_hub2
total_force_wheel_ideal_conditions['Обороты 3 передача'] = total_force_wheel_ideal_conditions_service.turnovers_hub3
total_force_wheel_ideal_conditions['Крутящий момент 3 передача'] = total_force_wheel_ideal_conditions_service.force_on_wheel_hub3
total_force_wheel_ideal_conditions['Обороты 4 передача'] = total_force_wheel_ideal_conditions_service.turnovers_hub4
total_force_wheel_ideal_conditions['Крутящий момент 4 передача'] = total_force_wheel_ideal_conditions_service.force_on_wheel_hub4
total_force_wheel_ideal_conditions['Обороты 5 передача'] = total_force_wheel_ideal_conditions_service.turnovers_hub5
total_force_wheel_ideal_conditions['Крутящий момент 5 передача'] = total_force_wheel_ideal_conditions_service.force_on_wheel_hub5
total_force_wheel_ideal_conditions.name='total_force_wheel_ideal_conditions'
all_dataframes.append(total_force_wheel_ideal_conditions)
response = JSONHelper().dataframes_to_dict(all_dataframes)

# таблица расчёта динамического фактора
dynamic_factor_service = DynamicFactorService(km_per_hour, speed_car, coefficient_polynom, wheel_info_table,
                                              dependence_torque_on_air_resistance)
dynamic_factor = pd.DataFrame()
dynamic_factor['Км/ч'] = dynamic_factor_service.km_per_hour_array
dynamic_factor['Обороты 1 передача'] = dynamic_factor_service.turnovers_hub1
dynamic_factor['Крутящий момент 1 передача'] = dynamic_factor_service.torque_hub1

#коэффициент влияния мощьности на расход топлива
influence_power_on_fuel_consumption = pd.DataFrame()


coefficients_of_influence_data = CoefficientsInfluence(frequency_turns_per_min)
coefficients_of_influence = pd.DataFrame()

coefficients_of_influence['Коэффиценты'] = coefficients_of_influence_data.coefficients
coefficients_of_influence['частота'] = coefficients_of_influence_data.frequency_turns_per_min
coefficients_of_influence.name = 'Коэффициент влияния мощности на расход топлива'
all_dataframes.append(coefficients_of_influence)
