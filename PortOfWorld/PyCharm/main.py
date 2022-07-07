import re
import pandas as pd
from webutility import GoogleSearch2
from getwikicontent import GetWikiPageContent
from getporturl import SelectWikiLink

# https://www.seabaycargo.com/seaport/detail/Qinhuangdao_China_CNSHF.html
# https://www.findaport.com/dashboard
# https://www.marinetraffic.com/en/ais/details/ports/1253?name=SHANGHAI&country=China#Statistics
# https://www.cargorouter.com/directory/ports/China/Shanghai/
# https://www.vesselfinder.com/ports
# http://www.worldportsource.com/ports/commerce/CHN_Port_of_Qingdao_408.php

# ------------------------------------------------------------ #
# df = pd.read_excel('../Seaports-of-the-World.xlsx', header=3)
# print(df.head())
# print(df)
#
# port_names = list(df['Port'])
# print(port_names)
#
# search_keys = ["Port of " + name + ' wikipedia' for name in port_names]
# print(search_keys)
#
# g_search_links = GoogleSearch2(search_keys)

# ports_global = list()
# for name,key,links in zip(port_names,search_keys,g_search_links):
#     port = dict()
#     port['name'] = name
#     port['key'] = key
#     port['wiki'] = SelectWikiLink(links)
#
#     print(port,',')
#     ports_global.append(port)

# for port in ports_global:
#     link = port['wiki']
#
#     if  link is None:
#         port['name2'] = None
#         port['wiki_content'] = None
#     else:
#         port['name2'], port['wiki_content'] = GetWikiPageContent(link)
#
#     print({'name':port['name'], 'name2':port['name2'], 'wiki':port['wiki'],
#            'wiki_content':port['wiki_content']},',')

# ------------------------------------ #
from port_names import port_names
# print(port_names)

from port_names import search_keys
# print(search_keys)

from g_search_links2 import g_search_links
# # print(g_search_links)

from ports_global import ports_global
# print(ports_global)

from ports_wiki_contents import ports_global_content
# print(ports_global_content)


from searchwikicontents import *

for port in ports_global_content:

    contents = port['wiki_content']

    if contents is None:
        continue

    country = [SearchForCountry(item) for item in contents]
    country = ''.join([item for item in country if item is not None])

    location = [SearchForLocation(item) for item in contents]
    location = ''.join([item for item in location if item is not None])

    latti = [SearchForCoordinates(item,'lattitude') for item in contents]
    latti = ''.join([item for item in latti if item is not None])

    longi = [SearchForCoordinates(item,'longitude') for item in contents]
    longi = ''.join([item for item in longi if item is not None])

    cargo = [SearchForCargo(item) for item in contents]
    cargo = ''.join([item for item in cargo if item is not None])

    container = [SearchForContainer(item) for item in contents]
    container = ''.join([item for item in container if item is not None])

    print(':'.join([country, port['name'], port['name2'], location, latti, longi, cargo, container]))
    # print(port['name'], country, latti, longi, cargo, container)


# print(re.findall(r"\-?\d+°\d+′\d+″[NS]", '29°56′13″N'))

# print(SearchForCountry(['Country', '\xa0', 'Ukraine']))

