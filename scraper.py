import selenium
import time
import clipboard
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

driver = webdriver.Chrome(ChromeDriverManager().install())

search_url = "https://identidad.mtess.gov.py/alumno/register.php"

driver.get(search_url)

elem = driver.find_element(By.NAME, "value_cedula_1")
elem.clear()
elem.send_keys("4669759")
elem.send_keys(Keys.TAB)

time.sleep(3)

elem2 = driver.find_element(By.ID, "readonly_value_nombre_1")

#This is added because you need to click before you can copy the text from the element
webdriver.ActionChains(driver).click(elem2).perform()

#This is the line that copies the text to the clipboard
webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").perform()
webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("c").perform()
nombres = clipboard.paste()

elem3 = driver.find_element(By.ID, "readonly_value_apellido_1")
webdriver.ActionChains(driver).click(elem3).perform()
webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("a").perform()
webdriver.ActionChains(driver).key_down(Keys.CONTROL).send_keys("c").perform()
apellidos = clipboard.paste()

elem4 = driver.find_element(By.ID, "dayvalue_fechanac_1")
dia = elem4.get_property("value")

elem5 = driver.find_element(By.ID, "monthvalue_fechanac_1")
mes = elem5.get_property("value")

elem6 = driver.find_element(By.ID, "yearvalue_fechanac_1")
anho = elem6.get_property("value")

