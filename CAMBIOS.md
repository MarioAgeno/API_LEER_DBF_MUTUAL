# Cambios Realizados en la API - Socios

## Resumen
Se agregaron nuevos campos y funcionalidades a los endpoints de consulta de socios para incluir información del trámite de DNI y datos de AgilPagos desde la tabla `sociosSG`.

## Cambios Específicos

### 1. Nueva Función: `get_socio_sg_data(codigo)`
- **Ubicación**: Antes de la función `get_socio_by_cuit`
- **Descripción**: Obtiene datos de AgilPagos relacionados con un socio desde la tabla `sociosSG`
- **Parámetro**: `codigo` - Código único del socio
- **Retorna**: Diccionario con los siguientes campos:
  - `id_sg`: ID en AgilPagos
  - `id_user`: ID de usuario en AgilPagos
  - `cuentamutu`: Cuenta del socio en la mutual
  - `alta`: Fecha de alta del socio en AgilPagos

### 2. Actualización: Función `get_socio_by_cuit(cuit)`
**Campos Nuevos Agregados:**
- `Tramite DNI`: Número de trámite del DNI (campo: `TRAMITEDNI`)
- `AgilPagos`: Objeto con datos relacionados de la tabla `sociosSG`
  - Contiene: `id_sg`, `id_user`, `cuentamutu`, `alta`

**Ejemplo de respuesta:**
```json
{
  "Codigo": "12345",
  "Nombre": "Juan Perez",
  "...": "...",
  "Tramite DNI": "1234567890",
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  }
}
```

### 3. Actualización: Función `get_socio_by_codigo(codigo_socio)`
**Campos Nuevos Agregados:**
- `Tramite DNI`: Número de trámite del DNI (campo: `TRAMITEDNI`)
- `AgilPagos`: Objeto con datos relacionados de la tabla `sociosSG`

**Ejemplo de respuesta:**
```json
{
  "Codigo": "12345",
  "Nombre": "Juan Perez",
  "...": "...",
  "Tramite DNI": "1234567890",
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  }
}
```

## Endpoints Afectados

1. **GET `/socio/{cuit}`**
   - Ahora retorna datos de AgilPagos y número de trámite de DNI
   
2. **GET `/sociocodigo/{codigo_socio}`**
   - Ahora retorna datos de AgilPagos y número de trámite de DNI

## Tablas Utilizadas

- **Socios.dbf**: Tabla principal de socios (contiene `TRAMITEDNI`)
- **sociosSG.dbf**: Tabla de relación con AgilPagos (relacionada por campo `CODIGO`)

## Notas Técnicas

- La función `get_socio_sg_data()` maneja excepciones gracefully si la tabla `sociosSG` no existe
- Si no hay datos en `sociosSG` para un socio, retorna un objeto vacío `{}`
- La búsqueda en `sociosSG` usa la función `ids_match()` para normalizar IDs
- Se preserva la compatibilidad hacia atrás; si no existe `sociosSG`, el campo `AgilPagos` será vacío

## Validación

El código ha sido compilado y validado sin errores de sintaxis.
