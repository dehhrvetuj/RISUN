import re
import requests
from requests.adapters import HTTPAdapter, Retry
import pandas as pd
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
    AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}

def GetWikiPageContent(url):

    if url is None:
        return None, None

    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"]
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount("https://", adapter)
    http.mount("http://", adapter)

    try:
        web_text = http.get(url, headers=headers).text
    except:
        return None, None

    # web_text = requests.get(url, headers=headers, timeout=10).text
    web_html = etree.HTML(web_text)

    title = None
    content = None

    # Find Page Title
    xpath = '//*[@id="firstHeading"]/text()'
    info = web_html.xpath(xpath)

    if info is None or len(info) < 1:
        pass
    else:
        title = ''.join(info)

    # Find Table Content
    xpath = '//table[@class="infobox vcard"]/tbody/tr'
    info = web_html.xpath(xpath)

    if info is None or len(info) < 1:
        pass
    else:
        content = [item.xpath('./descendant::*/text()') for item in info \
               if item.xpath('./descendant::*/text()')]

    return title, content



#
# url = 'https://en.wikipedia.org/wiki/Port_of_Durr%C3%ABs'
# # url = 'https://en.wikipedia.org/wiki/Port_of_Shanghai'
# web_text = requests.get(url, headers=headers).text
#
# xpath = '//*[@id="mw-content-text"]/div[1]/table/tbody/tr'
# xpath = '//table[@class="infobox vcard"]/tbody/tr'
# xpath = '//table[@class="infobox vcard"]/tbody/descendant-or-self::*/text()'
# xpath = '//table[@class="infobox vcard"]/tbody/tr[th[contains(descendant-or-self::*/text(),"Coordinates")]]'
# xpath = '//table[@class="infobox vcard"]/tbody/tr'
#
# # xpath = '//*[@id="firstHeading"]/text()'
#
# # //*[@id="mw-content-text"]/div[1]/table/tbody/tr[5]
# #  //*[@id="mw-content-text"]/div[1]/table/tbody/tr[6]/th/a
#
# # print(web_text)
#
# web_html = etree.HTML(web_text)
# info = web_html.xpath(xpath)
# print(info)
#
# for item in info:
#     print(item.xpath('./descendant::*/text()'))
#
#
# # for item in info:
# #     print(item.tag, item.text, item.tail)
# #     print(item.xpath('./descendant-or-self::*/text()'))
#
# # for item in info:
# #     print(item.tag, item.text)
# #     print(item.xpath('/descendant-or-self::*/text()'))
#
# # print(web_html.xpath('normalize-space(//*[@id="mw-content-text"]/div[1]/table/tbody)'))
# # print(web_html.xpath('normalize-space(//table[@class="infobox vcard"])'))
#
#
#
# # print(info)
# # for item in info:
# #     print(item.tag, item.text, item.tail)
#     # item.xpath.string()
#     # print(item.xpath('string()'))
#
# # def searchElement(node):
# #
# #     if not node:
# #         return
# #     else:
# #         for item in node:
# #             if item.text is not None:
# #                 print(item.text)
# #             searchElement(item)
# #
# #
# # searchElement(info)
#
