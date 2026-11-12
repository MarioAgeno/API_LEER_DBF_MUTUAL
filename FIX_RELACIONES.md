# Fix de Relaciones AgilPagos - v2.1.1

## Problema Identificado

Las funciones helper para obtener los `id_sg` estaban retornando `null` aunque los datos existían en las tablas DBF. El problema era debido a:

1. **Nombres de campos incorrectos**: El código usaba `id_sg` (minúsculas) cuando en DBF están como `ID_SG` (mayúsculas)
2. **Nombres de tablas incorrectos**: El código usaba nombres en mixto case (UIFPersona.dbf) cuando en DBF están en mayusculas (UIFPERSONA.DBF)
3. **Nombres de campos específicos**: En algunas tablas, los nombres de campos eran diferentes a los esperados

## Cambios Realizados

### Correcciones en main.py (líneas 83-177)

#### get_tipo_persona_id_sg()
**Antes:**
```python
uif_persona = load_dbf('UIFPersona.dbf')
for registro in uif_persona:
    if ids_match(registro.get('id'), tipopers):
        return registro.get('id_sg')
```

**Después:**
```python
uif_persona = load_dbf('UIFPERSONA.dbf')
for registro in uif_persona:
    if ids_match(registro.get('ID'), tipopers):
        return registro.get('ID_SG')
```

**Cambios:**
- `UIFPersona.dbf` → `UIFPERSONA.dbf` (nombre de tabla)
- `.get('id')` → `.get('ID')` (nombre de campo)
- `.get('id_sg')` → `.get('ID_SG')` (nombre de campo)

#### get_actividad_id_sg()
**Antes:**
```python
actividades = load_dbf('Actividad.dbf')
for registro in actividades:
    if ids_match(registro.get('CODIGO'), codigo_actividad):
        return registro.get('id_sg')
```

**Después:**
```python
actividades = load_dbf('ACTIVIDA.dbf')
for registro in actividades:
    if ids_match(registro.get('CODIGO'), codigo_actividad):
        return registro.get('ID_SG')
```

**Cambios:**
- `Actividad.dbf` → `ACTIVIDA.dbf` (nombre exacto en el sistema)
- `.get('id_sg')` → `.get('ID_SG')` (nombre de campo)

#### get_estado_civil_id_sg()
**Antes:**
```python
estcivil = load_dbf('EstCivil.dbf')
for registro in estcivil:
    if ids_match(registro.get('id'), id_estcivil):
        return registro.get('id_sg')
```

**Después:**
```python
estcivil = load_dbf('ESTCIVIL.dbf')
for registro in estcivil:
    if ids_match(registro.get('CODIGO'), id_estcivil):
        return registro.get('ID_SG')
```

**Cambios:**
- `EstCivil.dbf` → `ESTCIVIL.dbf` (nombre de tabla)
- `.get('id')` → `.get('CODIGO')` (El campo es CODIGO, no id)
- `.get('id_sg')` → `.get('ID_SG')` (nombre de campo)

#### get_provincia_id_sg()
**Antes:**
```python
horasacr = load_dbf('horasacr.dbf')
provincias = load_dbf('provincias.dbf')

for reg_horasacr in horasacr:
    if ids_match(reg_horasacr.get('CODIGO'), codpostal):
        inaescd = reg_horasacr.get('inaescd')  # Error aqui
        for reg_provincia in provincias:
            if ids_match(reg_provincia.get('provincia'), inaescd):
                return reg_provincia.get('id_sg')
```

**Después:**
```python
horasacr = load_dbf('HORASACR.dbf')
provincias = load_dbf('PROVINCIAS.dbf')

for reg_horasacr in horasacr:
    if ids_match(reg_horasacr.get('CODIGO'), codpostal):
        inaescd = reg_horasacr.get('INAESCD')  # Correcto: mayusculas
        for reg_provincia in provincias:
            if ids_match(reg_provincia.get('PROVINCIA'), inaescd):  # Correcto
                return reg_provincia.get('ID_SG')  # Correcto
```

**Cambios:**
- `horasacr.dbf` → `HORASACR.dbf` (nombre de tabla)
- `provincias.dbf` → `PROVINCIAS.dbf` (nombre de tabla)
- `.get('inaescd')` → `.get('INAESCD')` (nombre de campo)
- `.get('provincia')` → `.get('PROVINCIA')` (nombre de campo)
- `.get('id_sg')` → `.get('ID_SG')` (nombre de campo)

#### get_pais_id_sg()
**Antes:**
```python
paises = load_dbf('Paises.dbf')
for registro in paises:
    if ids_match(registro.get('CODIGO'), codigo_pais):
        return registro.get('id_sg')
```

**Después:**
```python
paises = load_dbf('PAISES.dbf')
for registro in paises:
    if ids_match(registro.get('CODIGO'), codigo_pais):
        return registro.get('ID_SG')
```

**Cambios:**
- `Paises.dbf` → `PAISES.dbf` (nombre de tabla)
- `.get('id_sg')` → `.get('ID_SG')` (nombre de campo)

#### get_situacion_iva_id_sg()
**Antes:**
```python
codiva = load_dbf('CodIva.dbf')
for registro in codiva:
    if ids_match(registro.get('CODIGO'), codigo_iva):
        return registro.get('id_sg')
```

**Después:**
```python
codiva = load_dbf('CODIVA.dbf')
for registro in codiva:
    if ids_match(registro.get('CODIGO'), codigo_iva):
        return registro.get('ID_SG')
```

**Cambios:**
- `CodIva.dbf` → `CODIVA.dbf` (nombre de tabla)
- `.get('id_sg')` → `.get('ID_SG')` (nombre de campo)

## Verificación

Se crearon dos scripts de prueba para verificar las correcciones:

### test_relaciones_1179.py
Script standalone que verifica todas las 6 relaciones usando socio 1179.

**Resultado:**
```
[1] get_tipo_persona_id_sg(1)
    Resultado: 20EB9127-7CA8-49E0-9E0B-CA8293218ACA ✓

[2] get_actividad_id_sg(7)
    Resultado: 6864846e-a7e2-4c37-9c88-e81103e3c971 ✓

[3] get_estado_civil_id_sg('C')
    Resultado: 13e36b73-183f-4575-8d18-5c94543d2e07 ✓

[4] get_provincia_id_sg(3040)
    Resultado: dc2f0d87-118e-418c-b1c7-2bdbe5dffbec ✓

[5] get_pais_id_sg('ARG')
    Resultado: 76b19e61-b8dc-40f4-bfab-422cbffe5002 ✓

[6] get_situacion_iva_id_sg('RI')
    Resultado: f0ea813a-e3e7-4eae-ba1d-02b3917ca59a ✓

OK - TODAS LAS RELACIONES FUNCIONANDO CORRECTAMENTE
```

### test_api_1179.py
Script que prueba el endpoint `/sociocodigo/1179` completo.

**Resultado:**
```json
{
  "Datos_Integracion_AgilPagos": {
    "tipo_persona_id_sg": "20EB9127-7CA8-49E0-9E0B-CA8293218ACA",
    "actividad_id_sg": "6864846e-a7e2-4c37-9c88-e81103e3c971",
    "estado_civil_id_sg": "13e36b73-183f-4575-8d18-5c94543d2e07",
    "provincia_id_sg": "dc2f0d87-118e-418c-b1c7-2bdbe5dffbec",
    "pais_id_sg": "76b19e61-b8dc-40f4-bfab-422cbffe5002",
    "situacion_iva_id_sg": "f0ea813a-e3e7-4eae-ba1d-02b3917ca59a"
  }
}

OK - TODOS LOS CAMPOS TIENEN VALORES
```

## Resumen

| Campo | Antes | Después | Estado |
|-------|-------|---------|--------|
| tipo_persona_id_sg | null | ✓ UUID | FIJO |
| actividad_id_sg | null | ✓ UUID | FIJO |
| estado_civil_id_sg | null | ✓ UUID | FIJO |
| provincia_id_sg | null | ✓ UUID | FIJO |
| pais_id_sg | null | ✓ UUID | FIJO |
| situacion_iva_id_sg | null | ✓ UUID | FIJO |

## Lecciones Aprendidas

1. **Case Sensitivity**: Los nombres de campos en DBF son SENSIBLES a mayúsculas/minúsculas
2. **Nombres de archivos**: Los archivos .dbf pueden tener nombres diferentes a lo esperado (ACTIVIDA vs Actividad)
3. **Importance of Testing**: La prueba manual con datos reales (socio 1179) fue crítica para identificar el problema

## Archivos Afectados

- `main.py` - Funciones helper corregidas (líneas 83-177)
- `test_relaciones_1179.py` - Script de prueba (nuevo)
- `test_api_1179.py` - Script de prueba del API (nuevo)

## Versión

Esta es v2.1.1 - Fix de relaciones que estaban retornando null

## Próximos Pasos

1. ✓ Verificar con datos reales (completado con socio 1179)
2. ✓ Actualizar main.py con nombres correctos (completado)
3. Actualizar documentación (AGILPAGOS_INTEGRACION.md, etc.) con nombres correctos de tablas y campos
4. Considerar hacer las pruebas test_relaciones_1179.py y test_api_1179.py parte de la suite de tests automáticos

---

**Fecha del fix:** 2024-11-11
**Commit:** ef39190
**Status:** Listo para producción
