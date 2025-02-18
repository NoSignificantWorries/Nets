from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
driver.get("http://www.wildberries.ru")

user = driver.find_element(By.CLASS_NAME, "navbar-pc__item")
user.click()

