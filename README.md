# 🚀 Proyecto ETL y Análisis de Datos - Programa de Lealtad Aerolínea

Este repositorio contiene el proyecto desarrollado en el bootcamp de analítica de datos de Adalab. El objetivo es analizar el comportamiento de clientes en un programa de lealtad de una aerolínea, realizando un proceso completo ETL y análisis exploratorio.

---

## 📂 Estructura del repositorio

### Ejercicio_propuesto/  
- Notebook Jupyter con el análisis original y respuestas al ejercicio propuesto.  
- Archivos incluidos:  
  - Datos originales (`Customer Flight Activity.csv`, `Customer Loyalty History.csv`)  
  - `Customer_union.csv` (resultado tras limpieza y unión de datos)

### Ejercicio_bonus_etl/  
- Código completo del proceso ETL en Python, organizado en:  
  - `main.py`: Script principal que orquesta el flujo completo.  
  - `functions.py`: Funciones para apertura, análisis, transformación, pruebas de hipótesis y guardado.  
  - `graphics.py`: Funciones para todas las visualizaciones relacionadas con el análisis.  
  - `bbdd_sql.py`: Scripts para crear la base de datos y cargar los datos en MySQL.  
- Archivos incluidos:  
  - Datos originales (`Customer Flight Activity.csv`, `Customer Loyalty History.csv`)  
  - `Customer_union_py.csv` (archivo final tras transformación y limpieza)

---

## 🎯 Objetivos del proyecto

- Realizar una exploración y limpieza exhaustiva de los datos, detectando y tratando valores nulos o inconsistencias.  
- Unificar ambos datasets para contar con una única fuente fiable y completa.  
- Visualizar y analizar la relación entre variables clave, como vuelos reservados, distancia y puntos acumulados.  
- Evaluar hipótesis estadísticas para detectar diferencias en comportamiento según el nivel educativo.  
- **No solicitado:** Implementar un proceso ETL robusto, incluyendo carga automatizada en base de datos MySQL para su posterior explotación.

---

## ⚙️ Requisitos y ejecución

- **Python 3.x**  
- Librerías: `pandas`, `numpy`, `seaborn`, `matplotlib`, `scikit-learn`, `sqlalchemy`, `pymysql`, entre otras.  
- **MySQL** configurado y accesible (solo para la parte de carga en base de datos).

Para ejecutar el proceso ETL completo desde la carpeta `Ejercicio_bonus_etl`, simplemente lanzar:

```bash
python main.py
```
Este script ejecuta todo el flujo: carga, limpieza, análisis, visualización y carga en base de datos.

---

## 📌 Notas

- Los archivos `.csv` originales se mantienen para reproducibilidad.  
- Los resultados intermedios y finales se encuentran en los archivos `Customer_union.csv` y `Customer_union_py.csv`.  
- Los scripts están diseñados para facilitar la comprensión y posible extensión del proyecto.

---

## 🙌 Sobre mí

Este proyecto refleja mi pasión por la analítica de datos y el compromiso con la mejora continua. He aplicado las mejores prácticas aprendidas durante el bootcamp de Adalab para entregar un trabajo organizado, claro y reproducible.

Estoy abierta a recibir feedback, sugerencias y colaboraciones para seguir creciendo en este campo.

¡Muchas gracias por tu interés y tiempo! 😊

---

*Autor: Silvia Farled*  
*Fecha: Junio 2025*