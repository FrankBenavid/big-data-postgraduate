# MATERIAL PRACTICO DEL CURSO DE BIG DATA

Este paquete acompaña los dos documentos Word. Incluye seis programas completos
y el archivo de dependencias. Los datos son sintéticos y se generan localmente.
No se necesitan cuentas de nube ni datos privados.

Entorno de referencia: Python 3.12 y Java 17.
Crear un entorno virtual e instalar con:

```bash
python -m pip install -r requirements.txt
```


Ejecutar desde esta carpeta, en este orden:

```bash
python 01_generar_datos.py --n 20000
python 02_calidad_duckdb.py
python 03_spark_lotes.py
python 04_benchmark.py
python 05_streaming.py
python 06_modelo.py
```


Los programas 03 y 05 requieren Java y crean una sesión local de Spark.
En un notebook deben ejecutarse en el entorno que tiene los paquetes instalados.
El script 01 usa argparse: desde Jupyter se recomienda invocarlo con

```python
%run 01_generar_datos.py --n 20000
```

Los demás también pueden invocarse con %run y su nombre.

## DATOS Y SALIDAS
Se escriben bajo datos/. Volver a ejecutar 01 reemplaza pedidos.csv y esperado.json.
Después hay que ejecutar 02 y los pasos siguientes para mantener consistencia.
Cada ejecución de streaming crea una carpeta nueva con identificador propio.
El ejemplo de consola no demuestra recuperación durable de extremo a extremo.

## RESULTADOS DE CONTROL PARA N=20000 Y SEMILLA 64
20100 filas originales; 100 duplicados exactos; 506 rechazados; 19494 válidos.
Importe válido: 600736176 centavos de una moneda didáctica.
DuckDB y Spark deben coincidir exactamente en conteos e importes por ciudad.
Los tiempos dependen del equipo y no son un criterio de aprobación numérico.

## VERIFICACION
Los seis programas se ejecutaron en macOS ARM con Python 3.12, Java 17,
DuckDB 1.4.1, PySpark 4.0.1, pandas 2.2.3, PyArrow 19.0.1,
NumPy 2.2.6, scikit-learn 1.6.1 y SciPy 1.14.1.
La instalación y los permisos deben verificarse en cada equipo del curso.
No se validaron todas las combinaciones de Windows, Linux o hardware.
JupyterLab y Matplotlib se incluyen para trabajo interactivo y visualización;
no son necesarios para ejecutar los seis scripts principales.

La guía docente desarrolla fundamentos, instrucciones, resultados esperados,
solucionarios, rúbricas y guiones para preparar las presentaciones.
