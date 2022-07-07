import re
import requests
import pandas as pd
from lxml import etree
from webutility import *


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
        elif re.search(r"en\.wikipedia.org/wiki/Puerto_", link, re.I) is not None:
            # print(link)
            # print(4)
            return link
        else:
            continue

    return None



# print(SelectWikiLink(['https://en.wikipedia.org/wiki/Limetree,_U.S._Virgin_Islands_ports']))

# link = 'https://en.wikipedia.org/wiki/Virgin_Islands_harbour_'
#
# print(re.search(r"en\.wikipedia.org/wiki/.+_[harbor|harbour]", link, re.I) )

