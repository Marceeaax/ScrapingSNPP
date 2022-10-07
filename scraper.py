import selenium
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

driver = webdriver.Chrome(ChromeDriverManager().install())

search_url = "https://identidad.mtess.gov.py/alumno/register.php"

driver.get(search_url)

elem = driver.find_element(By.NAME, "value_cedula_1")
elem.clear()
elem.send_keys("4669759")
elem.send_keys(Keys.TAB)

time.sleep(3)

elem2 = driver.find_element(By.ID, "readonly_value_nombre_1")
nombres = elem2.get_attribute("value")

elem3 = driver.find_element(By.ID, "readonly_value_apellido_1")
apellidos = elem3.get_property("value")

elem4 = driver.find_element(By.ID, "dayvalue_fechanac_1")
dia = elem4.get_property("value")

elem5 = driver.find_element(By.ID, "monthvalue_fechanac_1")
mes = elem5.get_property("value")

elem6 = driver.find_element(By.ID, "yearvalue_fechanac_1")
anho = elem6.get_property("value")

time.sleep(3)
