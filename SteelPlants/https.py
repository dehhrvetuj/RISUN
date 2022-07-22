import requests
from requests.adapters import HTTPAdapter, Retry
from lxml import etree

headers = {
    'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
    AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}

base_url = 'https://www.gem.wiki'

retry_strategy = Retry(
    total=3,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"])

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

    return etree.HTML(web_text)
