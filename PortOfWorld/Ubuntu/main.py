import re
import requests
# import pandas as pd
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
    AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}

url = 'https://en.wikipedia.org/wiki/Port_of_Durr%C3%ABs'
url = 'https://en.wikipedia.org/wiki/Port_of_Shanghai'
web_text = requests.get(url, headers=headers).text

xpath = '//*[@id="mw-content-text"]/div[1]/table/tbody/tr'


# //*[@id="mw-content-text"]/div[1]/table/tbody/tr[5]
#  //*[@id="mw-content-text"]/div[1]/table/tbody/tr[6]/th/a

# print(web_text)
web_html = etree.HTML(web_text)
info = web_html.xpath(xpath)

# print(web_html.xpath('normalize-space(//*[@id="mw-content-text"]/div[1]/table/tbody)'))

# print(info)
# for item in info:
#     print(item.tag, item.text, item.tail)
    # item.xpath.string()
    # print(item.xpath('string()'))

def searchElement(node):

    if not node:
        return
    else:
        for item in node:
            if item.text is not None:
                print(item.text)
            searchElement(item)


searchElement(info)





# -------------------------------------------------------------------- #
def GetHTMLElementList(url, xpath):

    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
        AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}

    try:
        web_text = requests.get(url, headers=headers).text
    except requests.exceptions.RequestException:
        return list()

    web_html = etree.HTML(web_text)

    return web_html.xpath(xpath)