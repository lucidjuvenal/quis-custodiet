# -*- coding: utf-8 -*-


import os
import codecs
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from PIL import Image
import numpy as np




"""
Goal here is to automatically scrape the official government website for the results.
we'd like to compare to previous elections, etc.

Currently have it to the point where running :
	cycle_provincia(driver)

will cycle all province/canton combinations.  And separately, I've made some 
progress on grabbing the captcha, but I can't yet grab it and send it to a bypass service.





<div id="captchaResultados" class="g-recaptcha" data-sitekey="6LfsvhUUAAAAAGUUILj726oSefrhdeHFXdeQyAF4">

<div style="width: 304px; height: 78px;"><div><iframe src="./Resultados 2017_files/anchor.html" title="recaptcha widget" width="304" height="78" frameborder="0" scrolling="no" name="undefined"></iframe></div>

<textarea id="g-recaptcha-response-6" name="g-recaptcha-response" class="g-recaptcha-response" style="width: 250px; height: 40px; border: 1px solid #c1c1c1; margin: 10px 25px; padding: 0px; resize: none;  display: none; ">		</textarea>
</div></div>

id="comboPro"
comboCanton
comboParro

GUAYAS;DAULE;LA AURORA


CheckBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID ,"recaptcha-anchor"))
        )
CheckBox.click()


"""

resultsPage = "https://resultados2017.cne.gob.ec/frmResultados.aspx" 


def init_driver():
	driver = webdriver.Firefox()
	driver.wait = WebDriverWait(driver, 2)
	return driver
 

# opts = driver.find_elements_by_tag_name('option')

def cycle_cantons(driver):
	combCanton = driver.find_element_by_name('comboCanton')
	optsCanton = combCanton.find_elements_by_tag_name('option')
	print("opts length :", len(optsCanton))

	# build list of 
	cantons = list()
	for opt in optsCanton:
		canton = opt.text
		if canton != "Todos":
			cantons.append(canton)

	# select each canton in turn
	for canton in cantons:
		print(canton)
		combCanton = driver.find_element_by_name('comboCanton')
		optsCanton = combCanton.find_elements_by_tag_name('option')
		for opt in optsCanton:
			if opt.text == canton:
				opt.click()
				time.sleep(2)		# Do something here (like looping parroquias, etc)
				break				# break out of loop to start looking for next 
	


def cycle_provincia(driver):
	combPro = driver.find_element_by_name('comboPro')
	optsPro = combPro.find_elements_by_tag_name('option')
	print("opts length :", len(optsPro))

	# build list of provinces
	provinces = list()
	for opt in optsPro:
		province = opt.text
		if province != "Todas":
			provinces.append(province)

	# select each province in turn
	for province in provinces:
		print(province)
		combPro = driver.find_element_by_name('comboPro')
		optsPro = combPro.find_elements_by_tag_name('option')
		for opt in optsPro:
			if opt.text == province:
				opt.click()
				cycle_cantons(driver)  # loop over cantons
				break				# break out of loop to start looking for next province



def click_captcha(driver)
	""" click captcha field to display.  Need to be able to grab it for sending
	to bypass service.  See these:

	http://scraping.pro/recaptcha-solve-selenium-python/

	https://www.captchasolutions.com/community/index.php?u=/topic/5/google-s-no-captcha-captcha-solutions-api-implementation-guide

	http://www.imagetyperz.com/Forms/bypass_Google_captcha_api.aspx
	"""
	CheckBox = WebDriverWait(driver, 10).until(
	        EC.presence_of_element_located((By.ID ,"recaptcha-anchor"))
	        )
	time.sleep( 1 + np.random.uniform(2))
	CheckBox.click()





if __name__ == "__main__":
	driver = init_driver()
	driver.get(resultsPage)
