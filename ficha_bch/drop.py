import sqlite3

# Conectar a la base de datos
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# Eliminar la tabla
cursor.execute('DROP TABLE IF EXISTS ficha_Registro_materialidad')

# Confirmar los cambios y cerrar la conexión
conn.commit()
conn.close()

print("Tabla eliminada exitosamente.")


