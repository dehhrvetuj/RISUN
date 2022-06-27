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


def GetLattitudeLongitude(coord_string, flag='longitude'):
    if pd.isnull(coord_string):
        return None

    coord_string = re.sub(r"[\(\[].*?[\)\]]", " ", coord_string)

    coord = re.findall(r"\-?\d+\.?\d*", coord_string)

    coord = [float(item) for item in coord]

    latti = None
    longi = None

    if len(coord) == 2:
        latti = coord[0]
        longi = coord[1]

    if len(coord) == 4:
        import numpy as np
        first = coord[0]
        coord = np.array(coord)
        coord_diff = (coord-first) * (coord-first)
        sorted_id = np.argsort(coord_diff)

        latti = (coord[sorted_id[0]] + coord[sorted_id[1]])/2.0
        longi = (coord[sorted_id[2]] + coord[sorted_id[3]])/2.0

    return latti if flag == 'lattitude' else longi


data['Lattitude'] = data['GPS'].apply(lambda x: GetLattitudeLongitude(x,'lattitude'))
data['Longitude'] = data['GPS'].apply(lambda x: GetLattitudeLongitude(x,'longitude'))

def GetNumAndUnit(num_string, minmax='max'):
    if pd.isnull(num_string):
        return None

    if 'million' in num_string.lower() or 'mtpa' in num_string.lower() or ' M' in num_string:
        convert = 1
    else:
        convert = 1e-6
    if 'per month' in num_string.lower():
        convert = convert*12

    # years = re.findall(r"20[1-2][0-9]", num_string)   # find 2018, 2019, 2020 etc.
    # if len(years) >= 1:
    #     years = [int(year) for year in years]

    numbers = re.sub(r"[\(\[].*?[\)\]]", " ", num_string)   # remove contents in parenthesis
    numbers = re.sub(r"20[0-2][0-9]", " ", numbers)     # remove 2018, 2019, 2020 etc.
    numbers = re.findall(r"\.?\d{1,3}(?:\,\d{1,3})*\.?\d*", numbers)

    numbers = [float(num.replace(',','')) for num in numbers]


    if len(numbers) > 0:
        if minmax == 'max':
            return max(numbers)*convert
        elif minmax == 'min':
            return min(numbers)*convert
        else:
            return None
    else:
        # print(num_string, numbers)
        return None

    # if len(numbers) == 1:
    #     return float(numbers[0]) * convert
    # elif len(numbers) >= 2 and len(years) >= 2:
    #
    #     ind = years.index(max(years)) if years.index(max(years))<len(numbers) else len(numbers)-1
    #     # print(num_string, "   ", numbers, ind)
    #     return float(numbers[ind]) * convert
    # else:
    #     print(num_string, "   ", numbers)
    #     return None




data['Production(short)'] = pd.concat([data[ind] for ind in prod_short_ind]).dropna().reindex_like(data)
data['Production(short) Max'] = data['Production(short)'].apply(lambda x: GetNumAndUnit(x,'max'))
data['Production(short) Min'] = data['Production(short)'].apply(lambda x: GetNumAndUnit(x,'min'))

data['Production(metric)'] = pd.concat([data[ind] for ind in prod_metric_ind]).dropna().reindex_like(data)
data['Production(metric) Max'] = data['Production(metric)'].apply(lambda x: GetNumAndUnit(x,'max'))
data['Production(metric) Min'] = data['Production(metric)'].apply(lambda x: GetNumAndUnit(x,'min'))

data['Production capacity (Mtpa)'] = data['Production capacity (Mtpa)'].apply(lambda x: None if pd.isnull(x) else str(x) + ' (mtpa) ')
data['Capacity (Mtpa)'] = data['Capacity (Mtpa)'].apply(lambda x: None if pd.isnull(x) else str(x) + ' (mtpa) ')
data['capacity (Mtpa)'] = data['capacity (Mtpa)'].apply(lambda x: None if pd.isnull(x) else str(x) + ' (mtpa) ')

data['Capacity of Production'] = pd.concat([data[ind] for ind in prod_cap_ind]).dropna().reindex_like(data)
data['Capacity of Production (MTPA)'] = data['Capacity of Production'].apply(lambda x: GetNumAndUnit(x))

# output = data[['Name','Country','Source','Location','Lattitude','Longitude','Status','Coal Type','Mine Type','Mine Size',
#             'Mine Method','Start Year','End Year', 'Production(metric)','Production(short)', 'Production(short)-',
#                'Owner','Operator','Sponsor','Parent']]

# output = data[['Name','Country','Source', 'GPS', 'Lattitude', 'Longitude',
#                'Production(metric)','Production(metric) Max','Production(metric) Min',
#                'Production(short)','Production(short) Max','Production(short) Min',
#                'Capacity of Production', 'Capacity of Production (MTPA)']]

output = data[['Name','Country','Location','Lattitude','Longitude','Status',
               'Coal Type','Mine Type','Mine Size','Mine Method','Start Year','End Year',
                'Production(metric) Max','Production(metric) Min',
               'Production(short) Max','Production(short) Min',
               'Capacity of Production (MTPA)',
               'Owner','Operator','Sponsor','Parent',
               'Source', 'GPS',
               'Production(metric)','Production(short)',
               'Capacity of Production']]

output.index = output.index + 1
output.to_excel('test.xlsx')
#

# print(GetNumAndUnit('700,000 t/year (as of 2008)' ))