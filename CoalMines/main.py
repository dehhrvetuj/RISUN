# ------------------------------------------------ #
url_parent = 'https://www.gem.wiki'
url_ini = 'https://www.gem.wiki/Category:Global_Coal_Mine_Tracker'

from utilities import GetHTMLElementList


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


# ------------------ Get URL for Each Country --------------------- #
xpath = '//*[@id="mw-subcategories"]/div/div/div[1]/ul/li'

info = GetHTMLElementList(url_ini, xpath)
info = [ul for ul in info if '/Category:Coal_mines_in_' in ul.find('a').attrib['href']]

name_all_country = [ul.find('a').text.split('Coal mines in')[-1].strip() for ul in info]
url_all_country = [url_parent + ul.find('a').attrib['href'] for ul in info]

coal_mines_all_country = list()

for name_country, url_country in zip(name_all_country, url_all_country):
    country = dict()
    country['Country_Name'] = name_country
    country['Country_url'] = url_country
    coal_mines_all_country.append(country)


# ------------------ Search URL by Country --------------------- #
for mine_country in coal_mines_all_country:

    info = SearchByCountry(mine_country['Country_url'])

    print(mine_country['Country_Name'], len(info))

    country_name = mine_country['Country_Name']
    mine_country['Mines'] = [{'name': item.attrib['title'], 'url': url_parent + item.attrib['href'],
                              'country': country_name} for item in info]


# ------------------------ Search URL of Each Coal Mine ------------------------ #
mines_global = [mine for mine_country in coal_mines_all_country for mine in mine_country['Mines']]

print('Num of global mines:', len(mines_global))

# ----------------- Excluding China ----------------------- #
mines_global = [mine for mine in mines_global if mine['country'] != 'China']


for mine in mines_global:
    xpath = '//*[@id="mw-content-text"]/div/ul[1]/li/b'
    info = GetHTMLElementList(mine['url'], xpath)
    for item in info:
        if item.text is not None:
            key = item.text.replace(':','').strip()
            if item.tail is not None:
                mine[key] = item.tail.replace(':','').strip()
            else:
                mine[key] = None
        else:
            pass
    print(mine)
