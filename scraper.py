import concurrent.futures
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions  # Importación corregida


def create_database_connection(db_name='paraguayosprueba.db'):
    """Create a database connection and return the connection and cursor."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    return conn, c

def create_table(c):
    """Create the database table if it doesn't exist."""
    c.execute('''CREATE TABLE IF NOT EXISTS paraguayosprueba
                 (cedula text, nombres text, apellidos text, dia integer, mes integer, anho integer)''')
    c.connection.commit()

def setup_webdriver():
    """Setup and return a Chrome WebDriver."""
    # Note: Make sure ChromeDriver is in your PATH or use ChromeDriverManager to manage this automatically
    options = ChromeOptions()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options) # si se quiere desactivar el headless mode solo hay que borrar el argumento de Chrome
    return driver

def open_website(driver):
    """Open the target website with the given WebDriver."""
    search_url = "https://identidad.mtess.gov.py/alumno/register.php"
    driver.get(search_url)
    time.sleep(3)

def fetch_data(driver, cedula):
    """Fetch data from the website for a given cedula and return the data."""
    try:
        elem = driver.find_element(By.NAME, "value_cedula_1")
        elem.clear()
        elem.send_keys(cedula)
        elem.send_keys(Keys.TAB)
        time.sleep(3.5)

        nombres_elem = driver.find_element(By.ID, "readonly_value_nombre_1")
        nombres = nombres_elem.get_attribute("value")

        if nombres != "noencontrada":
            apellidos = driver.find_element(By.ID, "readonly_value_apellido_1").get_property("value")
            dia = driver.find_element(By.ID, "dayvalue_fechanac_1").get_property("value")
            mes = driver.find_element(By.ID, "monthvalue_fechanac_1").get_property("value")
            anho = driver.find_element(By.ID, "yearvalue_fechanac_1").get_property("value")
            return cedula, nombres, apellidos, dia, mes, anho
    except Exception as e:
        print(f"Error fetching data for cedula {cedula}: {e}")
    return None

def process_range(start_cedula, end_cedula):
    """Process a range of cedulas, fetching data and saving to the database."""
    print(f"Processing cedulas from {start_cedula} to {end_cedula}")
    conn, c = create_database_connection()
    create_table(c)
    driver = setup_webdriver()
    open_website(driver)
    missings = []

    for cedula in range(start_cedula, end_cedula + 1):
        data = fetch_data(driver, cedula)
        if data:
            save_data(c, conn, data)
        else:
            missings.append(cedula)

    driver.quit()
    conn.close()
    return missings

def generate_ranges(start, end, parts):
    total_range = end - start + 1
    if total_range % parts != 0:
        raise ValueError("El rango total debe ser divisible por el número de partes")

    step = total_range // parts
    ranges = [(start + i * step, start + (i + 1) * step - 1) for i in range(parts)]
    return ranges

def save_data(c, conn, data):
    """Save the fetched data into the database."""
    c.execute("INSERT INTO paraguayosprueba VALUES (?, ?, ?, ?, ?, ?)", data)
    print(f"insertado {data[0]}")
    conn.commit()

def main():
    start_cedula = 4016000
    end_cedula = 4016999
    total_range = end_cedula - start_cedula + 1  # 100000 en tu ejemplo
    parts = 25  # Este valor puede ser ajustado. Debe ser un divisor de total_range

    # Asegúrate de que 'parts' sea divisor de 'total_range'
    if total_range % parts != 0:
        raise ValueError("El número de partes debe ser divisor del rango total de cédulas")

    ranges = generate_ranges(start_cedula, end_cedula, parts)

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_range, start, end) for start, end in ranges]

        for future in concurrent.futures.as_completed(futures):
            missings = future.result()
            with open('missings.txt', 'a') as f:
                for missing in missings:
                    f.write(f"{missing}\n")

if __name__ == "__main__":
    main()
