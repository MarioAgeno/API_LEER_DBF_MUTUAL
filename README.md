# API_LEER_DBF_MUTUAL

API REST desarrollada con FastAPI para consultar información de socios, préstamos, cuotas, saldos y movimientos en caja de ahorros desde archivos DBF de una mutual.

## Descripción general

Este servicio expone endpoints HTTP para leer datos desde los DBF definidos en la variable de entorno `DBF_PATH`.

La API incluye consultas para:

- Buscar un socio por CUIT.
- Buscar un socio por código.
- Consultar préstamos de un socio.
- Consultar un préstamo por número de ayuda.
- Consultar cuotas de un préstamo.
- Consultar saldos de cuenta.
- Consultar movimientos mensuales e históricos de caja de ahorro.

La documentación interactiva también está disponible en `/docs` y el esquema OpenAPI en `/openapi.json`.

## Requisitos

- Python 3.12 o superior.
- Acceso a los archivos DBF de la mutual.
- Variable de entorno `DBF_PATH` configurada.

## Instalación

1. Crear y activar un entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Configurar la variable de entorno `DBF_PATH`.

## Configuración

El archivo `.env` debe definir al menos:

```env
DBF_PATH=//servidor/ruta/a/DATA
```

Opcionalmente puede existir una ruta remota adicional como referencia operativa, pero la aplicación usa `DBF_PATH` para construir las rutas de los DBF.

### Archivos esperados

Según la implementación actual, la API intenta leer estos archivos:

- `Socios.dbf`
- `Movae01.dbf`
- `Cuotas.dbf`
- `sdoca01.dbf`
- `comprobantes.dbf`
- `movca01.dbf`
- `amvcpto.dbf`

## Ejecución

Desde la raíz del proyecto:

```bash
uvicorn main:app --reload
```

Por defecto el servicio queda disponible en:

```text
http://127.0.0.1:8000
```

La documentación Swagger se abre en:

```text
http://127.0.0.1:8000/docs
```

## Endpoints

### 1. Obtener socio por CUIT

`GET /socio/{cuit}`

Devuelve la información del socio buscado por CUIT.

#### Respuesta

```json
{
  "Codigo": 12345,
  "Nombre": "JUAN PEREZ",
  "Domicilio": "CALLE 123",
  "Codigo Postal": 1000,
  "CUIT": 20123456789,
  "Fecha Nacimiento": "1990-01-01",
  "Fecha Ingreso": "2020-01-01",
  "Es PEP": false,
  "Nacionalidad": "ARGENTINA",
  "Telefono": "12345678",
  "Telefono 2": "87654321",
  "Movil": "1155555555",
  "e-Mail": "persona@correo.com",
  "Codigo Actividad": 101
}
```

### 2. Obtener socio por código

`GET /sociocodigo/{codigo_socio}`

Devuelve la misma información operativa del socio por código.

#### Respuesta

La estructura es equivalente a la consulta por CUIT, incluyendo `Codigo`.

### 3. Obtener préstamos de un socio

`GET /prestamos/{codigo_socio}`

Devuelve todos los préstamos asociados al código de socio recibido.

#### Respuesta

```json
[
  {
    "Ayuda": 123456,
    "fecha": "2024-01-10",
    "TEM": 1.2,
    "TEA": 18.5,
    "TNA": 16.0,
    "CFT": 20.1,
    "Plazo": 24,
    "Cuotas": 24,
    "Capital": 150000.0,
    "Devengamientos": 12000.0,
    "Gastos": 3000.0,
    "Seguro": 2500.0,
    "Total": 167500.0,
    "Linea": "A1",
    "Tipo": "PERSONAL"
  }
]
```

Si no hay préstamos para el socio, el endpoint responde con `404` y el mensaje:

```json
{
  "detail": "No se encontraron préstamos"
}
```

### 4. Obtener préstamo por ayuda

`GET /ayuda/{ayuda}`

Devuelve un préstamo puntual por su número de ayuda.

### 5. Obtener cuotas por ayuda

`GET /cuotas/{ayuda}`

Devuelve el detalle de cuotas asociadas a una ayuda.

#### Respuesta

```json
[
  {
    "Ayuda": 123456,
    "Socio": 12345,
    "Vencimiento": "2024-02-10",
    "Nro.Cuota": 1,
    "Deuda": 150000.0,
    "Capital": 5000.0,
    "Interes": 1200.0,
    "Interes2": 0.0,
    "Gastos": 300.0,
    "Varios": 0.0,
    "Otros": 0.0,
    "Seguro": 250.0,
    "Improte Cuota": 6750.0,
    "Amortizado": 5000.0,
    "Linea": "A1"
  }
]
```

### 6. Obtener saldos de cuentas

`GET /saldos/{cuenta}`

Devuelve los saldos asociados a una cuenta de socio.

### 7. Resumen mensual de cuenta

`GET /resumen_cuenta/{cuenta}/{tipo}`

Devuelve el resumen de movimientos del mes para la cuenta y tipo indicados.

### 8. Resumen histórico de cuenta

`GET /resumen_cuenta_historico/{cuenta}/{tipo}`

Devuelve movimientos históricos filtrados por rango de fechas para la cuenta y tipo indicados.

## Códigos de respuesta

- `200`: consulta exitosa.
- `404`: no se encontraron registros para el criterio consultado.
- `500`: error inesperado al procesar la consulta o leer los archivos.

## Consideraciones técnicas

- La API usa `dbfread` para leer archivos DBF.
- Se implementó un parser tolerante para evitar que valores vacíos o inválidos en campos numéricos, de fecha o lógicos rompan la consulta completa.
- Los endpoints trabajan con rutas sincronizadas internamente, pero FastAPI las expone como HTTP estándar.

## Estructura de respuestas

Las claves de las respuestas mantienen el formato definido en el código actual, incluyendo nombres con mayúsculas, espacios y acentos donde corresponda.

Ejemplos:

- `Codigo`
- `Codigo Postal`
- `Fecha Nacimiento`
- `Nro.Cuota`
- `Improte Cuota`

## Desarrollo

Si vas a modificar la API, conviene tener en cuenta:

1. Los nombres de campos provienen directamente de los DBF.
2. La búsqueda de socio por CUIT y por código debe mantenerse alineada en la estructura de respuesta.
3. Si agregás nuevas tablas DBF, asegurate de revisar que la codificación y el tipo de campo sean compatibles con `dbfread`.

## Soporte

La forma más rápida de validar cada cambio es levantar la API y probar los endpoints desde `/docs` o con `curl` / Postman.
