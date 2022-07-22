import re
import pandas as pd
import numpy as np

production = ['2020 production', '2020 production (thousand tonnes per annum',
              '2020 production (thousand tonnes per annum)',
              'production (thousand tonnes per annum)',
              'crude steel production (thousand tonnes per annum) in 2020']

iron_cap = ['crude iron production capacities (thousand tonnes per annum)']

steel_cap = ['production capacities (thousand tonnes per annum)',
             'crude steel production capacities (thousand tonnes per annum)']

capacity = iron_cap + steel_cap

# 'crude steel proposed capacities (thousand tonnes per annum)'

proposed = [
    'additional proposed (thousand tonnes per annum)',
    'additional proposed capacity (thousand tonnes per annum)']

GPS = ['gps coordinates', 'coordenadas de gps']
status = ['plant status']
location = ['location']
owner = ['owner']
parent = ['parent company']
start = ['start year']
close = ['closed year']

alter_name = ['alternative plant names']
other_name = ['other language plant name']

prod_cate = ['steel product category']
products = ['steel products']

main_equip = ['main production equipment', 'primary steel production equipment']
deta_equip = ['detailed production equipment']

# private/state ownership

lst_plants = pd.read_excel('steel_plants3.xlsx', index_col=0)
lst_plants = lst_plants.iloc[0:991]


def ExtracInfo(text):
    entries = [entry for entry in eval(text) if len(entry) > 1]

    global lst_potential_keys
    lst_entry_info = [''] * len(lst_potential_keys)

    for ind, potential_key in enumerate(lst_potential_keys):
        for entry in entries:
            key = entry[0].lower().replace(':', '').strip()
            if key in potential_key:
                lst_entry_info[ind] += ' '.join(entry[1:]).replace(':', '').strip() + '\n'

    return pd.Series(lst_entry_info)


lst_potential_keys = [alter_name, other_name, owner, parent, location, GPS, status, start, close,
                      production, main_equip, deta_equip, production, iron_cap, steel_cap, capacity]

lst_plants[['alternative name', 'other language name', 'owner', 'parent', 'location', 'GPS',
            'status', 'start', 'close', 'production', 'main_equip', 'deta_equip', 'production',
            'iron_cap', 'steel_cap', 'capacity']] \
    = lst_plants['detail'].apply(lambda x: ExtracInfo(x))

from interpretinfo import Equipment, Status, MainEquip, IsCoking, RemoveBrackets, GPSCoord, Country, \
    Production, Capacity, str2num, add, Convert, IsShort, DropChina
from trans_chinese import trans_country

lst_plants['主要设备'] = lst_plants['main_equip'] + lst_plants['deta_equip']
lst_plants['自备焦炉'] = lst_plants['主要设备'].apply(lambda x: IsCoking(x))
lst_plants['长短流程'] = lst_plants['主要设备'].apply(lambda x: IsShort(x))
lst_plants['设备类型'] = lst_plants['主要设备'].apply(lambda x: MainEquip(Equipment(x)))
lst_plants['设备说明'] = lst_plants['main_equip'].apply(lambda x: Equipment(x))

lst_plants['deta_equip'] = lst_plants['deta_equip'].apply(lambda x: None if x == '' else x)
lst_plants['deta_equip'].fillna(lst_plants['main_equip'], inplace=True)
lst_plants['设备详细'] = lst_plants['deta_equip'].apply(lambda x: RemoveBrackets(x))

lst_plants['状态'] = lst_plants['status'].apply(lambda x: Status(x))
lst_plants['位置'] = lst_plants['location'].apply(lambda x: RemoveBrackets(x))
lst_plants[['纬度坐标', '经度坐标']] = lst_plants['GPS'].apply(lambda x: GPSCoord(x))
lst_plants['国家(英文)'] = lst_plants['location'].apply(lambda x: Country(x))
lst_plants['国家(中文)'] = lst_plants['国家(英文)'].apply(lambda x: trans_country(x))

lst_plants[['prod-total', 'prod-steel', 'prod-eaf', 'prod-bof', 'prod-iron', 'prod-bf', 'prod-dri', 'prod-prod',
            'prod-coking', 'prod-other']] = lst_plants['production'].apply(lambda x: Production(x))

lst_plants[['cap-st-total', 'cap-st-steel', 'cap-st-eaf', 'cap-st-bof', 'cap-st-iron', 'cap-st-bf', 'cap-st-dri',
            'cap-st-coking', 'cap-st-sinter', 'cap-st-pellet', 'cap-st-other']] \
    = lst_plants['steel_cap'].apply(lambda x: Capacity(x))

lst_plants[['cap-ir-total', 'cap-ir-steel', 'cap-ir-eaf', 'cap-ir-bof', 'cap-ir-iron', 'cap-ir-bf', 'cap-ir-dri',
            'cap-ir-coking', 'cap-ir-sinter', 'cap-ir-pellet', 'cap-ir-other']] \
    = lst_plants['iron_cap'].apply(lambda x: Capacity(x))

lst_plants['prod-steel'].fillna(lst_plants['prod-total'], inplace=True)
lst_plants['cap-st-steel'].fillna(lst_plants['cap-st-total'], inplace=True)
lst_plants['cap-ir-steel'].fillna(lst_plants['cap-ir-total'], inplace=True)

lst_plants.fillna({'cap-st-eaf': lst_plants['cap-ir-eaf'],
                   'cap-st-bof': lst_plants['cap-ir-bof'],
                   'cap-st-steel': lst_plants['cap-ir-steel']}, inplace=True)

lst_plants.fillna({'cap-ir-bf': lst_plants['cap-st-bf'],
                   'cap-ir-dri': lst_plants['cap-st-dri'],
                   'cap-ir-iron': lst_plants['cap-st-iron'],
                   'cap-ir-coking': lst_plants['cap-st-coking'],
                   'cap-ir-pellt': lst_plants['cap-ir-pellet']}, inplace=True)

for cname, ename in zip(['粗钢总产量', 'BOF产量', 'EAF产量', '成品产量', '生铁总产量', 'BF产量', 'DRI产量', '焦化产量'],
                        ['prod-steel', 'prod-bof', 'prod-eaf', 'prod-prod', 'prod-iron', 'prod-bf', 'prod-dri',
                         'prod-coking']):
    lst_plants[cname] = lst_plants[ename].apply(lambda x: str2num(x))

for cname, ename in zip(['粗钢总产能', 'BOF产能', 'EAF产能', '生铁总产能', 'BF产能', 'DRI产能', '焦化产能', '烧结产能', '球团产能'],
                        ['cap-st-steel', 'cap-st-bof', 'cap-st-eaf', 'cap-ir-iron', 'cap-ir-bf', 'cap-ir-dri',
                         'cap-ir-coking', 'cap-ir-sinter', 'cap-ir-pellet']):
    lst_plants[cname] = lst_plants[ename].apply(lambda x: str2num(x))

lst_plants.fillna({'粗钢总产量': lst_plants[['BOF产量', 'EAF产量']].apply(lambda x: add(*x), axis=1),
                   '生铁总产量': lst_plants[['BF产量', 'DRI产量']].apply(lambda x: add(*x), axis=1),
                   '粗钢总产能': lst_plants[['BOF产能', 'EAF产能']].apply(lambda x: add(*x), axis=1),
                   '生铁总产能': lst_plants[['BF产能', 'DRI产能']].apply(lambda x: add(*x), axis=1)}, inplace=True)

for name in ['粗钢总产量', 'BOF产量', 'EAF产量', '生铁总产量', 'BF产量', 'DRI产量', '焦化产量', '成品产量',
             '粗钢总产能', 'BOF产能', 'EAF产能', '生铁总产能', 'BF产能', 'DRI产能', '烧结产能', '球团产能', '焦化产能']:
    lst_plants[name] = lst_plants[name].apply(lambda x: Convert(x))

lst_plants.rename(columns={'name': '工厂名称(英文)', 'alternative name': '工厂别名', 'other language name': '工厂名称(所在国)',
                           'owner': '所有者', 'parent': '母公司'}, inplace=True)


lst_plants = lst_plants[lst_plants['国家(英文)'] != "China"]
# lst_plants = lst_plants[lst_plants['位置'].apply(lambda x: DropChina(x))]
lst_plants.reset_index(inplace=True, drop=True)

lst_plants.sort_values(by=['国家(英文)', '工厂名称(英文)'], ascending=True, inplace=True, ignore_index=True)

lst_plants[['国家(中文)', '国家(英文)', '工厂名称(英文)', '工厂别名', '工厂名称(所在国)', '位置', '纬度坐标', '经度坐标', '状态',
            '自备焦炉', '长短流程', '设备类型', '设备详细', '粗钢总产量', 'BOF产量', 'EAF产量', '生铁总产量', 'BF产量', 'DRI产量',
            '焦化产量', '成品产量', '粗钢总产能', 'BOF产能', 'EAF产能', '生铁总产能', 'BF产能', 'DRI产能', '烧结产能', '球团产能',
            '焦化产能', '所有者', '母公司']]\
    .to_excel("steel-plants-information.xlsx")




# lst_plants[['production', '粗钢总产量', 'BOF产量', 'EAF产量', '生铁总产量', 'BF产量', 'DRI产量', '焦化产量', '成品产量']].to_excel('production001.xlsx')
# lst_plants[['steel_cap', 'iron_cap', '粗钢总产能', 'BOF产能', 'EAF产能', '生铁总产能', 'BF产能', 'DRI产能', '烧结产能', '球团产能', '焦化产能']].to_excel('capacity001.xlsx')


# lst_plants[['cap-total', 'cap-steel', 'cap-eaf', 'cap-bof', 'cap-iron', 'cap-bf', 'cap-dri',
#             'cap-coking', 'cap-sinter', 'cap-pellet', 'cap-other']] \
#                                             = lst_plants['capacity'].apply(lambda x: Capacity(x))
# lst_plants[['cap-total', 'cap-steel', 'cap-eaf', 'cap-bof', 'cap-iron', 'cap-bf', 'cap-dri',
#             'cap-coking', 'cap-sinter', 'cap-pellet', 'cap-other']].to_excel('capacity.xlsx')


# lst_plants.rename(columns={'name': '工厂名称', 'alternative name': '工厂别名', 'other language name': '他文名称',
#                            'owner': '所有者', 'parent': '母公司'}, inplace=True)


# lst_plants[['国家', '工厂名称', '工厂别名', '他文名称', '位置', '纬度坐标', '经度坐标', '状态', '自备焦炉', '设备类型',
#             '设备详细', ]].to_excel('uuuuu.xlsx')
# lst_plants[['steel_cap']].to_excel('steel_cap.xlsx')


# lst_plants['工厂名称'] = lst_plants['name']
# lst_plants['工厂别名'] = lst_plants['alternative name']
# lst_plants['他文名称'] = lst_plants['other language name']
# lst_plants['所有者'] = lst_plants['owner']
# lst_plants['母公司'] = lst_plants['parent']
# lst_plants['地址'] = lst_plants['location']
# lst_plants['坐标'] = lst_plants['GPS']
#
# lst_plants[['main_equip', 'deta_equip']].to_excel('yyyy.xlsx')
#
# lst_plants[['main_equip', 'deta_equip']].to_excel('zzzz.xlsx')


# for entry in entries:
#
#     if len(entry) <= 1:
#         continue
#
#     key = entry[0].lower().replace(':', '').strip()
#
#     potential_key = [potential_key for potential_key in lst_potential_keys if key in potential_key]
#     ind
#     if key in owner:
#         owner = ' '.join(entry[1:])
#     if key in parent:
#         paren = ' '.join(entry[1:])
#     if key in location:
#         locat = ' '.join(entry[1:])


# lst_plants['detail'] = lst_plants['detail'].apply(lambda entries: [item for entry in entries for item in entry if item])
# print(lst_plants['detail'])

# entries = [['Private/State ownership:', ' state-owned (Ministry of Metal and Machine-Building Industries)', '[1]'], ['Parent company:', ' Government of North Korea', '[1]'], ['Owner:', ' Government of North Korea', '[1]'], ['Alternative plant names:', ' April 13 Iron Mill'], ['Other language plant name:', ' 4.13 製鋼所 (Chinese)'], ['Location:', ' Nampo, South Pyongan Province, North Korea', '[1]'], ['GPS Coordinates:', ' 38.729864, 125.414672 (approximate)'], ['Plant status', ':', ' operating', '[1]'], ['Start year:', ' During first Seven-Year Plan (1961-1970)', '[2]'], ['Production capacities (thousand tonnes per annum):', '\n', 'Crude steel:', ' 400', '[2]']]
#
# print([item for entry in entries for item in entry if item])


# owner = None
# paren = None
# locat = None
# statu = None
# coord = None
# start = None
# close = None
# altna = None
# othna = None
# prodt = None
# proca = None
# equip = None
