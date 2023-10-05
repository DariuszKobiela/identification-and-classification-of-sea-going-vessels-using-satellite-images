from constants import INTERPOLATED_AIS_DATA_PATH, DESIRED_COLUMNS_WIDTH

import pandas as pd
# import numpy as np

pd.set_option('display.width', DESIRED_COLUMNS_WIDTH)
pd.set_option('display.max_columns', 20)
# np.set_printoption(linewidth=desired_width)

df = pd.read_csv(INTERPOLATED_AIS_DATA_PATH + "interpolated_processed_AIS_2021_01_06.csv")
print(df)

print(df[df.Length < 30])