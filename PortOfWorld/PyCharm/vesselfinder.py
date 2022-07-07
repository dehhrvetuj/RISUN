import re
import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
import numpy as np
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
    AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}

base_url = 'https://www.vesselfinder.com'

retry_strategy = Retry(
    total = 2,
    status_forcelist = [429, 500, 502, 503, 504],
    allowed_methods = ["HEAD", "GET", "OPTIONS"])

adapter = HTTPAdapter(max_retries=retry_strategy)
http = requests.Session()
http.mount("https://", adapter)
http.mount("http://", adapter)
http.get(base_url)

def HTTPRequestHTML(url):
    if url is None:
        return None

    try:
        global http
        web_text = http.get(url, headers=headers).text
    except:
        return None

    return  etree.HTML(web_text)


lst_name = list()
lst_country = list()
lst_code = list()
lst_url = list()


def CrawlVesselFinderPage(page_url):

    try:
        page = HTTPRequestHTML(page_url)

        next_page = next(iter(page.xpath('/html/body/div/div/main/div[1]/nav[1]/a[2]/@href')), None)

        xpath = '/html/body/div/div/main/div[1]/section/table/tbody/tr'

        name = page.xpath(xpath + '/td[1]/div/a/div[1]/text()')
        country = page.xpath(xpath + '/td[1]/div/a/div[2]/text()')
        code = page.xpath(xpath + '/td[2]/text()')
        url = page.xpath(xpath + '/td[1]/div/a/@href')

        return next_page, name, country, code, url

    except:
        return None, None, None, None, None


def CrawlVesselFinderAllPages(next_page):

    global base_url
    next_page, name, country, code, url = CrawlVesselFinderPage(base_url + next_page)

    global lst_name, lst_country, lst_code, lst_url
    lst_name = lst_name + name
    lst_country = lst_country + country
    lst_code = lst_code + code
    lst_url = lst_url + url

    if pd.isnull(next_page):
        return
    else:
        CrawlVesselFinderAllPages(next_page)


def CrawlVesselFinderGPS(port_url):

    global base_url

    try:
        page = HTTPRequestHTML(base_url + port_url)
        text = page.xpath('/html/body/div[1]/div/main/div/div[3]/p/text()')

        coord = re.findall(r"\-?\d+\.?\d+\s?[NSEW]", next(iter(text),""))

        print(coord[0], coord[1])
        return coord[0], coord[1]

    except:
        return None, None


# CrawlVesselFinderAllPages('/ports')

# ports_all = pd.DataFrame(np.column_stack([lst_name, lst_country, lst_code, lst_url]),
#                          columns=['name','country','code','url'])
#
# ports_all.to_excel('ports_all_world.xlsx')

# ports_all['coord'] = ports_all['url'].apply(lambda x: CrawlVesselFinderGPS(x))
#
# ports_all.to_excel('ports_all_world.xlsx')

ports_all = pd.read_excel('ports_all_world.xlsx')
print(ports_all.head())

ports_all['lattitude'] = ports_all['coord'].apply(lambda x: eval(eval(x)[0].replace('N','').replace('S','*-1')))
ports_all['longitude'] = ports_all['coord'].apply(lambda x: eval(eval(x)[1].replace('E','').replace('W','*-1')))

output = ports_all[['name','country','code','lattitude','longitude']]
output.index = output.index + 1

output.to_excel('ports_all_world2.xlsx')
