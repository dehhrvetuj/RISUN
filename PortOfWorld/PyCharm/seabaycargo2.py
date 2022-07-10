import re
import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
import numpy as np
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
    AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}

base_url = 'https://www.seabaycargo.com'

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

xpath = '/html/body/div[3]/div[2]/div[1]/div[2]/div[3]/ul[2]/li/a/@href'
xpath_lst = '//*[@id="infoiata"]/tbody/tr'
xpath_next = '//a[@class="next"]/@href'

xpath_link = './td[1]/a/@href'
xpath_name = './td[1]/a/text()'
xpath_code = './td[2]/text()'
xpath_type = './td[2]/font/span/em/text()'
xpath_city = './td[3]/text()'
xpath_cate = './td[4]/text()'
xpath_coun = './td[5]/text()'


lst_name = list()
lst_coun = list()
lst_code = list()
lst_link = list()
lst_type = list()
lst_cate = list()
lst_city = list()


def CrawlSeabayAllPages(page_url):

    try:
        global base_url
        current_page = HTTPRequestHTML(base_url + page_url)

        lst_ports = current_page.xpath(xpath_lst)
        next_page = next(iter(current_page.xpath(xpath_next)), None)

        print(page_url, next_page)

        name = [next(iter(port.xpath(xpath_name)), None) for port in lst_ports]
        link = [next(iter(port.xpath(xpath_link)), None) for port in lst_ports]
        code = [next(iter(port.xpath(xpath_code)), None) for port in lst_ports]
        type = [next(iter(port.xpath(xpath_type)), None) for port in lst_ports]
        cate = [next(iter(port.xpath(xpath_cate)), None) for port in lst_ports]
        coun = [next(iter(port.xpath(xpath_coun)), None) for port in lst_ports]
        city = [next(iter(port.xpath(xpath_city)), None) for port in lst_ports]

    except:
        name = []
        link = []
        code = []
        type = []
        cate = []
        coun = []
        city = []


    global lst_name, lst_coun, lst_code, lst_link, lst_type, lst_cate, lst_city

    lst_name += name
    lst_coun += coun
    lst_code += code
    lst_link += link
    lst_type += type
    lst_cate += cate
    lst_city += city

    print(len(lst_name), len(lst_code), len(lst_coun), len(lst_type), len(lst_cate), len(lst_city), len(lst_link))

    if pd.isnull(next_page):
        return
    else:
        CrawlSeabayAllPages(next_page)


paths = HTTPRequestHTML(base_url + '/seaport').xpath(xpath)
print(len(paths))

for path in paths[0:]:

    try:
        CrawlSeabayAllPages(path)
    except:
        print(lst_name)
        print(lst_coun)
        print(lst_city)
        print(lst_code)
        print(lst_cate)
        print(lst_type)
        print(lst_link)


print(len(lst_name),len(lst_code),len(lst_coun), len(lst_type),len(lst_cate),len(lst_city),len(lst_link))

ports_all = pd.DataFrame(np.column_stack([lst_coun, lst_name, lst_code, lst_city, lst_type, lst_cate, lst_link]),
                         columns=['country','name','code','city','type','category','link'])

# ports_all.to_excel('seabaycargo-ports-global2.xlsx')

