import mines_url
import mines_detail
import mines_detail
import pandas as pd
from labels import *

data = pd.DataFrame(mines_detail.mines_global)
# data = data.loc[400:405]


data['GPS'] = pd.concat([data[ind] for ind in gps_ind]).dropna().reindex_like(data)
data['Status'] = pd.concat([data[ind] for ind in status_ind]).dropna().reindex_like(data)
data['Coal_Type'] = pd.concat([data[ind] for ind in coal_type_ind]).dropna().reindex_like(data)
data['Mine_Type'] = pd.concat([data[ind] for ind in mine_type_ind]).dropna().reindex_like(data)


print(data[['name','Status','Coal_Type','Mine_Type']])

# print(mines)



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