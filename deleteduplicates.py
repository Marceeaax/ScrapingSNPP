import sqlite3

conn = sqlite3.connect('paraguayosprueba2.db')
c = conn.cursor()

c.execute('''SELECT cedula, nombres, apellidos, dia, mes, anho, COUNT(cedula) FROM paraguayos GROUP BY cedula HAVING COUNT(cedula) > 1''')

rows = c.fetchall()

# print the duplicates

print("Duplicados: ")

for row in rows:
    print(row)

print("En total son " + str(len(rows)) + " registros duplicados")

print("Limpiar? (y/n)")

limpiar = input()

if limpiar == "y":

    # delete the duplicates

    c.execute('''DELETE FROM paraguayos WHERE rowid NOT IN (SELECT MIN(rowid) FROM paraguayos GROUP BY cedula)''')

    # commit the changes

    conn.commit()

    # close the connection

    conn.close()

    # print the number of duplicates deleted

    print("Duplicados eliminados: " + str(c.rowcount))

else:
    
        # close the connection
    
        conn.close()
    
        print("No se eliminaron registros")


