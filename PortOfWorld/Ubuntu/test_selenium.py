from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time
from lxml import etree

def test_eight_components():

    #options = ChromeOptions()
    #options = FirefoxOptions()
    #service = Service(executable_path="C:/Users/Cong/PycharmProjects/PortOfWorld/Lib/chromedriver")

    #prefs = {'profile.default_content_setting_values': {'images': 2,'javascript': 2}}
    #options.add_experimental_option("prefs", prefs)

    #driver = webdriver.Chrome(service=service, options=options)
    driver = webdriver.Firefox()
    driver.get("https://google.com")

    # Wait for Goolge Response
    driver.implicitly_wait(5)
    
    xpath = '/html/body/div[2]/div[2]/div[3]/span/div/div/div/div[3]/div[1]/button[2]/div'
    accept_button = driver.find_element(by=By.XPATH, value=xpath)
    accept_button.click()

    # Wait for 1 second
    driver.implicitly_wait(1)
    time.sleep(1)

    english_page = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/a[2]')
    english_page.click()

    time.sleep(1)

    # Identify Search Box
    search_box = driver.find_element(by=By.NAME, value="q")
    #search_button = driver.find_element(by=By.NAME, value="btnG")

    # Enter Search Text and Click Search Button
    search_box.send_keys("Port of Shanghai  Wikipedia")
    #search_button.click()
    search_box.submit()

    html = driver.page_source
    print(html)

    time.sleep(5)

    link = driver.find_element(by=By.XPATH, value='//*[@id="main"]/div[4]/div/div[1]/a/h3')
    link.click()

    time.sleep(100)
    driver.get("https://google.com")

    time.sleep(100)

    driver.close()
    driver.quit()


test_eight_components()

#  //*[@id="sf"]/div/div/input[1]
# //*[@id="qdClwb"]
# time.sleep(0.2)
# # perform Google search with Keys.ENTER
# m.send_keys(Keys.ENTER)

# < input type = "submit" value = "全部接受" class ="basebutton button searchButton" aria-label="全部接受" >

# search_box = browser.find_element(by=By.NAME, value="q")
# search_button = browser.find_element(by=By.NAME, value="btnK")
#
# search_box.send_keys("Selenium")
# search_button.click()
#
# search_box = browser.find_element(by=By.NAME, value="q")
# value = search_box.get_attribute("value")
# assert value == "Selenium"
