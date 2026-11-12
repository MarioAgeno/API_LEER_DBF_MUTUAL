# API_LEER_DBF_MUTUAL

API REST en FastAPI para consultar socios, prestamos, cuotas, saldos y movimientos desde archivos DBF de Mutual.

**Versión actual:** 2.1 con integración completa a AgilPagos

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
- **[v2.0]** Información de AgilPagos y trámite de DNI en consultas de socios
- **[v2.1 NUEVO]** Integración completa con catálogos de AgilPagos (Tipo de Persona, Actividad, Estado Civil, Provincia, País, Situación IVA)

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

Archivos DBF esperados por la implementacion actual (versión 2.1):

**REQUERIDOS:**
- Socios.dbf (contiene TRAMITEDNI, TIPOPERS, ESTCIVIL, CODPOSTAL, PAIS, SITIVA, ACTIVIDAD)
- Movae01.dbf
- Cuotas.dbf
- sdoca01.dbf
- comprobantes.dbf
- movca01.dbf
- amvcpto.dbf

**PARA INTEGRACIÓN AGILPAGOS (v2.1):**
- sociosSG.dbf (Datos de cuenta en AgilPagos)
- UIFPersona.dbf (Tipo de Persona con id_sg)
- Actividad.dbf (Actividades económicas con id_sg)
- EstCivil.dbf (Estados civiles con id_sg)
- horasacr.dbf (Relación para provincias)
- provincias.dbf (Provincias con id_sg)
- Paises.dbf (Países con id_sg)
- CodIva.dbf (Códigos de IVA con id_sg)

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

1. **GET /socio/{cuit}** - Consulta socio por CUIT
   - Incluye: Tramite DNI, AgilPagos, Datos de Integración (v2.1)
   
2. **GET /sociocodigo/{codigo_socio}** - Consulta socio por código
   - Incluye: Tramite DNI, AgilPagos, Datos de Integración (v2.1)
   
3. GET /prestamos/{codigo_socio}
4. GET /ayuda/{ayuda}
5. GET /cuotas/{ayuda}
6. GET /saldos/{cuenta}
7. GET /resumen_cuenta/{cuenta}/{tipo}
8. GET /resumen_cuenta_historico/{cuenta}/{tipo}

## Nuevos Campos en Endpoints de Socios - v2.0

### Tramite DNI
- Tipo: String o null
- Descripción: Número de trámite del DNI del socio
- Fuente: Campo TRAMITEDNI de Socios.dbf

### AgilPagos (Objeto)
- Descripción: Información de integración con AgilPagos desde tabla sociosSG.dbf
- Campos:
  - **id_sg**: ID único en sistema AgilPagos
  - **id_user**: ID de usuario en AgilPagos
  - **cuentamutu**: Número de cuenta del socio en la mutual
  - **alta**: Fecha de alta en AgilPagos (YYYY-MM-DD)

## Nuevos Campos en Endpoints de Socios - v2.1 (AgilPagos Completo)

### Datos_Integracion_AgilPagos (Objeto)
Contiene los identificadores en AgilPagos de los catálogos relacionados:

- **tipo_persona_id_sg**: ID de UIFPersona (Tipo de Persona)
- **actividad_id_sg**: ID de Actividad (Código de Actividad Económica)
- **estado_civil_id_sg**: ID de EstCivil (Estado Civil)
- **provincia_id_sg**: ID de Provincias (Provincia/Localidad)
- **pais_id_sg**: ID de Paises (País)
- **situacion_iva_id_sg**: ID de CodIva (Situación Fiscal/IVA)

Todos estos campos facilitan la integración con la billetera de AgilPagos del banco Coinag.

**Nota**: Si la tabla sociosSG no existe o el socio no está registrado en AgilPagos, el campo AgilPagos será un objeto vacío {}.

## Ejemplo de Respuesta

```json
{
  "Codigo": "1001",
  "Nombre": "Juan Carlos García López",
  "CUIT": "20123456789",
  "Numero Documento": "12345678",
  "Tramite DNI": "ABC123DEF456",
  "...otros campos...",
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  }
}
```

## Respuestas

- 200: consulta exitosa
- 404: sin resultados para el criterio indicado
- 500: error inesperado de lectura o procesamiento

## Notas tecnicas

- Se utiliza dbfread para leer DBF.
- Se usa un parser tolerante para evitar errores por campos invalidos o vacios en DBF.
- Para comparar identificadores (CUIT, codigo, ayuda), la API normaliza formatos numericos para tolerar diferencias de ceros, decimales y separadores.
- La función get_socio_sg_data() maneja excepciones gracefully si sociosSG.dbf no existe.
- Todas las funciones de integración AgilPagos (v2.1) devuelven null si la tabla no existe, sin interrumpir el flujo.

## Documentacion Adicional

### Guías Rápidas
- [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Inicio rápido y ejemplos básicos
- [CAMBIOS.md](CAMBIOS.md) - Detalles técnicos de las modificaciones

### Integración AgilPagos
- [AGILPAGOS_INTEGRACION.md](AGILPAGOS_INTEGRACION.md) - Guía técnica completa de la integración (v2.1)
  - Especificación de todas las 6 nuevas funciones helper
  - Diagramas de relación entre tablas
  - Lógica de resolución de cada id_sg
  - Troubleshooting y casos edge

- [EJEMPLOS_AGILPAGOS.md](EJEMPLOS_AGILPAGOS.md) - Ejemplos prácticos de integración
  - Respuestas JSON completas
  - Patrones de integración con AgilPagos
  - Código de validación
  - Manejo de casos especiales

### Ejemplos y Testing
- [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md) - Ejemplos completos de respuestas v2.0
- [test_socios.py](test_socios.py) - Suite de tests básica para v2.0
- [test_socios_v2.py](test_socios_v2.py) - Suite de tests ampliada con validación de campos AgilPagos (v2.1)

## Testing

Para verificar que la integración AgilPagos funciona correctamente:

```bash
# Ejecutar tests básicos
python test_socios.py

# Ejecutar tests completos de integración AgilPagos (v2.1)
python test_socios_v2.py
```

Los tests verifican:
- Presencia de todos los campos en la respuesta
- Formato correcto de los datos
- Relaciones entre tablas
- Valores null cuando las tablas no están disponibles

## Version History

**v2.1** (Actual)
- Integración completa con catálogos AgilPagos
- 6 nuevos campos id_sg para billetera de AgilPagos del banco Coinag
- Campo Datos_Integracion_AgilPagos con todos los identificadores
- Suite de tests ampliada (test_socios_v2.py)
- Documentación técnica detallada

**v2.0**
- Campo Tramite DNI (TRAMITEDNI)
- Integración inicial con sociosSG.dbf
- Campo AgilPagos con datos básicos
- Tests básicos

**v1.0**
- API inicial para consultas de socios, préstamos, cuotas, etc.

## Comandos utiles de Git para push

Si VS Code vuelve a generar conflicto con el README, podes hacer el push por terminal:

```bash
git add README.md
git commit -m "Actualizar README a v2.1 con integración AgilPagos"
git push origin master
```
