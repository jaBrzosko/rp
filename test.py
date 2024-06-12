import numpy as np
import pandas as pd
import tensorflow as tf
from collections import deque
from sklearn import preprocessing
import matplotlib.pyplot as plt

from model_creation import create_model
from constants import *

def plot_graph(test_df):
    plt.plot(test_df['Y_test'], c='b')
    plt.plot(test_df['Y_pred'], c='r')
    plt.xlabel("Hours")
    plt.ylabel("Temperature")
    plt.legend(["Actural temperature", "Predicted temperature"])
    plt.show()


def prepare_test_data(path, historyLength, lookupStep=1, scale=True):
    result = dict()
    features = ['date', 'temperature_2m', 'pressure_msl', 'surface_pressure', 'cloud_cover', 'soil_temperature_0_to_7cm', 'soil_moisture_0_to_7cm']
    df = pd.read_json(path)
    result['df'] = df.copy()
    
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

    df['Future'] = df['temperature_2m'].shift(-lookupStep)
    df.dropna(inplace=True)

    sequence_data = []
    sequences = deque(maxlen=historyLength)
    for entry, target in zip(df[features].values, df['Future'].values):
        sequences.append(entry)
        if len(sequences) == historyLength:
            sequence_data.append([np.array(sequences), target])

    X, Y = [], []
    for seq, target in sequence_data:
        X.append(seq)
        Y.append(target)
    result['X_test'] = np.array(X)
    result['Y_test'] = np.array(Y)
    result["X_test"] = result["X_test"][:, :, 1:].astype(np.float32)
    return result

def main():
    data = prepare_test_data("./data/df_54.868186950683594_24.10714340209961_2023.json", NUMBER_OF_DAYS, lookupStep = LOOKUP_STEP)
    model = tf.keras.models.load_model('./results/' + TESTED_MODEL + '.h5')
    print(model.summary())
    y_pred = model.predict(data['X_test'])

    y_test = np.squeeze(data["column_scaler"]["temperature_2m"].inverse_transform(np.expand_dims(data['Y_test'], axis=0)))
    # print(y_pred)
    y_pred = np.squeeze(data["column_scaler"]["temperature_2m"].inverse_transform(y_pred))

    data['Y_test'] = y_test[:-24]
    data['Y_pred'] = y_pred[24:]
    plot_graph(data)

if __name__ == "__main__":
    main()
