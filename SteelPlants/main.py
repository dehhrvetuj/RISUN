import pandas as pd
import numpy as np

plants_all = pd.read_excel('steel_plants.xlsx')

plant_details = list(plants_all['detail'].apply(lambda x: eval(x)))


print(len(plant_details))

test = [next(iter(entry), None) for detail in plant_details for entry in detail]

test = ["" if x is None else x.lower().replace(':','').strip() for x in test]

test = test[0:991]

test = list(set(test))

test = sorted(test)

for t in test:
    print(t)


