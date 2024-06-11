from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import L1

def create_model(nSequence, nFeatures, nLayers, units, dropout=0.3):
    model = Sequential()

    # First layer
    model.add(LSTM(units, return_sequences=True, batch_input_shape=(None, nSequence, nFeatures)))
    model.add(Dropout(dropout))
    
    for i in range(nLayers):
        model.add(LSTM(units, return_sequences=True))
        model.add(Dropout(dropout))

    # Last layer
    model.add(LSTM(units, return_sequences=False))
    model.add(Dropout(dropout))
    model.add(Dense(1, activation="linear"))

    model.compile(loss="mean_squared_error", metrics=["mean_squared_error"], optimizer=Adam(learning_rate=1e-3))
    return model

def simple_model(nSequence, nFeatures, units, learningRate = 1e-3, dropout=0.3):
    model = Sequential()

    model.add(LSTM(units, return_sequences=True, batch_input_shape=(None, nSequence, nFeatures)))
    model.add(LSTM(units, return_sequences=False))

    model.add(Dense(1, activation="linear"))
    model.compile(loss="mean_squared_error", metrics=["mean_squared_error"], optimizer=Adam(learning_rate=learningRate))
    model.compile(loss="mean_absolute_error", metrics=["mean_squared_error"], optimizer=Adam(learning_rate=learningRate))
    return model

# m = create_model(20, 5, 16, 256)
# m.build()
# print(m.summary())
