import graphics as g
import functions as f
import bbdd_sql as sql

# REVISIÓN

# Abrimos archivos
df_flight, df_loyalty = f.total_open("Customer Flight Activity.csv", "Customer Loyalty History.csv")

# Pasamos una función de análisis a los dataframes
f.data_review(df_flight, df_loyalty)

# LIMPIEZA, REVISIÓN Y UNIÓN

# Eliminamos duplicados, filas sobrantes y unimos los ficheros
df = f.first_cleaning_and_union(df_flight, df_loyalty)

# Pasamos de nuevo la función de análisis por el resultado de la unión para tomar decisiones
f.basic_eda(df)

# Vemos los gráficos de las variables numéricas para decidir la imputación de los datos
g.graph_review(df)

# Gestionamos nulos y concatenamos fechas
df = f.second_cleaning(df) 

# Guardamos el df en un nuevo csv
f.save(df, "Customer_union_py.csv")

# VISUALIZACIÓN

# Ejecutamos los gráficos con las consultas y respuestas del ejercicio. 
g.activate_graphics(df)

# BOUNUS: Prueba de hipótesis

# Ejecutamos la función de la prueba de hipótesis para grupos
f.bonus_hypothesis_test(df)

# CARGA DE DATOS: 

# Creamos la base de datos en SQL y cargamos la tabla
sql.data_upload("customers", df)