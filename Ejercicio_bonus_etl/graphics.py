# %%
# CONFIGURACIÓN
#=================================

import pandas as pd 
import numpy as np

# Librerías de visualización
# -----------------------------------------------------------------------
import seaborn as sns
import matplotlib.pyplot as plt

# Gestión de los warnings
# -----------------------------------------------------------------------
import warnings
warnings.filterwarnings("ignore") # Para evitar errores en el uso de palette en seaborn

pastel_colors = [
    "#A8DADC",  # Verde azulado pastel (frío)
    "#FFE5B4",  # Amarillo pastel (cálido)
    "#F1C0E8",  # Lila suave (frío)
    "#FFD6D6",  # Rosa melocotón muy suave (cálido)
    "#B5EAEA",  # Turquesa pastel (frío)
    "#FFCBC1",  # Salmón pastel (cálido)
    "#C1E1C1",  # Verde menta claro (frío)
    "#FFE3E3",  # Rosa claro (cálido)
    "#D4A5A5",  # Marrón claro pastel (cálido)
    "#C6D8D3",  # Verde grisáceo pastel (frío)
    "#F7E6C4",  # Beige claro (cálido)
    "#B9AEDC",  # Lavanda pastel (frío)
]

# Configuración valores por defecto:

plt.rcParams.update({
    'font.family': 'Comic Sans MS',
    'axes.titlesize': 18,
    'axes.titleweight': 'bold',
    'axes.labelsize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'figure.facecolor' : 'lightgray',
    'axes.facecolor': 'darkgray'

})

# %%
# GRÁFICOS
#=================================


def graph_review (df):
    # Generamos histogramas para valorar las columnas numéricas
    df.select_dtypes(include=[np.number]).hist(figsize=(16,12), bins=30, color = "black")
    plt.tight_layout()
    plt.show()
    return


def graph_1 (df):
    '''
    Gráfico para ejercicio 1
    ¿Cómo se distribuye la cantidad de vuelos reservados por mes durante el año?
    '''
    df_booking = df.groupby("Date")["Flights Booked"].sum()
    df_booking.index = pd.to_datetime(df_booking.index)
    formatted_dates = df_booking.index.strftime("%B %Y")  # Da formato a la columna para mostrar mes en letra

    plt.figure(figsize=(12, 6))
    plt.bar(x=formatted_dates, height=df_booking.values, color=pastel_colors, edgecolor='black')

    plt.xlabel('Meses')
    plt.ylabel('Vuelos Reservados')
    plt.title('Vuelos Reservados por Mes', fontsize=22)
    plt.xticks(rotation=45)
    ticks_y = np.arange(0, 110000, 10000)
    plt.yticks(ticks_y)
    plt.grid(True, axis='y', color='#eeeeee')
    plt.gca().spines[['right', "top"]].set_visible(False) # quitamos la línea de arriba y de la derecha
    plt.axvline(x=12 - 0.5, color='gray', linestyle='--', linewidth=1)
    plt.tight_layout()
    plt.show()
    return

def graph_2(df):
    '''
    Gráfico para ejercicio 2
    ¿Existe una relación entre la distancia de los vuelos y los puntos acumulados por los cliente?
    '''
    fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize = (20, 5))

    sns.regplot(x = "Distance", 
                y = "Points Accumulated", 
                data = df, 
                marker = "d", 
                line_kws = {"color": "black", "linewidth": 1}, # cambiamos el color y el grosor de la linea de tendencia
                scatter_kws = {"color": "crimson", "s": 2}, # cambiamos el color y el tamaño de los puntos del scaterplot
                ax = axes[0])
    axes[0].set_xlabel("Distancia")
    axes[0].set_ylabel("Puntos Acumulados")
    axes[0].set_title("Relación distancia recorrida y puntos acumulados")
    axes[0].spines[['top', 'right']].set_visible(False)

    df_corr = df[["Distance", "Points Accumulated"]].corr( method = "spearman").round(2)
    df_corr.index = ['Distancia', 'Puntos']
    df_corr.columns = ['Distancia', 'Puntos']
    sns.heatmap(df_corr, 
                cmap='coolwarm', 
                annot=True, 
                fmt='.2f', 
                linewidths=0.5, 
                vmin=-1, 
                vmax=1, 
                ax = axes[1])
    axes[1].set_title("Matriz de Correlación de distancia recorrida y puntos acumulados", fontsize=14) 
    plt.show() 
    return


def graph_3 (df):
    '''
    Gráfico para ejercicio 3
    ¿Cuál es la distribución de los clientes por provincia o estado?
    '''
    plt.figure(figsize=(8, 4))

    sns.countplot(data=df, 
                x="Province", 
                order=df["Province"].value_counts().index, 
                palette=pastel_colors, 
                edgecolor='black', 
                width=0.6)
    plt.title('Distribución de clientes por provincia')
    plt.xticks(rotation=45)
    plt.xlabel('Provincias')
    plt.ylabel('Número de clientes')
    plt.grid(True, axis='y', color='#eeeeee')
    plt.gca().spines[['right', "top"]].set_visible(False) # quitamos la línea de arriba y de la derecha
    plt.show()
    return


def graph_4(df):
    '''
    Gráfico para ejercicio 4
    ¿Cómo se compara el salario promedio entre los diferentes niveles educativos de los clientes?
    '''
    plt.figure(figsize=(8, 4))

    df_salary = df.groupby("Education")["Salary"].mean()
    order_education = ['High School or Below', 'College', 'Bachelor', 'Master', 'Doctor']
    df_salary = df_salary.reindex(order_education)
    df_salary.index = ['Secundaria', 'Técnica', 'Grado', 'Máster', 'Doctorado']

    df_salary.plot(kind='bar', color = pastel_colors, edgecolor='black', width=0.4)
    plt.title('Salario promedio por nivel de estudios')
    plt.xticks(rotation=45)
    plt.xlabel('Nivel de educación')
    plt.ylabel('Salario promedio')
    plt.grid(True, axis='y', color='#eeeeee')
    plt.gca().spines[['right', "top"]].set_visible(False) # quitamos la línea de arriba y de la derecha
    plt.show()
    return

def graph_5(df):
    '''
    Gráfico para ejercicio 5
    ¿Cuál es la proporción de clientes con diferentes tipos de tarjetas de fidelidad?
    '''
    plt.figure(figsize=(7, 4))

    df_fidelity = df["Loyalty Card"].value_counts()
    plt.pie(df_fidelity.values, 
            labels= df_fidelity.index,
            data = df, 
            autopct=  '%1.1f%%', 
            colors = pastel_colors, 
            textprops={'fontsize': 10}, 
            startangle=90, 
            wedgeprops={'edgecolor': 'black'} );
    plt.title('Proporción clientes por tarjeta de fidelidad',fontsize=18, fontname='Comic Sans MS')
    plt.axis('equal')  # Para que el círculo sea perfecto
    plt.show()
    return


def graph_6 (df):
    '''
    Gráfico para ejercicio 6
    ¿Cómo se distribuyen los clientes según su estado civil y género?
    '''
    plt.figure(figsize=(7, 5))

    new_names = ["Casado", "Soltero", "Divorciado"]
    sns.countplot(x = "Marital Status", 
                data = df,
                palette = pastel_colors,
                width=0.4, 
                hue = "Gender", 
                edgecolor='black')
    plt.xlabel("Estado civil")
    plt.ylabel("Nº clientes")
    plt.title('Distribución de clientes por género y estado civil')
    plt.xticks(ticks=range(len(new_names)), labels=new_names, rotation=0)
    plt.grid(True, axis='y', color='#eeeeee')
    plt.legend(title="Género", labels=["Mujeres", "Hombres"])
    plt.gca().spines[['right', "top"]].set_visible(False) # quitamos la línea de arriba y de la derecha
    plt.show()
    return

# %%
# FUNCIÓN COMBINADA
#=================================


def activate_graphics(df):
    '''
    Ejecuta cada pregunta con su gráfico y respuesta
    ''' 
    print("1. ¿Cómo se distribuye la cantidad de vuelos reservados por mes durante el año?")
    print("Respuesta: tras poder comprobar la información por mes de dos años consecutivos vemos que el patrón se repite, siendo el mes con más movimiento el de julio pero seguido de cerca por los meses de junio, agosto y diciembre. Podemos relacionar estos picos con las vacaciones estivales y Navidad. Por contra, los meses con menos movimiento son enero y febrero que coincide con que no hay fiestas reseñables en estos meses.")
    graph_1(df)
    print("-"*50)
    print("2. ¿Existe una relación entre la distancia de los vuelos y los puntos acumulados por los clientes?")
    print("Respuesta: definitivamente sí, están estrechamente relacionados. A más distancia recorrida en vuelo más puntos acumulan los clientes. ")
    graph_2(df)
    print("-"*50)
    print("3. ¿Cuál es la distribución de los clientes por provincia o estado?")
    print("Respuesta: Esta es la distribución, siendo con diferencia Ontario, British Columbia y Quebec las que acumulan la mayor parte de los clientes. ")
    graph_3(df)
    print("-"*50)
    print("4. ¿Cómo se compara el salario promedio entre los diferentes niveles educativos de los clientes?")
    print("Respuesta: el salario aumenta en relación al nivel de estudios con la única excepción de que los técnicos cobran de media ligeramente más que las personas con grado universitario. ")
    graph_4(df)
    print("-"*50)
    print("5. ¿Cuál es la proporción de clientes con diferentes tipos de tarjetas de fidelidad?")
    print("Respuesta: nada que añadir a lo reflejado en el gráfico:\nStar: 45.6%\nAurora: 20.6%\nNova: 33.8%")
    graph_5(df)
    print("-"*50)
    print("6. ¿Cómo se distribuyen los clientes según su estado civil y género?")
    print("Respuesta: no hay diferencias reseñables entre género pero sí entre estado civil. Son los casados los que más reservan seguidos de los solteros y en último caso los divorciados.")
    graph_6(df)
    print("-"*50)
    return                      
# %%