from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import NoSuchElementException
import re
import time
import requests
from lxml import etree
from lxml import html


# --------------------------------------------------- #
def GoogleSearch(list_of_keys, extractfunc=None):

    options = ChromeOptions()
    service = Service(executable_path="C:/Users/Cong/PycharmProjects/PortOfWorld/Lib/chromedriver")

    # Disable Images and JS
    prefs = {'profile.default_content_setting_values': {'images': 2,'javascript': 2}}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://google.com")

    # Wait for Goolge Response
    driver.implicitly_wait(5)
    time.sleep(2)

    try:
        # Accept all cookies
        accept_button = driver.find_element(by=By.XPATH, value="/html/body/div[2]/div[2]/form[2]/input[12]")
        accept_button.click()

        # Wait for 1 seconds
        time.sleep(1)

    except NoSuchElementException:
        pass


    output = list()

    for key in list_of_keys:
        print(key)

        driver.get("https://google.com")

        # Identify Search Box
        search_box = driver.find_element(by=By.NAME, value="q")
        search_button = driver.find_element(by=By.NAME, value="btnG")

        # Enter Search Text and Click Search Button
        search_box.send_keys(key)
        search_button.click()

        time.sleep(0.5)

        # resulst = driver.find_element(By.CSS_SELECTOR, 'div.g')
        # link = results[0].find_element(By.TAG_NAME, 'a')
        # results = driver.find_elements_by_css_selector('div.g')
        # link = results[0].find_element_by_tag_name("a")
        # href = link.get_attribute("href")

        # html_text = driver.page_source
        # html_text = driver.find_element(By.TAG_NAME, 'body')
        # html_text = driver.find_element(By.ID, 'search').text
        # html_text = driver.find_element(By.XPATH, '//*[@id="search"]/div').text

        # print(type(html_text))
        # print(html_text)

        # if extractfunc is None:
        #     output.append(html_text)
        # else:
        #     output.append(extractfunc(html_text))

        # # Click the first result
        # link = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[4]/div/div[1]/a/h3')
        # link.click()

        # click second link
        # for i in range(10):
        #     try:
        #         driver.find_elements(By.XPATH, '//*[@id="rso"]/div[' + str(i) + ']/div/div[2]/div/div/div[1]/a').click()
        #         break
        #     except:
        #         print("------------------------------------------------------")
        #         pass
        #
        # results = driver.find_elements(by=By.XPATH, value='//*[@id="rso"]/div[3]/div/div[1]/div') #''//[@class="yuRUbf"]/a/h3')  # finds webresults
        # print(results)
        # results[0].click()
        # results = driver.find_elements()
        # results = driver.find_elements(By.ID, 'search')
        # results = driver.find_elements(By.TAG_NAME, 'a')
        # # print(results)
        # hrefs = [item.get_attribute('href') for item in results]
        #
        # for href in hrefs:
        #     if re.search(r"en.wikipedia", href):
        #         print(href)
        #
        # soup = BeautifulSoup(driver.page_source, 'lxml')
        # result_div = soup.find_all('div', attrs={'class': 'g'})
        #
        # for res in result_div:
        #     link = res.find('a', href=True)
        #     title = res.find('h3')
        #     print("---",tilte)


    time.sleep(1)

    # Close the browser and quit
    driver.close()
    driver.quit()

    return output

# ----------------------------------------------------------------- #
def GoogleSearch2(list_of_keys):

    options = ChromeOptions()
    service = Service(executable_path="C:/Users/Cong/PycharmProjects/PortOfWorld/Lib/chromedriver")

    driver = webdriver.Chrome(service=service, options=options)

    driver.get("https://google.com")

    # Wait for Goolge Response
    driver.implicitly_wait(5)
    time.sleep(2)

    try:
        # Languag Selection //*[@id="vc3jof"]
        language_selet = driver.find_element(by=By.XPATH, value='//*[@id="vc3jof"]')
        language_selet.click()

        # Select the English Page /li[contains(text(),"English")]
        english_page = driver.find_element(by=By.XPATH, value='//li[contains(text(),"English")]')
        english_page.click()

    except NoSuchElementException:
        pass

    try:
        # Accept all cookies //*[@id="L2AGLb"]
        accept_button = driver.find_element(by=By.XPATH, value='//*[@id="L2AGLb"]')
        accept_button.click()

    except NoSuchElementException:
        pass

    # Wait for seconds
    time.sleep(2)

    try:
        # Go to English page  "//a[text()='English']"
        english_page = driver.find_element(by=By.XPATH, value='//a[text()="English"]')
        english_page.click()

    except NoSuchElementException:
        pass

    # Wait for seconds
    time.sleep(2)

    output = list()

    for key in list_of_keys:

        try:
            # Visit google.com
            driver.get("https://google.com")

            # Identify Search Box
            search_box = driver.find_element(by=By.NAME, value="q")
            # search_button = driver.find_element(by=By.NAME, value="btnK")  # exising two 'btnK', not used

            # Enter Search Text and Sumbit / Click Search Button
            search_box.send_keys(key)
            search_box.submit()
            # search_button.click()     # unable to click, not used

            time.sleep(5)

            try:
                search_results = driver.find_elements(by=By.CLASS_NAME, value="yuRUbf")
                hrefs = [result.find_element(by=By.TAG_NAME,value="a").get_attribute('href') for result in search_results]

            except:
                print(f"***** Error when searching href for {key} *****")
                output.append(None)
                continue

            print(hrefs, ',')
            output.append(hrefs)

        except:
            print(f"???????????????????? Error When Accessing Google Searching for {key} ??????????????????")
            output.append(None)
            continue

    # Close the browser and quit
    driver.close()
    driver.quit()

    return output




# ----------------------------------------------------------------- #
def ExtractWikiLinkFromGoogleSearch(list_of_hrefs):
    for href in list_of_hrefs:
        if href is None:
            continue
        if re.search(r"en\.wikipedia.org/wiki/.*port", href, re.I) is not None:
            print(href)
            return href
        else:
            continue




    # # reg = r"\"(https://en\.wikipedia\.org/wiki/[\S]*)\""
    # pattern = re.compile(r'ref=\"(https://en\.wikipedia\.org/wiki/[\S]*)\"', re.M)
    # url = pattern.findall(page_source)
    # #
    # print(url, ",")
    # return url

    # web_html = html.fromstring(page_source)
    # # web_html = etree.HTML(page_source)
    # # print(web_html)
    # urls = web_html.xpath('//a/@href')
    #
    # print('\n'.join(urls))


    # print(web_html.xpath('normalize-space(//*[@id="search"]/div[1]/div[1])'))
    # data = self.driver.page_source
    # doc = lxml.html.fromstring(data)
    # target = doc.xpath('some xpath')


# GoogleSearch2(['Port of Durres (Durazzo) wikipedia'], ExtractWikiLinkFromGoogleSearch)

# hrefs = ['https://en.wikipedia.org/wiki/Durr%C3%ABs', 'https://en.wikipedia.org/wiki/Port_of_Durr%C3%ABs', 'https://nl.wikipedia.org/wiki/Durr%C3%ABs_(stad)', 'https://zh.m.wikipedia.org/zh-hans/%E9%83%BD%E6%8B%89%E6%96%AF', 'https://zh.wikipedia.org/zh-hans/%E9%83%BD%E6%8B%89%E6%96%AF', 'https://zh.wikipedia.org/zh/File:Panorama_of_Durres_Port.jpg', 'https://vi.wikipedia.org/wiki/Durr%C3%ABs', 'https://zh.wikipedia.org/zh-mo/%E9%83%BD%E6%8B%89%E6%96%AF', 'https://ro.wikipedia.org/wiki/Durr%C3%ABs', 'https://en.wikipedia.org/wiki/Durr%C3%ABs_County']

# ExtractWikiLinkFromGoogleSearch(hrefs)

# print(re.search(r"en\.wikipedia.org/wiki/.*port", hrefs[1], re.I))



# print(ExtractWikiLinkFromPage(string))

# print(ExtractWikiLinkFromPage('href="https://en.wikipedia.org/wiki/Port_of_Shanghai" data-ved="2ahUKEwjK-cPtwd74AhXDAewKHXaxAYMQFnoECAgQAQ" ping="/url?sa=t&'))
#
#
# def GoogleSearch(search_url, target):
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0(Macintosh; Intel Mac OS X 10_11_4)\
#         AppleWebKit/537.36(KHTML, like Gecko) Chrome/52 .0.2743. 116 Safari/537.36'}
#
#     try:
#         web_req = requests.get(search_url, headers=headers)
#     except requests.exceptions.RequestException:
#         print('# -------------- WEB ACCESS FAILED --------------- #')
#         return None
#
#     if web_req.status_code == 200:
#         print(web_req.content)
#     else:
#         print(f"STATUS CODE {web_req.status_code}")
#
#     # print(web_text)
#     web_html = etree.HTML(web_req.text)
#     # web_html = etree.HTML(web_text)
#
#     print(web_html)
#     return None
#
# GoogleSearch('https://www.google.com/search?q=port+shanghai+wikipedia', 'wiki')
#
# # -------------------------------------------------------------------- #