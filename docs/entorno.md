# Datos y ejecución sobre WSL Ubuntu-26.04

[Instalación completa desde Windows](instalacion-wsl.md) · [Índice](../README.md)

Como apoyo para las personas con poca experiencia en la CLI de Linux, se anexó la [guía de línea de comandos](guia-cli-linux/README.md), con ejemplos de navegación, consulta y verificación de archivos, además de un cheat sheet de 100 comandos y sus opciones habituales.

Todas las instrucciones de esta página se ejecutan en **Ubuntu-26.04 sobre WSL 2**, después de preparar el entorno indicado en la guía. Antes de iniciar:

```bash
cd /mnt/c/Users/TUPTC/bigdata
cd big-data-postgraduate
source .venv/bin/activate
cd kit
```

El clon no incluye los originales agroambientales ni los completos PQRS; `--verificar` requiere obtener antes todas las fuentes correspondientes.

## Tres rutas para obtener los datos

- Ruta A, recomendada para clase: descomprimir el paquete docente, que ya contiene data/raw. Ejecutar --verificar. Permite continuar sin Internet una vez instalado el software.
- Ruta B, práctica de descarga: crear una carpeta nueva, copiar 00_datos.py y fuentes.json, y ejecutar --descargar con los IDs requeridos. No descargar todas las fuentes simultáneamente.
- Ruta C, contingencia: copiar una carpeta raw de respaldo verificada mediante --respaldo. El script comprueba el SHA-256 antes de incorporar archivos.

```
python 00_datos.py --descargar agrosavia divipola eva
python 00_datos.py --descargar igac_capacidad igac_quimica
python 00_datos.py --descargar soilgrids wosis nasa chirps
python 00_datos.py --respaldo "/ruta/kit_original/data/raw" --verificar
```

Las URLs exactas están en fuentes.json y en el [catálogo de fuentes](datasets.md). El descargador limita cada respuesta a tres veces el tamaño de referencia o 2 MB, lo que sea mayor. Rechaza páginas HTML, no sobrescribe archivos existentes y conserva una descarga que cambió como .nueva. Un SHA-256 distinto puede deberse a nuevos datos o a cambios de serialización: el docente revisa esquema, valores y conteos antes de aprobar otro corte. No se considera que un HTTP 200 por sí solo sea una descarga válida.

## Descarga manual de los shapes DANE

[Fuente](<https://geoportal.dane.gov.co/servicios/descarga-y-metadatos/datos-geoestadisticos/>)

- Abrir el catálogo vigente y buscar MGN2025-Nivel. Seleccionar los enlaces de Nivel Departamento y Nivel Municipio en formato Shapefile.
- Guardar los ZIP sin modificar como dane_departamentos.zip y dane_municipios.zip dentro de data/raw. Tamaños observados: 12,52 MB y 71,58 MB. Las etiquetas del catálogo pueden diferir del tamaño descargado.
- Verificar con 00_datos.py --verificar. GeoPandas lee los ZIP DANE con read_file y el prefijo zip://. Si se extraen, conservar .shp, .shx, .dbf y .prj juntos y comprobar el CRS antes de reproyectar.
- Si el portal responde 403 o la descarga tarda, usar la copia docente. No insistir con múltiples descargas. El enlace antiguo del MGN devolvió 404 y no debe quedar como dependencia del taller.

No descargar MGN2025_00_COLOMBIA.zip con todos los niveles: el catálogo anuncia aproximadamente 1,5 GB y contiene detalle que no requiere el curso. Los dos ZIP seleccionados incluyen exclusivamente los niveles necesarios. No se reemplazan polígonos por puntos de DIVIPOLA para evitar esa descarga.

## Verificación y organización

```
kit/
  fuentes.json
  00_datos.py
  talleres.py
  spark_taller.py
  data/raw/       # originales sin editar
  salidas/        # resultados reconstruibles
  entregas/      # informes personales
```

Leer salidas/verificacion.json: archivo presente, huella coincidente, conteo esperado, JSON sin error de API y ZIP íntegro. Los scripts reconstruyen y sobrescriben sus salidas homónimas; las conclusiones del estudiante se guardan en entregas. En nuevas descargas registrar fecha, versión, licencia, URL, tamaño y huella. Para reproducibilidad guardar también python --version y python -m pip freeze.

## Preparación del dominio PQRS

Las dependencias se instalan según [la guía WSL](instalacion-wsl.md). Desde `kit/`, en Ubuntu y con `.venv` activo:

```
python pqrs_descarga.py --listar
python pqrs_talleres.py perfil
python pqrs_talleres.py formatos
```

Por defecto se utilizan las tres muestras incluidas en data/pqrs_muestras. Para datos completos: descargar selectivamente y señalar la carpeta con --datos y --completo. No se incluye otra copia de 1,82 GB en el ZIP docente.

```
python pqrs_descarga.py --descargar 2024_I
python pqrs_descarga.py --verificar
python pqrs_talleres.py perfil --completo --datos data/pqrs_completos
```

La verificación completa requiere los tres cortes; si solo se descargó uno, la comprobación informará los que faltan. Para probar un único CSV con pandas, usar su separador y chunksize según P01. Los scripts de prácticas completas están diseñados para los tres cortes. La descarga rechaza HTML, limita cada archivo a 1,5 veces el tamaño de referencia y conserva como .nueva una fuente cuyo hash cambió.

Espacio: 5 GB para la ruta de muestras y datos agroambientales; reservar 8 GB para los tres CSV PQRS, Parquet, temporales y salidas. Con herramientas instaladas, planificar 15–20 GB libres para la ruta completa. Son presupuestos preventivos, no tamaños de instalación medidos. Usar SSD y bloques de 25.000 filas; bajar a 5.000–10.000 si la RAM es limitada. Con 8 GB se recomienda mantener el benchmark pandas en muestras y ampliar completos con DuckDB/Polars.

## Notebooks actuales

Seguir [la instalación WSL y registro del kernel](instalacion-wsl.md). Desde Ubuntu, con el entorno de la raíz activo y situado en `kit/`:

```bash
python -m jupyter lab --no-browser --ip=127.0.0.1
```

Abrir `Notebooks/` y seleccionar el kernel BigData de WSL. Las dependencias y herramientas se instalan en Ubuntu, no en Windows. Los anexos históricos conservan comandos originales de Colab únicamente como referencia.

## Rutas de los scripts

Los scripts vigentes resuelven sus fuentes y salidas a partir de su archivo dentro de `kit/`. En PQRS, `--config`, `--datos` y `--salidas` relativos también se interpretan desde `kit/`; las rutas absolutas se respetan. El descargador general interpreta `--respaldo` desde el directorio actual: usar una ruta absoluta para una copia externa. No escribir rutas de otra máquina dentro de los scripts.

## Ejecución geoespacial

Usar el único entorno WSL del curso con GeoPandas, Pyogrio, Rasterio y Matplotlib. Desde `kit/`, `python talleres.py geografia` ejecuta E08, `python talleres.py suelo` prepara E09 y `python talleres.py clima` prepara E11. Los mapas se generan en Jupyter o como PNG en `salidas/`. `python talleres.py clima_suelo` reúne ambos informes para compatibilidad y requiere las cuatro fuentes SoilGrids, WoSIS, NASA y CHIRPS. Consultar el [índice de notebooks](../kit/Notebooks/README.md).
