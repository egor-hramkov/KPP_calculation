import json
from dataclasses import dataclass

import numpy
import numpy as np
import pandas as pd
from pandas import DataFrame
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures


@dataclass
class TrendLinesService:
    '''Класс для построения линий трендов'''
    power_and_torque_info_dataset:DataFrame

    def __post_init__(self):
        self.predicate_freq_array = np.linspace(0,4800, 101)

    @property
    def polynom_coefs_hm(self):
        x_data, y_data = self._get_linear_regression(self.power_and_torque_info_dataset[['power_and_torque_hms']])
        return self._get_polynom_coefs(x_data, y_data)

    @property
    def polynom_coefs_hp(self):
        x_data, y_data = self._get_linear_regression(self.power_and_torque_info_dataset[['power_and_torque_horse_powers']])
        return self._get_polynom_coefs(x_data, y_data)

    def _get_linear_regression(self, y_column):
        polynomial_features = PolynomialFeatures(degree=4, include_bias=False)
        x_data = polynomial_features.fit_transform(self.power_and_torque_info_dataset[['power_and_torque_turns']])
        predicate_data = polynomial_features.fit_transform(self.predicate_freq_array.reshape(-1,1))
        model = linear_model.LinearRegression()
        model.fit(x_data, y_column)
        predicate_result = model.predict(predicate_data)
        return (self.predicate_freq_array, predicate_result.reshape(-1,1))

    def _get_polynom_coefs(self, x_array, y_aaray):
        return np.polyfit(x_array, y_aaray, 4)


