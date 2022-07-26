import re

import pandas as pd

data = pd.read_excel("中国以外世界钢厂列表(产量产能单位为万吨).xlsx")


def Select(x):

    if x["自备焦炉"] == "是" and re.search(r"运营", x["状态"]):
        return True
    else:
        return False


coking_plants = data[data.apply(lambda x: Select(x), axis=1)].copy()
coking_plants.reset_index(inplace=True, drop=True)


def Capacity(x):
    steel = f"{int(x['粗钢总产能(万吨)'])}万吨" if pd.notnull(x['粗钢总产能(万吨)']) else "未知"
    coke = f"{int(x['焦化产能(万吨)'])}万吨" if pd.notnull(x['焦化产能(万吨)']) else "未知"

    return f"粗钢产能{steel}; 焦化产能{coke}"


def Name(x):
    name1 = x['工厂名称(英文)']
    name2 = f"({x['工厂名称(所在国)']})" if pd.notnull(x['工厂名称(所在国)']) else ""

    return name1 + name2


coking_plants['Capacity'] = coking_plants.apply(lambda x: Capacity(x), axis=1)
coking_plants['Name'] = coking_plants.apply(lambda x: Name(x), axis=1)

coking_plants[['Name', '国家(中文)', '位置', '自备焦炉', 'Capacity', '经度坐标', '纬度坐标']].to_excel('coking_plants.xlsx')
