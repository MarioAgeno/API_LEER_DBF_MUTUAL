# API_LEER_DBF_MUTUAL

API REST en FastAPI para consultar socios, prestamos, cuotas, saldos y movimientos desde archivos DBF de Mutual.

## Descripcion

La API toma la ruta base de los DBF desde la variable de entorno DBF_PATH y expone endpoints de consulta.

Incluye:

- Consulta de socio por CUIT
- Consulta de socio por codigo
- Prestamos por socio
- Prestamo por numero de ayuda
- Cuotas por ayuda
- Saldos de cuentas
- Resumen mensual de movimientos
- Resumen historico de movimientos

Tambien expone documentacion en /docs y esquema OpenAPI en /openapi.json.

## Requisitos

- Python 3.12 o superior
- Acceso a los archivos DBF
- Archivo .env con DBF_PATH

## Instalacion

1. Crear entorno virtual:

   python -m venv venv

2. Activar entorno virtual en PowerShell:

   .\venv\Scripts\Activate.ps1

3. Instalar dependencias:

   pip install -r requirements.txt

## Configuracion

Crear archivo .env en la raiz con:

DBF_PATH=\\servidor\ruta\a\DATA

Archivos DBF esperados por la implementacion actual:

- Socios.dbf
- Movae01.dbf
- Cuotas.dbf
- sdoca01.dbf
- comprobantes.dbf
- movca01.dbf
- amvcpto.dbf

## Ejecucion

Desde la raiz del proyecto:

uvicorn main:app --reload

URL local:

http://127.0.0.1:8000

Documentacion:

http://127.0.0.1:8000/docs

## Produccion

Para que la API quede accesible desde la red y no solo desde localhost, definila con variables de entorno:

APP_HOST=0.0.0.0
APP_PORT=8000

Despues se accede con la IP publica o la IP del servidor, por ejemplo:

http://IP_PUBLICA:8000/docs

Si cambiamos el puerto, hay que abrir ese puerto en el firewall del servidor.

## NSSM

Si la vas a levantar como servicio con NSSM, una configuracion simple es:

Programa:

D:\PYTHON\API_LEER_DBF_MUTUAL\venv\Scripts\python.exe

Argumentos:

main.py

Directorio inicial:

D:\PYTHON\API_LEER_DBF_MUTUAL

Variables de entorno del servicio:

APP_HOST=0.0.0.0
APP_PORT=8000
DBF_PATH=\\servidor\ruta\a\DATA

Tambien podes usar uvicorn directo desde NSSM con:

main:app --host 0.0.0.0 --port 8000

## Endpoints

1. GET /socio/{cuit}
2. GET /sociocodigo/{codigo_socio}
3. GET /prestamos/{codigo_socio}
4. GET /ayuda/{ayuda}
5. GET /cuotas/{ayuda}
6. GET /saldos/{cuenta}
7. GET /resumen_cuenta/{cuenta}/{tipo}
8. GET /resumen_cuenta_historico/{cuenta}/{tipo}

## Respuestas

- 200: consulta exitosa
- 404: sin resultados para el criterio indicado
- 500: error inesperado de lectura o procesamiento

## Notas tecnicas

- Se utiliza dbfread para leer DBF.
- Se usa un parser tolerante para evitar errores por campos invalidos o vacios en DBF.
- Para comparar identificadores (CUIT, codigo, ayuda), la API normaliza formatos numericos para tolerar diferencias de ceros, decimales y separadores.

## Comandos utiles de Git para push

Si VS Code vuelve a generar conflicto con el README, podes hacer el push por terminal:

git add README.md
git commit -m "Recrear README"
git push origin master
