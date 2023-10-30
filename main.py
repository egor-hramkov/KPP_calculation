import json

import numpy as np
import pandas as pd

from gear_ratio_service import GearRatioService

frequency_turns_per_min = np.linspace(600, 4200, 19)

file_json = open('source/config.json')
config = json.load(file_json)

gear_rations = config['data']['gear_ratio']

a = GearRatioService(
    hub1=gear_rations['hub_1'],
    hub2=gear_rations['hub_2'],
    hub3=gear_rations['hub_3'],
    hub4=gear_rations['hub_4'],
    hub5=gear_rations['hub_5'],
    hub_reverse=gear_rations['hub_reverse'],
    transfer_case=gear_rations['transfer_case'],
    on_board_gearbox=gear_rations['on_board_gearbox'],
    main_pair=gear_rations['main_pair'],
    frequency_turns_per_min=list(frequency_turns_per_min)
)

data_frame = pd.DataFrame()
data_frame['frequency'] = frequency_turns_per_min
data_frame['hub1'] = a.gear_ratio_hub1
data_frame['hub2'] = a.gear_ratio_hub2
data_frame['hub3'] = a.gear_ratio_hub3
data_frame['hub4'] = a.gear_ratio_hub4
data_frame['hub5'] = a.gear_ratio_hub5
