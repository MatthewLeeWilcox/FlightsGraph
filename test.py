import pickle

with open("aircraft_data.pkl", "rb") as file:
    x = pickle.load(file)


print(x)

import pandas as pd

x.to_csv("test.csv")