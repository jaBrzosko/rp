import pandas as pd
import numpy as np
from sklearn import preprocessing
from collections import deque
from sklearn.model_selection import train_test_split

def load_data(path, history_length, lookup_step=1, test_size=0.3, shuffle=False, scale=True):
    result = {}
    features = ['date', 'temperature_2m', 'pressure_msl', 'surface_pressure', 'cloud_cover', 'soil_temperature_0_to_7cm', 'soil_moisture_0_to_7cm']

    df = pd.read_json(path)
    df['date'] = pd.to_datetime(df['date'])
    

    if scale:
        column_scaler = {}
        # scale the data (prices) from 0 to 1
        for column in features:
            if column == 'Date':
                continue
            scaler = preprocessing.MinMaxScaler()
            df[column] = scaler.fit_transform(np.expand_dims(df[column].values, axis=1))
            column_scaler[column] = scaler
        # add the MinMaxScaler instances to the result returned
        result["column_scaler"] = column_scaler

    df['Future'] = df['temperature_2m'].shift(-lookup_step)
    df.dropna(inplace=True)
    # df['Future'] = df['Close'] / df['Future']
    # print(df['Future'])
    sequence_data = []
    sequences = deque(maxlen=history_length)
    for entry, target in zip(df[features].values, df['Future'].values):
        sequences.append(entry)
        if len(sequences) == history_length:
            sequence_data.append([np.array(sequences), target])

    X, Y = [], []
    for seq, target in sequence_data:
        X.append(seq)
        Y.append(target)

    X = np.array(X)
    Y = np.array(Y)

    result["X_train"], result["X_test"], result["Y_train"], result["Y_test"] = train_test_split(X, Y, test_size=test_size, shuffle=shuffle)
    result["X_train"] = result["X_train"][:, :, 1:].astype(np.float32)
    result["X_test"] = result["X_test"][:, :, 1:].astype(np.float32)

    return result
