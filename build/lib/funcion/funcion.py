

#| echo: true
#| code-fold: true
#| code-summary: "Ver código completo"
import pandas as pd
import statistics

df = pd.read_csv("Accidentalidad_en_Barranquilla_victimas_20260227.csv")

def analizar_dataframe(df):

    # ─── Medidas ───────────────────────────────────────────────────

    def _mdp(datos_ordenados, k):
        """Calcula el percentil k de una lista ya ordenada."""
        n = len(datos_ordenados)
        posicion = (k / 100) * (n - 1)
        inferior = int(posicion)
        if inferior >= n - 1:
            return datos_ordenados[-1]
        fraccion = posicion - inferior
        return datos_ordenados[inferior] + fraccion * (datos_ordenados[inferior + 1] - datos_ordenados[inferior])

    def _mdtc(datos):
        """Calcula y muestra estadísticas descriptivas de una lista numérica."""
        n = len(datos)
        media = sum(datos) / n

        datos_ord = sorted(datos)

        mediana = datos_ord[n // 2] if n % 2 != 0 else (datos_ord[n // 2 - 1] + datos_ord[n // 2]) / 2

        frecuencias = {}
        for x in datos:
            frecuencias[x] = frecuencias.get(x, 0) + 1
        moda = max(frecuencias, key=frecuencias.get)

        valor_min, valor_max = datos_ord[0], datos_ord[-1]
        rango = valor_max - valor_min

        varianza   = sum((x - media) ** 2 for x in datos) / n
        desviacion = varianza ** 0.5
        sesgo      = (sum((x - media) ** 3 for x in datos) / n) / (desviacion ** 3)
        curtosis   = (sum((x - media) ** 4 for x in datos) / n) / (varianza ** 2) - 3

        q1  = _mdp(datos_ord, 25)
        q3  = _mdp(datos_ord, 75)
        iqr = q3 - q1

        print("  > TENDENCIA CENTRAL:")
        print(f"    Media:              {media}")
        print(f"    Mediana:            {mediana}")
        print(f"    Moda:               {moda}")
        print("  > DISPERSIÓN Y FORMA:")
        print(f"    Rango:              {rango}  ({valor_min} a {valor_max})")
        print(f"    Varianza:           {round(varianza, 2)}")
        print(f"    Desviación est.:    {round(desviacion, 2)}")
        print(f"    Coef. asimetría:    {round(sesgo, 2)}")
        print(f"    Curtosis:           {curtosis:.4f}")
        print("  > LOCALIZACIÓN (CUARTILES):")
        print(f"    Q1 (25%):           {round(q1, 2)}")
        print(f"    Q3 (75%):           {round(q3, 2)}")
        print(f"    Rango intercuartil: {round(iqr, 2)}")

    # ─── 1. DATOS FALTANTES ────────────────────────────────────────────────────

    filas_total   = len(df)
    porcentaje_na = (df.isna().sum() / filas_total) * 100
    df_faltantes  = pd.DataFrame({
        'Total_NA': df.isna().sum(),
        'Porcentaje_NA (%)': porcentaje_na
    })
    columnas_na = df_faltantes[df_faltantes['Total_NA'] >= 0].sort_values(
        by='Porcentaje_NA (%)', ascending=False
    )

    print("=== REPORTE DE DATOS FALTANTES ===")
    if columnas_na.empty:
        print("¡Excelente! No hay datos faltantes en ninguna columna.\n")
    else:
        print(columnas_na, "\n")

    # ─── 2. DUPLICADOS ────────────────────────────────────────────────────────

    filas_vistas = set()
    duplicados   = 0
    for fila in df.values.tolist():
        t = tuple(fila)
        if t in filas_vistas:
            duplicados += 1
        else:
            filas_vistas.add(t)

    print("=== REPORTE DE REGISTROS DUPLICADOS ===")
    if duplicados == 0:
        print("No se encontraron filas duplicadas.\n")
    else:
        print(f"Se encontraron {duplicados} filas exactamente iguales.\n")

    # ─── 3. VARIABLES NUMÉRICAS ───────────────────────────────────────────────

    columnas_numericas = df.select_dtypes(include=['number', 'Int64']).columns
    print("=== ANÁLISIS DE VARIABLES NUMÉRICAS ===")
    for columna in columnas_numericas:
        print(f"\n--- {columna} ---")
        lista_datos = df[columna].dropna().tolist()
        _mdtc(lista_datos)

    # ─── 4. VARIABLES CATEGÓRICAS ─────────────────────────────────────────────

    columnas_categoricas = df.select_dtypes(include=['object', 'string']).columns
    print("\n=== ANÁLISIS DE VARIABLES CATEGÓRICAS (MODA) ===")
    for col in columnas_categoricas:
        datos_cat = df[col].dropna().tolist()
        if datos_cat:
            frec = {}
            for x in datos_cat:
                frec[x] = frec.get(x, 0) + 1
            moda_cat = max(frec, key=frec.get)
            print(f"  Variable: {col:20} | Moda: {moda_cat}")

    # ─── 5. TABLA DE VALIDACIÓN ────────────────────────────────────────────────

    print("\n=== TABLA DE VALIDACIÓN CON LIBRERÍAS NATIVAS ===")

    filas = []
    for columna in df.select_dtypes(include=['number', 'Int64']).columns:
        datos = df[columna].dropna().tolist()
        if not datos:
            continue

        filas.append({
            'Columna':    columna,
            'Media':      round(statistics.mean(datos), 2),
            'Mediana':    round(statistics.median(datos), 2),
            'Moda':       statistics.mode(datos),
            'Varianza':   round(statistics.pvariance(datos), 2),
            'Desv. Est.': round(statistics.pstdev(datos), 2),
            'Q1':         round(statistics.quantiles(datos, n=4)[0], 2),
            'Q3':         round(statistics.quantiles(datos, n=4)[2], 2),
            'Rango':      round(max(datos) - min(datos), 2),
        })

    df_validacion = pd.DataFrame(filas).set_index('Columna')
    print(df_validacion.to_string())


analizar_dataframe(df)