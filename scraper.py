import concurrent.futures
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Funciones relacionadas con la base de datos
def create_database_connection(db_name='paraguayosprueba.db'):
    """Crea una conexión a la base de datos y devuelve el objeto conexión y cursor."""
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    return conn, c

def create_table(c):
    """Crea la tabla en la base de datos si no existe ya."""
    c.execute('''CREATE TABLE IF NOT EXISTS paraguayosprueba
                 (cedula text, nombres text, apellidos text, dia integer, mes integer, anho integer)''')
    c.connection.commit()

def save_data(c, conn, data):
    """Guarda los datos obtenidos en la base de datos."""
    c.execute("INSERT INTO paraguayosprueba VALUES (?, ?, ?, ?, ?, ?)", data)
    print(f"Insertado {data[0]}")
    conn.commit()

def fetch_existing_data(c, cedula):
    """Obtiene los datos de la base de datos para una cédula dada."""
    c.execute("SELECT * FROM paraguayosprueba WHERE cedula = ?", (cedula,))
    return c.fetchone()

# Funciones relacionadas con WebDriver
def setup_webdriver():
    """Configura y devuelve un Chrome WebDriver en modo headless."""
    options = ChromeOptions()
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    return driver

def open_website(driver):
    """Abre el sitio web objetivo utilizando el WebDriver dado."""
    search_url = "https://identidad.mtess.gov.py/alumno/register.php"
    driver.get(search_url)
    time.sleep(3)

def send_keys_slowly(element, text, delay=1):
    """Envía las teclas al elemento lentamente con un retardo entre cada tecla."""
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def fetch_data(driver, cedula):
    """Obtiene los datos del sitio web para un número de cédula dado y devuelve los datos."""
    try:
        elem = driver.find_element(By.NAME, "value_cedula_1")
        elem.clear()
        send_keys_slowly(elem, str(cedula))  # Convertir cedula en cadena de caracteres
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
        print(f"Error obteniendo datos para la cédula {cedula}: {e}")
    return None

# Funciones de procesamiento
def process_range(start_cedula, end_cedula):
    """Procesa un rango de cédulas, obteniendo datos y guardándolos en la base de datos."""
    print(f"Procesando cédulas desde {start_cedula} hasta {end_cedula}")
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

def compare_and_report_changes(start_cedula, end_cedula):
    """Vuelve a verificar un rango de cédulas, comparando los valores extraídos con los datos almacenados."""
    print(f"Comparando datos para cédulas desde {start_cedula} hasta {end_cedula}")
    conn, c = create_database_connection()
    driver = setup_webdriver()
    open_website(driver)
    changes = []

    for cedula in range(start_cedula, end_cedula + 1):
        data = fetch_data(driver, cedula)
        if data:
            existing_data = fetch_existing_data(c, cedula)
            if existing_data and data != existing_data:
                changes.append((existing_data, data))

    driver.quit()
    conn.close()

    # Reportar cambios
    with open('changes_detected.txt', 'w') as f:
        for old_data, new_data in changes:
            if old_data != new_data:  # Verificar si hay diferencias
                f.write(f"Diferencias para la cédula {old_data[0]}:\n")
                f.write(f"Anterior: {old_data}\n")
                f.write(f"Nuevo: {new_data}\n\n")

def generate_ranges(start, end, parts):
    """Genera una lista de rangos divididos en partes iguales entre un rango inicial y final."""
    total_range = end - start + 1
    if total_range % parts != 0:
        raise ValueError("El rango total debe ser divisible por el número de partes")

    step = total_range // parts
    return [(start + i * step, start + (i + 1) * step - 1) for i in range(parts)]

# Función principal
def main():
    start_cedula = 5000000
    end_cedula = 5000999
    total_range = end_cedula - start_cedula + 1
    parts = 10

    if total_range % parts != 0:
        raise ValueError("El número de partes debe ser divisor del rango total de cédulas")

    ranges = generate_ranges(start_cedula, end_cedula, parts)

    # Primer paso: recopilación inicial
    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(process_range, start, end) for start, end in ranges]

        # Recopila las cédulas que no pudieron ser encontradas
        for future in concurrent.futures.as_completed(futures):
            missings = future.result()
            with open('missings.txt', 'a') as f:
                for missing in missings:
                    f.write(f"{missing}\n")

    # Segundo paso: comparación de datos
    compare_and_report_changes(start_cedula, end_cedula)

if __name__ == "__main__":
    main()
