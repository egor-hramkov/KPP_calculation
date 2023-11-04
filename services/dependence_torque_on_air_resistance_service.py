from dataclasses import dataclass

import numpy
from pandas import DataFrame


@dataclass
class DependenceOfTorqueOnAirResistance:
    km_per_hour_array:numpy.array
    dimensions_dataset:DataFrame
    speed_car_dataset:DataFrame



