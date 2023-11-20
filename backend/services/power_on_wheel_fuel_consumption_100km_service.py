from dataclasses import dataclass

import numpy


@dataclass
class PowerOnWheelFuelConsumption100kmService:
    """Сервис для формирования таблицы Мощность на колесе и расход топлива на 100 км"""
    km_per_hour_array: numpy.array

