import sqlite3

def chequear_cedulas_duplicadas(cursor):
    cursor.execute('SELECT cedula,nombres,apellidos, COUNT(*) FROM paraguayosprueba GROUP BY cedula HAVING COUNT(*) > 1')
    cedulas_duplicadas = cursor.fetchall()
    if cedulas_duplicadas:
        print("Se encontraron cédulas duplicadas:")
        for cedula,nombre,apellido,count in cedulas_duplicadas:
            print(cedula,count)
            print(nombre,apellido)
            print(" ")
    else:
        print("No se encontraron cédulas duplicadas.")

def chequear_nombres_apellidos_duplicados(cursor):
    cursor.execute('SELECT nombres, apellidos, COUNT(*) FROM paraguayosprueba GROUP BY nombres, apellidos HAVING COUNT(DISTINCT cedula) > 1')
    nombres_apellidos_duplicados = cursor.fetchall()
    if nombres_apellidos_duplicados:
        print("\nSe encontraron nombres y apellidos duplicados con cédulas diferentes:")
        for registro in nombres_apellidos_duplicados:
            print(registro)
    else:
        print("\nNo se encontraron nombres y apellidos duplicados con cédulas diferentes.")

def chequear_registros_vacios(cursor):
    cursor.execute('SELECT * FROM paraguayosprueba WHERE cedula IS NULL OR cedula = "" OR nombres IS NULL OR nombres = "" OR apellidos IS NULL OR apellidos = ""')
    registros_vacios = cursor.fetchall()
    if registros_vacios:
        print("\nSe encontraron registros con nombres, apellidos o cédulas vacíos:")
        for registro in registros_vacios:
            print(registro)
    else:
        print("\nNo se encontraron registros con nombres, apellidos o cédulas vacíos.")

def menu():
    print("\n--- Menú ---")
    print("1. Chequear cédulas duplicadas")
    print("2. Chequear nombres y apellidos duplicados")
    print("3. Chequear registros con datos vacíos")
    print("4. Salir")

def main():
    # Conexión a la base de datos
    conn = sqlite3.connect('paraguayosprueba.db')
    c = conn.cursor()

    while True:
        menu()
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            chequear_cedulas_duplicadas(c)
        elif opcion == "2":
            chequear_nombres_apellidos_duplicados(c)
        elif opcion == "3":
            chequear_registros_vacios(c)
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")

    # Cerrar la conexión a la base de datos
    conn.close()

if __name__ == "__main__":
    main()
