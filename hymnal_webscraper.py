from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import string

driver = webdriver.Chrome()
driver.maximize_window()

driver.get('https://www.churchofjesuschrist.org/study/manual/hymns/the-morning-breaks?lang=eng')
count = 0

while count < 342:
	time.sleep(1)
	wfilename = driver.find_element_by_id("title1")
	ufilename = (wfilename.text)
	filename = ufilename.translate(str.maketrans('', '', string.punctuation))
	file = filename + ".txt"
	f = open(file, "w")
	if len(driver.find_elements(By.CLASS_NAME, 'poetry')) > 0:
		wlyrics = driver.find_element(By.CLASS_NAME, 'poetry')
		lyrics = (wlyrics.text)
		f.write(lyrics)
	f.close()	
	count += 1
	turn = driver.find_element_by_xpath('//*[@id="app"]/div/main/div/div[2]/span[2]/a').click()