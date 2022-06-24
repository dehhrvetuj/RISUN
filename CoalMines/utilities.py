import requests
from lxml import etree

# ---------------------------------------------- #
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
