import os
import pickle

pickle_file = os.path.join("back", "data", "dict_effet.pkl")


def get_dict_effet_theorique():
    with open('filename.pickle', 'rb') as handle:
        b = pickle.load(handle)
    return b
