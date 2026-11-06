# Guía de visualización estadística y espacial de Boyacá

Esta guía acompaña al [notebook ejecutable](../kit/Notebooks/Visualizacion_Boyaca.ipynb) y al [proyecto final](../proyecto/Proyecto_final_Boyaca.md). Su objetivo es seleccionar, construir e interpretar visualizaciones de datos municipales con Matplotlib, `pyplot`, Seaborn y GeoPandas.

## Preparación

Desde la raíz del repositorio, active el entorno Python del curso e instale las dependencias:

```bash
python -m pip install -r kit/requirements_visualizacion.txt
jupyter lab
```

Abra `kit/Notebooks/Visualizacion_Boyaca.ipynb`, seleccione el kernel del entorno y ejecute las celdas en orden. Los tres recortes de datos necesarios están en `proyecto/datos/`; no es necesaria una descarga adicional. Las imágenes exportadas quedan en `kit/salidas/visualizacion/`, carpeta que no se incorpora al repositorio.

Si falta `jupyter`, verifique que el entorno esté activo y que la instalación haya terminado sin errores. Si falta una biblioteca, confirme que el kernel sea el del mismo entorno en que se ejecutó `pip`. Las fuentes originales, transformaciones, vigencias y hashes están en el [registro de datos](../proyecto/datos/README.md).

## Conceptos esenciales

**Matplotlib** es la biblioteca de gráficos; `matplotlib.pyplot` es una interfaz para crear figuras y ejes. Se recomienda `fig, ax = plt.subplots(...)`, porque permite personalizar y combinar gráficos. **Seaborn** construye gráficos estadísticos sobre Matplotlib y acepta datos en formato tabular. **GeoPandas** amplía pandas para geometrías y mapas; usa Matplotlib para dibujarlos.

Una figura adecuada responde una pregunta, indica unidad, fuente y periodo, muestra valores faltantes y evita confundir asociación con causalidad. En datos municipales, cada punto representa un municipio, no una persona.

## 1 Comparar poblaciones con barras horizontales

Para reconocer los municipios más poblados en un año, ordene y seleccione antes de dibujar. Ejecute primero las celdas de preparación del notebook para disponer de `base` y `ANIO`.

```python
top = base.nlargest(10, "poblacion_total").sort_values("poblacion_total")
fig, ax = plt.subplots(figsize=(9, 5))
ax.barh(top["municipio"], top["poblacion_total"], color="#3478a3")
ax.set(title=f"10 municipios más poblados de Boyacá, {ANIO}",
       xlabel="Habitantes proyectados", ylabel="Municipio")
fig.tight_layout()
plt.show()
```

Las barras deben partir de cero. El número de habitantes es una proyección del DANE, no el resultado de un conteo directo en el año mostrado.

## 2 Comparar hombres y mujeres en los municipios más extensos

Seleccione primero los diez municipios con mayor `area_km2`. Use `melt` para llevar las columnas de hombres y mujeres a dos series y `hue` para distinguirlas:

```python
top_area = base.nlargest(10, "area_km2")
series = top_area.melt(id_vars="municipio", value_vars=["hombres", "mujeres"],
                       var_name="sexo", value_name="poblacion")
sns.barplot(data=series, y="municipio", x="poblacion", hue="sexo", errorbar=None)
plt.xlabel("Habitantes proyectados")
plt.ylabel("Municipio")
plt.tight_layout()
plt.show()
```

Los municipios se eligen por extensión, pero la longitud de las barras muestra población. El área se calculó con los polígonos MGN 2025 originales en un CRS proyectado, antes de simplificarlos para el mapa. El notebook también presenta series temporales 2020–2025, en paneles separados. Como los paneles tienen escalas independientes, compare las tendencias observando los ejes.

## 3 Examinar distribuciones

El histograma cuenta municipios en intervalos de porcentaje; el diagrama de caja resume mediana, cuartiles y posibles valores extremos:

```python
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(data=base, x="porcentaje_18_44", bins=12, ax=ax[0])
sns.boxplot(data=base, x="porcentaje_18_44", ax=ax[1])
ax[0].set(ylabel="Número de municipios", xlabel="Población de 18 a 44 años (%)")
ax[1].set(xlabel="Población de 18 a 44 años (%)")
fig.tight_layout()
plt.show()
```

Investigue los valores extremos antes de excluirlos. Un municipio con un porcentaje inusual no es necesariamente un registro erróneo.

## 4 Explorar relaciones entre variables

Una dispersión muestra la relación de dos indicadores. El notebook une por código municipal la proporción de población joven y el rendimiento de papa en 2024. El rendimiento se calcula como suma de producción dividida por suma de área cosechada, para la categoría y estado físico documentados.

```python
sns.scatterplot(data=validos, x="porcentaje_18_44", y="rendimiento_t_ha")
plt.xlabel("Población de 18 a 44 años (%)")
plt.ylabel("Rendimiento de papa (t/ha)")
plt.title("Relación exploratoria por municipio")
plt.tight_layout()
plt.show()
```

El notebook también calcula la correlación de Spearman y reporta la cantidad de municipios disponibles. La figura no demuestra causalidad. El ejemplo usa rendimiento de papa y no evalúa la hipótesis de desempeño municipal: para ello hay que integrar y validar el puntaje oficial.

## 5 Dibujar mapas municipales

Un coroplético colorea polígonos según una variable. Los mapas de cantidad y de porcentaje responden preguntas distintas; el gris distingue ausencia de información.

```python
fig, ax = plt.subplots(figsize=(8, 7))
base.plot(column="porcentaje_18_44", cmap="YlGn", legend=True, ax=ax,
          edgecolor="white", linewidth=0.15,
          missing_kwds={"color": "lightgrey", "label": "Sin datos"})
ax.set_title(f"Boyacá: población de 18 a 44 años (%), {ANIO}")
ax.set_axis_off()
fig.tight_layout()
plt.show()
```

Para medir áreas no use coordenadas geográficas en grados: transforme a un sistema proyectado apropiado. La geometría de ejemplo está simplificada para visualización; para intersecciones de suelos, mediciones y análisis finales use las capas originales y evalúe su calidad, escala y vigencia. Los límites MGN son geoestadísticos y no deben tratarse automáticamente como límites legales.

## Del ejemplo al proyecto final

1. Integre los puntajes oficiales de desempeño por DIVIPOLA y año; compruebe cardinalidad y cobertura.
2. Repita la dispersión y el mapa para la proporción de población de 18 a 44 años frente al desempeño. Reporte el número de municipios, el método, la incertidumbre y las limitaciones.
3. Incorpore la capa original de capacidad de uso de las tierras y calcule composición por municipio. No interprete el rendimiento de papa como calidad del suelo.
4. Ajuste títulos, escalas, unidades, colores y fuentes; represente explícitamente los municipios sin información.
5. Guarde las figuras desde el pipeline e incluya el código y los datos o su procedimiento de obtención en la entrega.

El ejemplo de población no equivale a población económicamente activa ni a trabajadores agrícolas. Los datos y geometrías son recortes para aprender; cada grupo debe validar y actualizar las fuentes de su propio análisis.
