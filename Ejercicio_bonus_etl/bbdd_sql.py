# %%

# CONFIGURACIÓN
#=================================

import pandas as pd
import pymysql
from sqlalchemy import create_engine

# Configuración de la base de datos
host = '127.0.0.1'
user = 'root'
password = 'AlumnaAdalab'
database = 'customer_data'


# %%

# FUNCIONES SIMPLES
#=================================

def create_db():
    '''
    Crea una base de datos en MySQL si no existe
    '''
    # Conectar a MySQL usando pymysql
    connection = pymysql.connect(
                host=host,
                user=user,
                password=password
                )

    # Crear un cursor
    cursor = connection.cursor()

    # Crear una base de datos si no existe
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    print("Base de Datos creada exitosamente.")

    # Cerrar la conexión
    connection.close()
    return


def load_data(table_name, data):
    '''
    Carga un DataFrame en una tabla MySQL usando SQLAlchemy
    '''

    print(f"Cargando datos en la tabla {table_name}...")

    # Crear conexión a MySQL usando SQLAlchemy
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

    # Insertar datos desde el DataFrame en MySQL
    data.to_sql(table_name, con=engine, if_exists='append', index=False)
    print(f"Datos insertados en la tabla {table_name} exitosamente.")
    return

# %%

# FUNCIÓN COMBINADA
#=================================

def data_upload(table_name, data):
    '''
    Crea la base de datos y carga los datos en la tabla especificada
    '''
    create_db()
    load_data(table_name, data)
    return

# %%