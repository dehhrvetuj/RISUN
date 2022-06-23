# ------------------------------------------------ #
url_parent = 'https://www.gem.wiki'
url_ini = 'https://www.gem.wiki/Category:Global_Coal_Mine_Tracker'


# ---------------------------------------------- #
def GetHTMLElementList(url, xpath):
    import requests
    from lxml import etree
    headers = {
        'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
        AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}

    try:
        web_text = requests.get(url, headers=headers).text
    except requests.exceptions.RequestException:
        return list()

    web_html = etree.HTML(web_text)

    return web_html.xpath(xpath)


# ---------------------------------------------- #
def SearchByCountry(url):
    xpath_0 = '//*[@id="mw-pages"]/div/div/div/ul/li/a'
    xpath_1 = '//*[@id="mw-pages"]/div/ul/li/a'
    xpath_next = '//*[@id="mw-pages"]/a'

    info = GetHTMLElementList(url, xpath_0)
    if not info:
        info = GetHTMLElementList(url, xpath_1)

    # print(len(info), info)

    next_page = [page for page in GetHTMLElementList(url, xpath_next) if 'next page' in page.text]

    if not next_page:
        return info
    else:
        url_next = url_parent + next_page[0].attrib['href']
        # print(url_next)
        info = info + SearchByCountry(url_next)

    return info


# # ----------------------------------------------------------------- #
# url_china = 'https://www.gem.wiki/Category:Coal_mines_in_China'
# url_australia = 'https://www.gem.wiki/Category:Coal_mines_in_Australia'
# url_afghanistan = 'https://www.gem.wiki/Category:Coal_mines_in_Afghanistan'
# url__ = 'https://www.gem.wiki/Category:Coal_mines_in_Swaziland'
#
# info = SearchByCountry(url_australia)


# ------------------ Get URL for Each Country --------------------- #
xpath = '//*[@id="mw-subcategories"]/div/div/div[1]/ul/li'

info = GetHTMLElementList(url_ini, xpath)
info = [ul for ul in info if '/Category:Coal_mines_in_' in ul.find('a').attrib['href']]

name_all_country = [ul.find('a').text.split('Coal mines in')[-1].strip() for ul in info]
url_all_country = [url_parent + ul.find('a').attrib['href'] for ul in info]
# url_all_country = [url_parent + country for country in url_all_country if '/Category:Coal_mines_in_' in country]

coal_mines_all_country = list()

for name_country, url_country in zip(name_all_country, url_all_country):
    country = dict()
    country['Country_Name'] = name_country
    country['Country_url'] = url_country
    coal_mines_all_country.append(country)

# print(coal_mines_all_country)

# ------------------ Search URL by Country --------------------- #
for mine_country in coal_mines_all_country:

    info = SearchByCountry(mine_country['Country_url'])

    print(mine_country['Country_Name'], len(info))

    # mine_country['Mines'] = list()
    # for item in info:
    #     mine = dict()
    #     mine['name'] = item.attrib['title']
    #     mine['url'] = url_parent + item.attrib['href']
    #     mine['country'] = mine_country['Country_Name']
    #     mine_country['Mines'].append(mine)

    country_name = mine_country['Country_Name']
    mine_country['Mines'] = [{'name': item.attrib['title'], 'url': url_parent + item.attrib['href'],
                              'country': country_name} for item in info]
    # print(mine_country)
    # mine_country['Mines_url'] = [url_parent + item.attrib['href'] for item in info]

# ------------------------ Search URL of Each Coal Mine ------------------------ #
mines_global = [mine for mine_country in coal_mines_all_country for mine in mine_country['Mines']]

print('Num of global mines:', len(mines_global))

mines_global = [mine for mine in mines_global if mine['country'] != 'China']
print(mines_global)
# for mine in mines_global:
#     print(mine)

# for mine in mines_global:
#     if mine['country'] == ' China':
#         continue
#     xpath = '//*[@id="mw-content-text"]/div/ul[1]/li/b'
#     info = GetHTMLElementList(mine['url'], xpath)
#     for item in info:
#         if item.text is not None and item.tail is not None:
#             mine[item.text.strip()[0:-1]] = item.tail.strip()
#         elif item.text is not None:
#             mine[item.text[0:-1]] = None
#     print(mine)


# for mine_country in coal_mines_all_country:
#     for mine in mine_country['Mines']:
#         xpath = '//*[@id="mw-content-text"]/div/ul[1]/li/b'
#         info = GetHTMLElementList(mine['url'], xpath)
#         for item in info:
#             if item.text is not None and item.tail is not None:
#                 mine[item.text.strip()[0:-1]] = item.tail.strip()
#             elif item.text is not None:
#                 mine[item.text[0:-1]] = None
#         print(mine)
#
# print(coal_mines_all_country)


# mine = dict()
# xpath = '//*[@id="mw-content-text"]/div/ul[1]/li/b'
# info = GetHTMLElementList('https://www.gem.wiki/Appin_mine', xpath)
# for item in info:
#     # print(item.text)
#     # print(item.tail)
#     if item.text is not None and item.tail is not None:
#         mine[item.text.strip()[0:-1]] = item.tail.strip()
#     elif item.text is not None:
#         mine[item.text[0:-1]] = None
#
# print(mine)

## -------------------------------------------------- ##
# for mine_url in mine_country['Mines_url']:
#     xpath = '//*[@id="mw-content-text"]/div/ul[1]/li/b'
#     info = GetHTMLElementList(mine_url, xpath)
#     print(mine_url)
#     mine = dict()
#     mine['url'] = mine_url
#     mine['details'] = dict()
#     for item in info:
#         print(item.text)
#         print(item.tail)


# url = 'https://www.gem.wiki/Category:Global_Coal_Mine_Tracker'
# xpath = '//*[@id="mw-subcategories"]/div/div/div[1]/ul/li'

# //*[@id="mw-subcategories"]/div/div/div[1]/ul/li[1]

#
# web_text = requests.get(url_ini, headers=headers).text
# web_html = etree.HTML(web_text)
# info = web_html.xpath(xpath)
#
# url_parent = 'https://www.gem.wiki'
#
# url_by_country = [ul.find('a').attrib['href'] for ul in info]
# url_by_country = [url_parent + item for item in url_by_country if '/Category:Coal_mines_in_' in item]
#
#
# print(url_by_country)


# url = 'https://www.gem.wiki/Category:Coal_mines_in_China'
# xpath = '//*[@id="mw-pages"]/div/div'
# xpath = '//*[@id="mw-pages"]/div/div/div/ul/li'
# xpath = '//*[@id="mw-pages"]/div/div/div/ul/li/a'
#
# web_text = requests.get(url, headers=headers).text
# web_html = etree.HTML(web_text)
#
# info = web_html.xpath(xpath)
# print(info)
# # info = info[0]
# #
# for item in info:
#     print(item.attrib['href'])


# url = 'https://www.gem.wiki/Baiyinhua_Haizhou_No.4_Surface_Mine_(Phase_II)'
# xpath = '//*[@id="mw-content-text"]/div/ul[1]/li/b'
#
# web_text = requests.get(url, headers=headers).text
# web_html = etree.HTML(web_text)
#
# info = web_html.xpath(xpath)
# print(info)
#
# key_list = ['Owner', 'Parent', 'Location', 'GPS', 'Status', 'Start',
#             'Mineable reserves', 'Coal type', 'Mine size', 'Mine type', 'Production']
#
# detail = dict()
# for item in info:
#     detail[item.text[0:-1]] = item.tail
#
# print(detail)
# property = [item.text for item in info]
# value = [item.tail for item in info]
#
# mine = dict()
# for key in key_list:
#     if key in property and :
#         mine[key] =


# detail = [zip(item.text, item.tail) for item in info]
# print(detail)

# for item in info:
#     print(item.text)
#     print(item.tail)


# for item in info.findall('div'):
#     print(item.attrib['class'])

# //*[@id="mw-pages"]/div/div/div/ul/li

# //*[@id="mw-pages"]/div/div/div[1]/ul/li[1]/a
# for ul in info:
#     # print(ul)
#     url_body = ul.find('a').attrib['href']
#     if '/Category:Coal_mines_in_' in url_body:
#         print(url_body)


# for ul in info:
#     for li in ul.findall('li'):
#         for a in li.findall('a'):
#             print(a.attrib['href'])
#
# from xml.etree import ElementTree as ET
#
# tree = ET.parse("C:/Users/Cong/PycharmProjects/smx2avl/new.html")
# root = tree.getroot()
#
# for item in root.findall('li'):
#     print(item.find('b').text)
#     print(item.find('b').tail)
#     # print(item.tail)
