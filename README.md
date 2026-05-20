# 📊 `analisis_df` — Análisis Exploratorio de Datos desde cero

Una función de **Análisis Exploratorio de Datos (EDA)** construida sobre Pandas que implementa su propia lógica estadística y matemática, sin depender de métodos de alto nivel como `.describe()`. Ideal para proyectos académicos o para quienes quieren entender los cálculos que hay detrás del análisis de datos.

---

## ✨ Características

- 🔢 **Estadísticas descriptivas completas** calculadas algorítmicamente: media, mediana, moda, varianza, desviación estándar, sesgo y curtosis.
- 📦 **Cuartiles y rango intercuartil** con interpolación lineal precisa.
- 🕳️ **Detección de valores faltantes** con conteo absoluto y porcentaje por columna.
- 👥 **Identificación de filas duplicadas** usando hashing O(1) con `set()`.
- 🔤 **Análisis de variables categóricas**: extrae la moda de cada columna de texto.
- 🔢 **Análisis de variables numéricas**: reporte estadístico completo por columna.

---

## 🧠 Lógica Interna

### Funciones auxiliares

| Función | Descripción |
|---|---|
| `_mdp(datos_ordenados, k)` | Calcula el percentil *k* mediante **interpolación lineal**. Usado para Q1 y Q3. |
| `_mdtc(datos)` | Motor estadístico principal. Calcula todas las métricas descriptivas iterando sobre los datos. |

### Métricas calculadas por `_mdtc`

**Tendencia Central**
- **Media**: suma total / *n*
- **Mediana**: valor central de la lista ordenada (promedia los dos centrales si *n* es par)
- **Moda**: valor más frecuente, determinado construyendo un diccionario de frecuencias

**Dispersión y Forma**
- **Rango**: máximo − mínimo
- **Varianza poblacional**: promedio de los cuadrados de las desviaciones respecto a la media
- **Desviación estándar**: raíz cuadrada de la varianza
- **Coeficiente de asimetría (sesgo)**: tercer momento central normalizado por σ³
- **Curtosis (exceso)**: cuarto momento central normalizado por σ⁴, restando 3 para referencia respecto a la distribución normal

**Localización**
- **Q1 (percentil 25)** y **Q3 (percentil 75)** por interpolación lineal
- **Rango intercuartil (IQR)**: Q3 − Q1

### Bloques del reporte principal

| Sección | Método | Complejidad |
|---|---|---|
| Datos faltantes | `isna().sum()` vectorizado | O(n·m) |
| Duplicados | Conversión a tupla + `set` | O(n) promedio |
| Variables numéricas | `select_dtypes` + `_mdtc` | O(n log n) por columna |
| Variables categóricas | Conteo iterativo + moda | O(n) por columna |

---

## ⚙️ Requisitos

- Python 3.x
- [pandas](https://pandas.pydata.org/)

```bash
pip install pandas
```

---

## 🚀 Uso

```python
import pandas as pd

# 1. Crear el DataFrame
datos = {
    'Variable_A': [12.5, 15.0, 14.2, 12.5, None, 18.1],
    'Variable_B': [100, 200, 150, 100, 300, 250],
    'Categoria':  ['Tipo1', 'Tipo2', 'Tipo1', 'Tipo3', 'Tipo1', 'Tipo2']
}
df_ejemplo = pd.DataFrame(datos)

# 2. Ejecutar el análisis
analisis_df(df_ejemplo)
```

### Salida esperada

```
=== REPORTE DE DATOS FALTANTES ===
              Total_NA  Porcentaje_NA (%)
Variable_A           1          16.666667
Variable_B           0           0.000000
Categoria            0           0.000000

=== REPORTE DE REGISTROS DUPLICADOS ===
No se encontraron filas duplicadas.

=== ANÁLISIS DE VARIABLES NUMÉRICAS ===

--- Variable_A ---
  > TENDENCIA CENTRAL:
    Media:              14.46
    Mediana:            14.2
    Moda:               12.5
  > DISPERSIÓN Y FORMA:
    Rango:              5.6  (12.5 a 18.1)
    Varianza:           3.87
    Desviación est.:    1.97
    Coef. asimetría:    0.73
    Curtosis:           -0.8262
  > LOCALIZACIÓN (CUARTILES):
    Q1 (25%):           12.5
    Q3 (75%):           15.35
    Rango intercuartil: 2.85

=== ANÁLISIS DE VARIABLES CATEGÓRICAS (MODA) ===
  Variable: Categoria            | Moda: Tipo1
```

---

## 📁 Estructura del proyecto

```
📦 tu-repositorio/
 ┣ 📜 analisis_df.py      # Función principal
 ┣ 📓 demo.ipynb          # Notebook de ejemplo (opcional)
 ┗ 📄 README.md
```

---

## 📌 Notas de diseño

> Este script **no usa** `.describe()`, `.skew()`, `.kurt()` ni ningún método estadístico de alto nivel de pandas o scipy. Toda la matemática es implementada directamente en Python puro, lo que lo convierte en una referencia de aprendizaje sobre cómo funcionan estas métricas internamente.

La detección de duplicados utiliza una estructura `set` de Python, cuya verificación de pertenencia tiene complejidad **O(1)** en promedio, lo que resulta más eficiente que una búsqueda iterativa tradicional O(n).

---


