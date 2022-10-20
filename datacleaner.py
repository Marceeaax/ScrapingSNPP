# This is a python script that removes duplicates and corrects data

import time
import selenium
import sqlite3
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

conn = sqlite3.connect('paraguayosprueba2.db')
c = conn.cursor()

# select all rows where only cedula is distinct and order by nombres, nombres, apellidos, dia, mes, anho are the same

c.execute("""SELECT DISTINCT A.cedula, A.nombres, A.apellidos, A.dia, A.mes, A.anho
FROM paraguayos A, paraguayos B
WHERE A.cedula <> B.cedula
AND A.nombres = B.nombres
AND A.apellidos = B.apellidos
AND A.dia = B.dia
AND A.mes = B.mes
AND A.anho = B.anho
ORDER BY A.nombres, A.apellidos, A.dia, A.mes, A.anho""")

# create a list of tuples with the results

rows = c.fetchall()

cedula = 0

print("Existen " + str(len(rows)) + " registros duplicados")

print("Limpiar? (y/n)")

limpiar = input()

if limpiar == "y":
    while True:
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install())

            # Go to the website

            search_url = "https://identidad.mtess.gov.py/alumno/register.php"

            driver.get(search_url)

            time.sleep(3)

            elem = driver.find_element(By.NAME, "value_cedula_1")

            while cedula < len(rows):
                while True:
                    try: 
                        print("Procesando cedula: " + str(rows[cedula][0]))
                        elem.clear()
                        elem.send_keys(rows[cedula][0])
                        elem.send_keys(Keys.TAB)

                        time.sleep(3)

                        elem2 = driver.find_element(By.ID, "readonly_value_nombre_1")
                        nombres = elem2.get_attribute("value")

                        if(nombres != "noencontrada"):
                            elem3 = driver.find_element(By.ID, "readonly_value_apellido_1")
                            apellidos = elem3.get_attribute("value")

                            elem4 = driver.find_element(By.ID, "dayvalue_fechanac_1")
                            dia = elem4.get_attribute("value")

                            elem5 = driver.find_element(By.ID, "monthvalue_fechanac_1")
                            mes = elem5.get_attribute("value")

                            elem6 = driver.find_element(By.ID, "yearvalue_fechanac_1")
                            anho = elem6.get_attribute("value")

                            if(nombres != rows[cedula][1] or apellidos != str(rows[cedula][2]) or dia != str(rows[cedula][3]) or mes != str(rows[cedula][4]) or anho != str(rows[cedula][5])):
                                print("SE ENCONTRARON diferencias en la cedula: " + str(rows[cedula][0]))
                                print("Datos de la web: " + nombres + " | " + apellidos + " | " + dia + " | " + mes + " | " + anho)
                                print("Datos en la database: " + str(rows[cedula][1]) + " | " + str(rows[cedula][2]) + " | " + str(rows[cedula][3]) + " | " + str(rows[cedula][4]) + " | " + str(rows[cedula][5]))
                                print("")

                                # update the row with the new data

                                c.execute("UPDATE paraguayos SET nombres = ?, apellidos = ?, dia = ?, mes = ?, anho = ? WHERE cedula = ?", (nombres, apellidos, dia, mes, anho, rows[cedula][0]))

                                conn.commit()
                            else:
                                print("No se encontraron diferencias en la cedula: " + str(rows[cedula][0]))
                                print("Datos de la web: " + nombres + " | " + apellidos + " | " + dia + " | " + mes + " | " + anho)
                                print("Datos en la database: " + str(rows[cedula][1]) + " | " + str(rows[cedula][2]) + " | " + str(rows[cedula][3]) + " | " + str(rows[cedula][4]) + " | " + str(rows[cedula][5]))
                                print("")
                            cedula = cedula + 1
                            break
                        else:
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

    driver.close()

    conn.close()

else:
    print("No se limpiaron los registros")
    













