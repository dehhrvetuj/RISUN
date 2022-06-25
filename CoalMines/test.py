import mines_url
import mines_detail
import pandas as pd
from labels import *
import re


data = pd.DataFrame(mines_detail.mines_global)
# data = data.loc[400:405]

data['Name'] = data['name']
data['Country'] = data['country']
data['Source'] = data['url']
data['GPS'] = pd.concat([data[ind] for ind in gps_ind]).dropna().reindex_like(data)
data['Status'] = pd.concat([data[ind] for ind in status_ind]).dropna().reindex_like(data)
data['Coal Type'] = pd.concat([data[ind] for ind in coal_type_ind]).dropna().reindex_like(data)
data['Mine Type'] = pd.concat([data[ind] for ind in mine_type_ind]).dropna().reindex_like(data)
data['Mine Size'] = pd.concat([data[ind] for ind in mine_size_ind]).dropna().reindex_like(data)
data['Mine Method'] = pd.concat([data[ind] for ind in mine_method_ind]).dropna().reindex_like(data)
data['Start Year'] = pd.concat([data[ind] for ind in start_year_ind]).dropna().reindex_like(data)
data['End Year'] = pd.concat([data[ind] for ind in end_year_ind]).dropna().reindex_like(data)
data['Owner'] = pd.concat([data[ind] for ind in owner_ind]).dropna().reindex_like(data)
data['Operator'] = pd.concat([data[ind] for ind in operator_ind]).dropna().reindex_like(data)
data['Sponsor'] = pd.concat([data[ind] for ind in sponsor_ind]).dropna().reindex_like(data)
data['Parent'] = pd.concat([data[ind] for ind in parent_ind]).dropna().reindex_like(data)


def GetLattitudeLongitude(coordinates, flag):
    if not pd.isnull(coordinates):
        coord = re.findall(r"\-?\d+\.?\d*", coordinates)
    else:
        return None

    if len(coord) == 2:
        return float(coord[0]) if flag == 'lattitude' else float(coord[1])
    else:
        return None

data['Lattitude'] = data['GPS'].apply(lambda x: GetLattitudeLongitude(x,'lattitude'))
data['Longitude'] = data['GPS'].apply(lambda x: GetLattitudeLongitude(x,'longitude'))



output = data[['Name','Country','Source','Location','Lattitude','Longitude','Status','Coal Type','Mine Type','Mine Size',
            'Mine Method','Start Year','End Year','Owner','Operator','Sponsor','Parent']]

# print(output)

output.to_excel('test.xlsx')





#
#
#
# name = data['name']
# source = data['url']
# country = data['country']
# location = data['Location']
# gps_coord = data['GPS Coordinates']
#
# status = data['Status']
# coal_type = data['Coal type']
# mine_type = data['Mine Type']
# mine_size = data['Mine size']
# start_year = data['Start Year']
# operator = data['Operator']
# owner = data['Owner']
# pro_cap = data['Production Capacity']
# parent = data['Parent company'] # 'Parent Company'  'Parent', '# Parent company of the operator' '# Operator's parent company'
#













# mines_global = mines_url.mines_global
#
# # print(mines_global)
#
#
# for mine in mines_global:
#     if mine['country'] == ' China':
#         continue
#     xpath = '//*[@id="mw-content-text"]/div/ul[1]/li/b'
#     info = GetHTMLElementList(mine['url'], xpath)
#     for item in info:
#         if item.text is not None:
#             key = item.text.replace(':','').strip()
#             if item.tail is not None:
#                 mine[key] = item.tail.replace(':','').strip()
#             else:
#                 mine[key] = None
#         else:
#             pass
#
#     print(mine,',')