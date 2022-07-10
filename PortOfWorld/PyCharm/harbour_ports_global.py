import re
import pandas as pd
import numpy as np

# Load Ports from Seabay and Ports from Worldportsource
wordport_ports_global = pd.read_excel('worldportsource.xlsx', index_col=0)


# Droping Row Criteria
def drop_rows(row):
    if pd.isnull(row['type']) or pd.isnull(row['code']) or pd.isnull(row['size']):
        return False
    elif row['size'] == 'Very Small':
        return False
    elif row['type'] in {'Off-Shore Terminal','Waterway Region','Pier, Jetty or Wharf','Marina','Canal', 'Ferry'}:
        return False
    else:
        return True

# Drop rows and reset index (NBS: drop=True)
wordport_ports_global = wordport_ports_global.loc[wordport_ports_global.apply(lambda x: drop_rows(x), axis=1)]
wordport_ports_global.reset_index(inplace=True, drop=True)

# Translate into Chinese
from trans_chinese import trans_country, port_cate, port_type, port_size

wordport_ports_global['纬度坐标'] = wordport_ports_global['latitude'].apply(lambda x: ''.join(x.split(' ')))
wordport_ports_global['经度坐标'] = wordport_ports_global['longitude'].apply(lambda x: ''.join(x.split(' ')))

wordport_ports_global['国家(英文)'] = wordport_ports_global['country']
wordport_ports_global['国家(中文)'] = wordport_ports_global['country'].apply(lambda x: trans_country(x))

wordport_ports_global['所在地'] = wordport_ports_global['location']

wordport_ports_global['港口名称'] = wordport_ports_global['name']
wordport_ports_global['港口代码'] = wordport_ports_global['code']

wordport_ports_global['港口大小'] = wordport_ports_global['size'].apply(lambda x: port_size[x] if not pd.isnull(x) else None)
wordport_ports_global['港口说明'] = wordport_ports_global['type'].apply(lambda x: port_type[x] if not pd.isnull(x) else None)
wordport_ports_global['管理单位'] = wordport_ports_global['authority']


# Write to Excel file
harbour_ports = wordport_ports_global[['国家(中文)', '国家(英文)', '港口名称', '所在地', '港口代码',  '纬度坐标',
                           '经度坐标', '港口大小', '港口说明', '管理单位']]
harbour_ports.index += 1
harbour_ports.to_excel('yyyyy.xlsx')