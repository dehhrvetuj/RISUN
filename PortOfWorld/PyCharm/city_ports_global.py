import re
import pandas as pd
import numpy as np

# Load Ports from Seabay and Ports from Worldportsource
seabay_ports_global = pd.read_excel('seabaycargo-ports-global.xlsx', index_col=0)
seabay_ports_global2 = pd.read_excel('seabaycargo-ports-global2.xlsx', index_col=0)
seabay_ports_global = seabay_ports_global.append(seabay_ports_global2, ignore_index=True)
seabay_ports_global.drop_duplicates(inplace=True)

wordport_ports_global = pd.read_excel('worldportsource.xlsx', index_col=0)
vesselfinder_ports_global = pd.read_excel('vesselfinder.xlsx', index_col=0)

# print(set(seabay_ports_global['country']))
# print(set(wordport_ports_global['type']))


# Select only City Port, drop Dry Port (keep Main Port and Feeder Port)
city_ports_global = seabay_ports_global[seabay_ports_global['category'] == 'City Port']
city_ports_global = city_ports_global[city_ports_global['type'] != 'Dry Port']
city_ports_global.reset_index(inplace=True, drop=True)

# Rename 'type: {Seaport, River port, etc.}' as 'port_type'; 'link' -> 'WPS_link'
wordport_ports_global.rename({'type': 'port_type', 'link': 'WPS_link'}, axis='columns', inplace=True)
# Rename 'code' in vesselfinder as 'code2'
# vesselfinder_ports_global.rename({'code': 'code2'}, axis='columns', inplace=True)


# Prepare to Copy (size, authority, port type) from Seabay ports; Copy cod2 from vesselfinder
city_ports_global['size'] = None
# city_ports_global['code2'] = None
city_ports_global['authority'] = None
city_ports_global['port_type'] = None
city_ports_global['latitude'] = None
city_ports_global['longitude'] = None
city_ports_global['WPS_link'] = None

# ------------------------ Update 0th Round --------------------------------#
# Use the first two letters in 'code' to represent country
wordport_ports_global['country_code'] = wordport_ports_global['code'].apply(lambda x: x[0:2] if not pd.isnull(x) else None)
vesselfinder_ports_global['country_code'] = vesselfinder_ports_global['code'].apply(lambda x: x[0:2] if not pd.isnull(x) else None)
city_ports_global['country_code'] = city_ports_global['code'].apply(lambda x: x[0:2] if not pd.isnull(x) else None)

# Remove/Drop duplicates of both name and country and reset index
wordport_ports_global.drop_duplicates(subset=['name','country_code'], keep='first', inplace=True)
vesselfinder_ports_global.drop_duplicates(subset=['name','country_code'], keep='first', inplace=True)

wordport_ports_global.reset_index(inplace=True, drop=True)
vesselfinder_ports_global.reset_index(inplace=True, drop=True)

# Set 'name' and 'country_code' as index
wordport_ports_global.set_index(['name','country_code'], inplace=True)
vesselfinder_ports_global.set_index(['name','country_code'], inplace=True)
city_ports_global.set_index(['name','country_code'], inplace=True)

# Update city ports by Seabay and Vesselfinder information based on 'name' & 'country_code'
city_ports_global.update(wordport_ports_global[['port_type', 'size', 'authority', 'WPS_link']])
city_ports_global.update(vesselfinder_ports_global[['latitude', 'longitude']])

# Set back index
wordport_ports_global.reset_index(inplace=True)
vesselfinder_ports_global.reset_index(inplace=True)
city_ports_global.reset_index(inplace=True)

# ------------------------ Update 1st - 1 Round --------------------------------#
# Remove/Drop duplicates of both name and country and reset index
wordport_ports_global.drop_duplicates(subset=['name','country'], keep='first', inplace=True)
wordport_ports_global.reset_index(inplace=True, drop=True)

# Make a new column as port name like 'Port of Shanghai'
city_ports_global['port_of_name'] = city_ports_global['name'].apply(lambda x: f"Port of {x.strip()}")

# Set port name (Port of XXX) and country as the index
city_ports_global.set_index(['port_of_name','country'], inplace=True)
wordport_ports_global.set_index(['name','country'], inplace=True)

# Update city ports by Seabay ports information based on 'port of name' and 'country'
city_ports_global.update(wordport_ports_global[['port_type', 'size', 'authority', 'WPS_link']])

# Set back the index of both port sources
city_ports_global.reset_index(inplace=True)
wordport_ports_global.reset_index(inplace=True)

# ------------------------ Update 1st - 2 Round --------------------------------#

# Remove/Drop duplicates of both name and country and reset index
wordport_ports_global.drop_duplicates(subset=['name','country_code'], keep='first', inplace=True)
wordport_ports_global.reset_index(inplace=True, drop=True)

# Make a new column as port name like 'Port of Shanghai'
city_ports_global['port_of_name'] = city_ports_global['name'].apply(lambda x: f"Port of {x.strip()}")

# Set port name (Port of XXX) and country as the index
city_ports_global.set_index(['port_of_name','country_code'], inplace=True)
wordport_ports_global.set_index(['name','country_code'], inplace=True)

# Update city ports by Seabay ports information based on 'port of name' and 'country'
city_ports_global.update(wordport_ports_global[['port_type', 'size', 'authority', 'WPS_link']])

# Set back the index of both port sources
city_ports_global.reset_index(inplace=True)
wordport_ports_global.reset_index(inplace=True)

# Remove the column 'port_of_name'
city_ports_global.drop(columns=['port_of_name'], inplace=True)

# ----------------- Update 2nd Round -------------------------------------------#
# Remove rows/Drop duplicates of 'code' and reset in the index
wordport_ports_global.drop_duplicates(subset=['code'], keep='first', inplace=True)
wordport_ports_global.reset_index(inplace=True, drop=True)

# Set port code as index
city_ports_global.set_index(['code'], inplace=True)
wordport_ports_global.set_index(['code'], inplace=True)
vesselfinder_ports_global.set_index(['code'], inplace=True)

# Update city ports from Seabay ports information based on 'code'
city_ports_global.update(wordport_ports_global[['port_type', 'size', 'authority', 'WPS_link']])
city_ports_global.update(vesselfinder_ports_global[['latitude', 'longitude']])

# Set back the index of both sources
city_ports_global.reset_index(inplace=True)
wordport_ports_global.reset_index(inplace=True)
vesselfinder_ports_global.reset_index(inplace=True)

# ----------------- Update 3rd - 1 Round ----------------------------------------------#
# Remove rows/Drop duplicates of 'location' and 'country' and reset in the index
wordport_ports_global.drop_duplicates(subset=['location','country'], keep='first', inplace=True)
wordport_ports_global.reset_index(inplace=True, drop=True)

vesselfinder_ports_global.drop_duplicates(subset=['name','country'], keep='first', inplace=True)
vesselfinder_ports_global.reset_index(inplace=True, drop=True)

# Set location/name and country as index
city_ports_global.set_index(['name','country'], inplace=True)
wordport_ports_global.set_index(['location','country'], inplace=True)
vesselfinder_ports_global.set_index(['name','country'], inplace=True)

# Update city ports from Seabay ports information
city_ports_global.update(wordport_ports_global[['port_type', 'size', 'authority', 'WPS_link']])
city_ports_global.update(vesselfinder_ports_global[['latitude', 'longitude']])

# Set back the index of both sources
city_ports_global.reset_index(inplace=True)
wordport_ports_global.reset_index(inplace=True)
vesselfinder_ports_global.reset_index(inplace=True)

# ----------------- Update 3rd - 2 Round ----------------------------------------------#
# Remove rows/Drop duplicates of 'location' and 'country' and reset in the index
wordport_ports_global.drop_duplicates(subset=['location','country_code'], keep='first', inplace=True)
wordport_ports_global.reset_index(inplace=True, drop=True)

vesselfinder_ports_global.drop_duplicates(subset=['name','country_code'], keep='first', inplace=True)
vesselfinder_ports_global.reset_index(inplace=True, drop=True)

# Set location/name and country as index
city_ports_global.set_index(['name','country_code'], inplace=True)
wordport_ports_global.set_index(['location','country_code'], inplace=True)
vesselfinder_ports_global.set_index(['name','country_code'], inplace=True)

# Update city ports from Seabay ports information
city_ports_global.update(wordport_ports_global[['port_type', 'size', 'authority', 'WPS_link']])
city_ports_global.update(vesselfinder_ports_global[['latitude', 'longitude']])

# Set back the index of both sources
city_ports_global.reset_index(inplace=True)
wordport_ports_global.reset_index(inplace=True)
vesselfinder_ports_global.reset_index(inplace=True)



# Droping Row Criteria
def drop_rows(row):
    if pd.isnull(row['type']):
        return False
    elif row['size'] == 'Very Small':
        return False
    elif row['port_type'] in {'Off-Shore Terminal','Waterway Region','Pier, Jetty or Wharf','Marina',
                              'Canal', 'Ferry'}:
        return False
    elif pd.isnull(row['size']) and pd.isnull(row['longitude']) and row['type'] == 'Feeder Port':
        return False
    else:
        return True

# Drop rows and reset index (NBS: drop=True)
city_ports_global = city_ports_global.loc[city_ports_global.apply(lambda x: drop_rows(x), axis=1)]
city_ports_global.reset_index(inplace=True, drop=True)

# Translate into Chinese
from trans_chinese import trans_country, port_cate, port_type, port_size
city_ports = city_ports_global
city_ports['国家(英文)'] = city_ports['country']
city_ports['国家(中文)'] = city_ports['country'].apply(lambda x: trans_country(x))
city_ports['城市(英文)'] = city_ports['name']
city_ports['港口代码'] = city_ports['code']
city_ports['纬度坐标'] = city_ports['latitude']
city_ports['经度坐标'] = city_ports['longitude']
city_ports['港口分类'] = city_ports['type'].apply(lambda x: port_cate[x] if not pd.isnull(x) else None)
city_ports['港口大小'] = city_ports['size'].apply(lambda x: port_size[x] if not pd.isnull(x) else None)
city_ports['港口说明'] = city_ports['port_type'].apply(lambda x: port_type[x] if not pd.isnull(x) else None)
city_ports['管理单位'] = city_ports['authority']


# city_ports_global.to_excel('yyyyyyyyy.xlsx')

# Write to Excel file
city_ports = city_ports[['国家(中文)', '国家(英文)', '城市(英文)', '港口代码', '港口分类', '纬度坐标',
                         '经度坐标', '港口大小', '港口说明', '管理单位']].copy()
city_ports.sort_values(by=['国家(英文)','城市(英文)'], ascending=True, inplace=True, ignore_index=True)

city_ports.index += 1
city_ports.to_excel('xxxxx.xlsx')

# print(list(city_ports_global['name']))

