import pandas as pd

from getallplanturls import lst_plant_paths
from https import *

print(len(lst_plant_paths))

xpath_page = '//*[@id="mw-content-text"]/div/ul/li'
xpath_title = 'normalize-space(//*[@id="firstHeading"])'
# xpath_intro = 'normalize-space(//*[@id="mw-content-text"]/div/p[1])'
xpath_intro = 'normalize-space(//*[@id="mw-content-text"]/div/table/following-sibling::p)'

lst_steel_plants = list()

for plant_path in lst_plant_paths:
    # print(plant_path)
    try:
        global base_url
        page = HTTPRequestHTML(base_url + plant_path)

        title = page.xpath(xpath_title)
        intro = page.xpath(xpath_intro)
        entries = page.xpath(xpath_page)

        plant_detail = list()

        plant_detail = [entry.xpath('./descendant-or-self::text()') for entry in entries]

        # if len(plant_detail) < 1:
        #     print("###############", lst_plant_paths.index(plant_path), plant_path)

        plant = dict()
        plant['name'] = title
        plant['intro'] = intro
        plant['path'] = plant_path
        plant['detail'] = plant_detail

        print(plant, ",")
        lst_steel_plants.append(plant)

    except Exception:
        print("###############", lst_plant_paths.index(plant_path), plant_path)
        continue


steel_plants = pd.DataFrame(lst_steel_plants)
print(steel_plants)
steel_plants.to_excel('steel_plants3.xlsx')

