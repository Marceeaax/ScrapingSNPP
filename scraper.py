import selenium
import time
import sqlite3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Create a database connection to a SQLite database and a cursor, which is necessary to execute SQL commands
 
conn = sqlite3.connect('paraguayosprueba.db')
c = conn.cursor()

# Create table - only run this once!

c.execute('''CREATE TABLE IF NOT EXISTS paraguayosprueba
                (cedula text, nombres text, apellidos text, dia integer, mes integer, anho integer)''')

# Create a new instance of the Chrome driver

cedula = 4052317

nombreanterior = ""
apellidoanterior = ""
diaanterior = ""
mesanterior = ""
anhoanterior = ""

while True:
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())

        # Go to the website

        search_url = "https://identidad.mtess.gov.py/alumno/register.php"

        driver.get(search_url)

        time.sleep(3)

        elem = driver.find_element(By.NAME, "value_cedula_1")

        missings = []

        while cedula < 4100000:
            while True:
                try: 
                    print("Procesando cedula: " + str(cedula))
                    elem.clear()
                    elem.send_keys(cedula)
                    elem.send_keys(Keys.TAB)

                    time.sleep(3.5)

                    
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
                        
                        # If all the fields are the same as the previous ones, retry:
                        if(nombres == nombreanterior and apellidos == apellidoanterior and dia == diaanterior and mes == mesanterior and anho == anhoanterior):
                            print("Datos repetidos, reintentando...")
                        
                        # If the fields are different, save them and move on:
                        else:
                            nombreanterior = nombres
                            apellidoanterior = apellidos
                            diaanterior = dia
                            mesanterior = mes
                            anhoanterior = anho

                            print("Datos nuevos, guardando...")

                            c.execute("INSERT INTO paraguayosprueba VALUES (?, ?, ?, ?, ?, ?)", (cedula, nombres, apellidos, dia, mes, anho))
                            conn.commit()

                            cedula = cedula + 1

                        time.sleep(2)

                    else:
                        print("No encontrado")
                        missings.append(cedula)
                        # append to a list of not found
                        cedula = cedula + 1

                    break

                except Exception as e:
                    print(e)
                    print("Error, reintentando")
                    time.sleep(2)
                    continue
        break
    except Exception as e:
        print(e)
        print("Error, reintentando")
        time.sleep(2)
        continue



# the list of not found in a file
with open('missings.txt', 'w') as f:
    for item in missings:
        f.write("%s " % item)

print("There are " + str(len(missings)) + " missing")

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()

driver.quit()

#The script is pretty straightforward. It opens the website, enters the cedula, and then grabs the data from the fields. It then inserts the data into a SQLite database.
