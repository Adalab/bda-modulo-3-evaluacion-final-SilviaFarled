# %%
# CONFIGURACIÓN
#=================================

import pandas as pd 
from IPython.display import display # Para .py
import scipy.stats as stats

# Evaluar linealidad de las relaciones entre las variables
# ------------------------------------------------------------------------------
import scipy.stats as stats
from scipy.stats import shapiro, poisson, chisquare, expon, kstest
from scipy.stats import levene, bartlett, shapiro

# Imputación de nulos usando métodos avanzados estadísticos
# -----------------------------------------------------------------------
from sklearn.impute import KNNImputer

# ver todas las columnas
pd.set_option('display.max_columns', None)
# ver todas las filas
pd.set_option('display.max_rows', None)

# %%
# FUNCIONES SIMPLES
#=================================

def open(file_name):
    '''
    Abre un archivo CSV y carga su contenido en un DataFrame, omitiendo líneas con errores
    '''    
    df1 = pd.read_csv(file_name, on_bad_lines='skip')
    return df1

def basic_eda(df):
    '''
    Permite revisar un df para comprobar el contenido 
    y la forma para comenzar la limpieza de datos
    '''

    print('🌷Ejemplo de datos del DF:')
    display(df.head(3))
    display(df.tail(3))
    display(df.sample(3))
    print('________________________________________________________________________________________________________')

    print('🌻Número de Filas:')
    display(df.shape[0])
    print('________________________________________________________________________________________________________')

    print('🌱Número de Columnas:')
    display(df.shape[1])
    print('________________________________________________________________________________________________________')

    print('🌼Información de la tabla:')
    display(df.info())
    print('________________________________________________________________________________________________________')

    print('🌑Nombre de las columnas:')
    display(df.columns)
    print('________________________________________________________________________________________________________')

    print('🍄Descripción de los datos numéricos:')
    display(df.describe().T)
    print('________________________________________________________________________________________________________')

    print('🌋Descripción de los datos no-numéricos:')
    try:
        display(df.describe(include='object').T)
    except:
        pass
    print('________________________________________________________________________________________________________')

    print('🍂Saber si hay datos únicos:')
    display(df.nunique())
    print('________________________________________________________________________________________________________')

    print('🐖Que datos son nulos por columnas:')
    display(df.isnull().sum())
    print('________________________________________________________________________________________________________')

    print('🐲Filas duplicadas:')
    total_duplicados = df.duplicated().sum()
    if total_duplicados > 0:
        print(f'cantidad de duplicados: {total_duplicados}')
        print('Primeros duplicados')
        display(df[df.duplicated()].head(3))
    else:
        print('No hay duplicados')
    print('________________________________________________________________________________________________________')

    print('🪹 Columnas constantes (solo 1 valor único):')
    constantes = df.columns[df.nunique() <= 1]
    if len(constantes) > 0:
        print(f'{len(constantes)} columnas con 1 valor único:')
        display(constantes)
    else:
        print('No hay columnas constantes')
    print('________________________________________________________________________________________________________')
    
    print('🚀 Valores únicos en columnas categóricas:')
    for col in df.select_dtypes(include='object'):
        print(f'🔸 {col}')
        print('-----------------------------')
        print(df[col].unique())
        print('________________________________________________________________________________________________________')

    print('🧬 Tipos de datos por columna:')
    display(df.dtypes.value_counts())
    print('________________________________________________________________________________________________________')
    return



def to_union(df1,df2):
    '''
    Une dos tablas con una columna en común con el mismo nombre
    '''
    df_new = df1.merge(df2, how='right')
    return df_new


def duplicates(df):
    '''
    Comprueba si hay filas duplicadas y, en caso de haberlas
    las elimina
    '''
    if df.duplicated().sum() > 0:
        df= df.drop_duplicates()
        return df
    else:
        return df
    

def change_data(df, column, type):
    '''
    Modifica el tipo de dato de una columna dada al indicado
    '''
    try:
        if type == "int":
            df[column] = df[column].astype(int)
        elif type == "object":
            df[column] = df[column].astype(str)
        elif type == "datetime":
            df[column] = pd.to_datetime(df[column], errors='coerce')
        elif type == "float":
            df[column] = df[column].astype(float)
        else:
            print("Solo se acepta: int, object, datetime o float")
    except:
        print("Hay nulos")
    return


def date_union (df, year_column, month_column, date_column):  
    '''
    Une las columnas de año y mes creando una única de fecha 
    y elimina las originales
    '''
    localizacion = df.columns.get_loc(year_column)
    df.insert(localizacion, date_column, None)
    df[date_column] = df[year_column].astype(str) + "-" + df[month_column].astype(str).str.zfill(2) + "-01"
    df[date_column] = pd.to_datetime(df[date_column])
    df[date_column] = df[date_column].dt.date
    df.drop([year_column, month_column], axis=1, inplace=True)
    return


def multigroup_hypothesis_test(*args):

    """
    Realiza una prueba de hipótesis para comparar grupos.
    1. Primero verifica si los datos son normales usando el test de Shapiro-Wilk o Kolmogorov-Smirnov.
    2. Si los datos son normales, usa Bartlett para probar igualdad de varianzas. Si no son normales, usa Levene.
    3. Si las varianzas son iguales, usa el ANOVA; si no, usa la versión de Kruskal-Wallis.

    Parámetros:
    *args: listas o arrays con los datos de cada grupo. Espera VARIOS grupos a comparar

    Retorna:
    dict con resultados del test de normalidad, varianza e hipótesis.
    """


    if len(args) < 2:
        raise ValueError("Se necesitan al menos dos conjuntos de datos para realizar la prueba.")

    # Test de normalidad por grupo
    normality = []
    for group in args:
        if len(group) > 50:
            p_value_norm = stats.kstest(group, 'norm').pvalue
        else:
            p_value_norm = stats.shapiro(group).pvalue
        normality.append(p_value_norm > 0.05)

    normal_data = all(normality)

    # Test de igualdad de varianzas para todos los grupos juntos
    if normal_data:
        p_variance_value = stats.bartlett(*args).pvalue
    else:
        p_variance_value = stats.levene(*args, center="median").pvalue

    equal_variances = p_variance_value > 0.05

    # Test final según normalidad y varianzas
    if normal_data and equal_variances:
        t_stat, p_value = stats.f_oneway(*args)
        test_used = "ANOVA"
    else:
        t_stat, p_value = stats.kruskal(*args)
        test_used = "Kruskal-Wallis"

    alfa = 0.05

    result = {
        "Test de Normalidad": normality,
        "Datos Normales": normal_data,
        "p-valor Varianza": p_variance_value,
        "Varianzas Iguales": equal_variances,
        "Test Usado": test_used,
        "Estadístico": t_stat,
        "p-valor": p_value,
        "Conclusión": "Rechazamos H0. Hay diferencias significativas entre grupos" if p_value < alfa else "No se rechaza H0. No hay diferencias significativas entre grupos"
    }

    print("\n📊 **Resultados de la Prueba de Hipótesis Multigrupos** 📊")
    print(f"✅ Normalidad en todos los grupos: {'Sí' if normal_data else 'No'}")
    print(f"   - Normalidad por grupo: {normality}")
    print(f"✅ Varianzas: {'Iguales' if equal_variances else 'Desiguales'} (p = {p_variance_value:.4f})")
    print(f"✅ Test aplicado: {test_used}")
    print(f"📉 Estadístico: {t_stat:.4f}, p-valor: {p_value:.4f}")
    print(f"🔍 Conclusión: {result['Conclusión']}\n")
    return


def save (df, name):
    '''
    Guarda un df como csv
    '''
    df.to_csv(name)
    return


# %%
# FUNCIONES COMBINADAS
#=================================

def total_open (file_name1, file_name2):
    '''
    Abre dos archivos CSV y devuelve ambos DataFrames
    '''
    df1 = open(file_name1)
    df2 = open(file_name2)
    return df1, df2


def data_review (df1, df2):
    '''
    Ejecuta la función de análisis de dos DataFrames
    '''
    basic_eda(df1)
    basic_eda(df2)


def first_cleaning_and_union(df1, df2):
    '''
    Limpia duplicados y filas sin vuelos en df1, y une df2 con df1
    '''
    # Eliminamos duplicados
    df1 = duplicates(df1)
    # Eliminamos filas sin información
    df1 = df1[df1["Total Flights"] != 0]
    # Unimos los ficheros
    df3 = to_union(df2, df1)
    # Devolvemos la unión
    return df3

def second_cleaning(df):
    '''
    Limpia y corrige datos de Salary, maneja nulos y tipos en columnas clave,
    y unifica columnas de año y mes en columnas de fecha
    '''
    # Comprobamos que la columna Salary tiene valores negativos. Utilizamos .abs() para sacar el valor absoluto:
    df["Salary"] = df["Salary"].abs()

    # También tiene valores nulos. Elegimos el método KNN para la imputación y facilitamos otras columnas numéricas en las que apoyar la imputación. 
    # Sin embargo, para esta versión .py, para evitar la tardanza en el método KNN, imputamos a la media:
    df['Salary'] = df['Salary'].fillna(df['Salary'].mean())

    # Completamos los nulos de las columnas de mes y año de cancelación a fechas absurdas en el futuro: 
    df["Cancellation Year"] = df["Cancellation Year"].fillna(2262)
    df["Cancellation Month"] = df["Cancellation Month"].fillna(1)

    # Una vez gestionado los nulos, cambiamos el tipo de dato de estas columnas de float a int: 
    columns_int = ["Points Accumulated", "Salary", "Cancellation Year", "Cancellation Month"]

    for column in columns_int: 
        change_data(df, column, "int")
        print(f"Cambiada la columna {column}")

    # Concatenamos las fechas en una sola columna juntando el año, el mes y el día 1. Lo convertimos a datatime y eliminamos las columnas de año y mes iniciales con la función date_union: 
    date_union(df, "Enrollment Year", "Enrollment Month", "Enrollment Date")
    date_union(df, "Cancellation Year", "Cancellation Month", "Cancellation Date")
    date_union(df, "Year", "Month", "Date")
    return df


def bonus_hypothesis_test(df):
    '''
    Prepara grupos por nivel educativo y realiza prueba estadística para comparar vuelos reservados
    '''
    #  Preparación de datos: Generamos un nuevo df con las columnas indicadas: 
    df_bon = df[["Flights Booked", "Education"]]

    # Generamos una variable por cada nivel de educación y mostramos sólo la columna de vuelos reservados: 
    bachelor_group = df_bon[df_bon["Education"] == "Bachelor"]["Flights Booked"]
    college_group = df_bon[df_bon["Education"] == "College"]["Flights Booked"]
    doctor_group = df_bon[df_bon["Education"] == "Doctor"]["Flights Booked"]
    secondary_group = df_bon[df_bon["Education"] == "High School or Below"]["Flights Booked"]
    master_group = df_bon[df_bon["Education"] == "Master"]["Flights Booked"]

    # Prueba estadística: Activamos la función de la prueba de hipótesis adaptada para gestionar con varios grupos:
    multigroup_hypothesis_test(bachelor_group, college_group, doctor_group, secondary_group, master_group)
    return

# %%