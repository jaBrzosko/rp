from constants import *
from model_creation import simple_model
from data_preparation import load_data
from tensorflow.keras.callbacks import ModelCheckpoint, TensorBoard
import os
import numpy as np
from pprint import pprint
import tensorflow as tf

# accepted_years = [2000, 2004, 2008, 2012, 2016, 2020]
accepted_years = [2022]

def make_paths():
    if not os.path.isdir("results"):
        os.mkdir("results")
    if not os.path.isdir("logs"):
        os.mkdir("logs")
    if not os.path.isdir("data"):
        os.mkdir("data")

def shuffle_in_unison(a, b):
    assert len(a) == len(b)
    shuffled_a = np.empty(a.shape, dtype=a.dtype)
    shuffled_b = np.empty(b.shape, dtype=b.dtype)
    permutation = np.random.permutation(len(a))
    for old_index, new_index in enumerate(permutation):
        shuffled_a[new_index] = a[old_index]
        shuffled_b[new_index] = b[old_index]
    return shuffled_a, shuffled_b

def main():

    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
    # Restrict TensorFlow to only use the first GPU
        try:
            tf.config.set_visible_devices(gpus[0], 'GPU')
            tf.config.experimental.set_memory_growth(gpus[0], enable=True)
            logical_gpus = tf.config.list_logical_devices('GPU')
            print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
        except RuntimeError as e:
            # Visible devices must be set before GPUs have been initialized
            print(e)

    if MULTIPLE_DATASETS:
        files = [f for f in os.listdir(DATA_DIR) if f.endswith(".json") and int(f.split("_")[-1].split(".")[0]) in accepted_years]
        data = load_data(os.path.join(DATA_DIR, files[0]), NUMBER_OF_DAYS, shuffle=SHUFFLE, lookup_step = LOOKUP_STEP)
        for f in files[1:]:
            p = os.path.join(DATA_DIR, f)
            temp = load_data(p, NUMBER_OF_DAYS, shuffle=SHUFFLE, lookup_step = LOOKUP_STEP)
            data["X_train"] = np.concatenate((data["X_train"], temp["X_train"]), axis=0)
            data["Y_train"] = np.concatenate((data["Y_train"], temp["Y_train"]), axis=0)
            data["X_test"] = np.concatenate((data["X_test"], temp["X_test"]), axis=0)
            data["Y_test"] = np.concatenate((data["Y_test"], temp["Y_test"]), axis=0)
        data["X_train"], data["Y_train"] = shuffle_in_unison(data["X_train"], data["Y_train"])  
        data["X_test"], data["Y_test"] = shuffle_in_unison(data["X_test"], data["Y_test"])  
    else:
        data = load_data("./data/points/df_44.81546401977539_14.188563346862793_2022.json", NUMBER_OF_DAYS, shuffle=SHUFFLE, lookup_step = LOOKUP_STEP)

    model = simple_model(NUMBER_OF_DAYS, NUMBER_OF_FEATURES, UNITS_PER_LAYER, learningRate=LEARNING_RATE)
    # model = create_model(NUMBER_OF_DAYS, NUMBER_OF_FEATURES, LAYERS, UNITS_PER_LAYER)
    make_paths()

    checkpointer = ModelCheckpoint(os.path.join("results", MODEL_NAME + ".h5"), save_best_only=True, verbose=1)
    tensorboard = TensorBoard(log_dir=os.path.join("logs", MODEL_NAME))
    history = model.fit(data["X_train"], data["Y_train"],
                    batch_size=BATCH_SIZE,
                    epochs=EPOCHS,
                    validation_data=(data["X_test"], data["Y_test"]),
                    callbacks=[checkpointer, tensorboard],
                    verbose=1)


if __name__ == "__main__":
    main()
