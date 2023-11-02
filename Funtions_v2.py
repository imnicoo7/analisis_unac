# Libraries
import pandas as pd
from sklearn.preprocessing import StandardScaler
# ----------------------------------------------------------------------------------------------------------------------


class DataConverter_v2:

    def convert_data_2(self, df):
        df = df.dropna()

        return df
