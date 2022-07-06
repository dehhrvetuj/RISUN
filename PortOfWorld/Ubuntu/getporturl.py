import re
import requests
import pandas as pd
from lxml import etree
from webutility import *

# https://www.seabaycargo.com/seaport/detail/Qinhuangdao_China_CNSHF.html
# https://www.findaport.com/dashboard
# https://www.marinetraffic.com/en/ais/details/ports/1253?name=SHANGHAI&country=China#Statistics
# https://www.cargorouter.com/directory/ports/China/Shanghai/

# 
# 

#df = pd.read_excel('./Seaports-of-the-World.xlsx', header=3)

# print(df.head())
# print(df)

# search_keys = ["Port of " + name + ' wikipedia' for name in df['Port']]
# print(search_keys)

# ~ from port_names import *
# ~ from g_search_links import *

# ~ GoogleSearch2(search_keys)

# ~ lst_keys = list()

# ~ for key, links in zip(search_keys,g_search_links):
	# ~ if links is not None and len(links) >= 3:
		# ~ print(key,',          OK')
	# ~ else:
		# ~ print(key, '           NO')
		# ~ lst_keys.append(key)


# ~ GoogleSearch2(lst_keys)

# ~ print(len(search_keys),len(g_search_links))

# ~ I = 0

# ~ for ind in range(0,820):
	# ~ key = search_keys[ind]
	# ~ links = g_search_links[ind]
	
	# ~ if links is not None and len(links) >= 3:
		# ~ print(links,',')
	# ~ else:
		# ~ print(recovered_search_links[I],',')
		# ~ I = I + 1
		
		

# --------------------------------- #
from port_names import port_names
# print(port_names)

from port_names import search_keys
# print(search_keys)

from g_search_links2 import g_search_links
# print(g_search_links)

def SelectWikiLink(lst_of_links):
    for link in lst_of_links:
        # print(link)
        if link is None or len(link) < 1:
            continue
        if re.search(r"en\.wikipedia.org/wiki/Port_of", link, re.I) is not None:
            # print(link)
            # print(1)
            return link
        elif re.search(r"en\.wikipedia.org/wiki/\S+_port$", link, re.I) is not None:
            # print(link)
            # print(2)
            return link
        elif re.search(r"en\.wikipedia.org/wiki/\S+_(harbor|harbour)$", link, re.I) is not None:
            # print(link)
            # print(3)
            return link
        else:
            continue

    return None

ports_global = list()

for name,key,links in zip(port_names,search_keys,g_search_links):
    port = dict()
    port['name'] = name
    port['key'] = key
    port['wiki'] = SelectWikiLink(links)

    ports_global.append(port)


