from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions
import re
import time
import requests
from lxml import etree
from lxml import html


# ----------------------------------------------------------------- #
def GoogleSearch2(list_of_keys):

	# ~ options = ChromeOptions()
	# ~ service = Service(executable_path="C:/Users/Cong/PycharmProjects/PortOfWorld/Lib/chromedriver")

	# ~ driver = webdriver.Chrome(service=service, options=options)
	driver = webdriver.Firefox()
	driver.get("https://google.com")

	# Wait for Goolge Response
	driver.implicitly_wait(5)
	time.sleep(2)

	# Accept all cookies //*[@id="L2AGLb"]
	accept_button = driver.find_element(by=By.XPATH, value='//*[@id="L2AGLb"]')
	accept_button.click()

	# Wait for 1 seconds
	time.sleep(2)

	# Go to English page
	english_page = driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[4]/div/div/a[2]')
	english_page.click()

	# Wait for 1 seconds
	time.sleep(2)

	output = list()

	for key in list_of_keys:
		
		try:
			driver.get("https://google.com")
			
			# Wait for Google.com 
			time.sleep(2)

			# Identify Search Box
			search_box = driver.find_element(by=By.NAME, value="q")
			# search_button = driver.find_element(by=By.NAME, value="btnK")  # exising two 'btnK', not used

			# Enter Search Text and Sumbit / Click Search Button
			search_box.send_keys(key)
			search_box.submit()
			# search_button.click()     # unable to click, not used
			
			# Wait for Google Search Results
			time.sleep(10)

			try:
				search_results = driver.find_elements(by=By.CLASS_NAME, value="yuRUbf")
				hrefs = [result.find_element(by=By.TAG_NAME,value="a").get_attribute('href') for result in search_results]

			except:
				print(f"*****Error when searching href for {key} *****")
				output.append(None)
				continue
				
			print(hrefs,',')
			output.append(hrefs)		
					
		except:
			print(f"???????????????????? Error When Accessing Google Searching for {key} ??????????????????")
			output.append(None)
			continue


	# Close the browser and quit
	driver.close()
	driver.quit()

	return output

