# 📊 Ejemplos de Respuesta - Integración AgilPagos v2.1

## Ejemplo Completo: Socio con Todos los Datos

### GET `/sociocodigo/1001`

```json
{
  "Codigo": "1001",
  "Nombre": "Juan Carlos García López",
  "Sucursal": "CENTRAL",
  "Sexo": "M",
  "Domicilio": "Calle Principal 1234",
  "Codigo Postal": "1636",
  "Localidad": "San Isidro",
  "CUIT": "20123456789",
  "Tipo Documento": "DNI",
  "Numero Documento": "12345678",
  "Tramite DNI": "ABC123DEF456",
  "Estado Civil": "2",
  "Condicion Fiscal": "1",
  "Sujeto Obligado UIF": "No",
  "Residente": "Sí",
  "Codigo Pais Extranjero": null,
  "Fecha Nacimiento": "1980-05-15",
  "Fecha Ingreso": "2010-03-20",
  "Es PEP": false,
  "Nacionalidad": "Argentina",
  "Telefono": "1123456789",
  "Telefono 2": null,
  "Movil": "1198765432",
  "e-Mail": "juan.garcia@email.com",
  "Codigo Actividad": "0147",
  
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  },
  
  "Datos_Integracion_AgilPagos": {
    "tipo_persona_id_sg": "PER_FIS_001",
    "actividad_id_sg": "ACT_0147_02",
    "estado_civil_id_sg": "EC_CASADO_002",
    "provincia_id_sg": "PROV_BA_001",
    "pais_id_sg": "PAIS_AR_001",
    "situacion_iva_id_sg": "IVA_RI_001"
  }
}
```

---

## Desglose de Campos de Integración

### 1. `tipo_persona_id_sg`
- **Valor:** `"PER_FIS_001"`
- **Significado:** Persona Física - Código 001 en AgilPagos
- **Fuente:** `UIFPersona.dbf`
- **Origen:** `socios.TIPOPERS` → `UIFPersona.id` → `UIFPersona.id_sg`

### 2. `actividad_id_sg`
- **Valor:** `"ACT_0147_02"`
- **Significado:** Actividad 0147 (Servicios Financieros) - Variante 02
- **Fuente:** `Actividad.dbf`
- **Origen:** `socios.ACTIVIDAD` → `Actividad.CODIGO` → `Actividad.id_sg`

### 3. `estado_civil_id_sg`
- **Valor:** `"EC_CASADO_002"`
- **Significado:** Estado Civil Casado - ID 002
- **Fuente:** `EstCivil.dbf`
- **Origen:** `socios.ESTCIVIL` → `EstCivil.id` → `EstCivil.id_sg`

### 4. `provincia_id_sg`
- **Valor:** `"PROV_BA_001"`
- **Significado:** Provincia Buenos Aires - ID 001
- **Fuente:** `Provincias.dbf` (vía `horasacr.dbf`)
- **Origen:** `socios.CODPOSTAL` → `horasacr.CODIGO` → `horasacr.inaescd` → `provincias.provincia` → `provincias.id_sg`
- **Relación:** Más compleja por pasar por tabla intermedia `horasacr`

### 5. `pais_id_sg`
- **Valor:** `"PAIS_AR_001"`
- **Significado:** País Argentina - ID 001
- **Fuente:** `Paises.dbf`
- **Origen:** `socios.PAIS` → `Paises.CODIGO` → `Paises.id_sg`

### 6. `situacion_iva_id_sg`
- **Valor:** `"IVA_RI_001"`
- **Significado:** Responsable Inscripto - ID 001
- **Fuente:** `CodIva.dbf`
- **Origen:** `socios.SITIVA` → `CodIva.CODIGO` → `CodIva.id_sg`

---

## Ejemplo 2: Socio con Datos Parciales

Si algún campo no existe en sus tablas relacionadas, aparecerá como `null`:

```json
{
  "Codigo": "2002",
  "Nombre": "María José Rodríguez",
  "...otros campos...",
  
  "AgilPagos": {},
  
  "Datos_Integracion_AgilPagos": {
    "tipo_persona_id_sg": "PER_FIS_001",
    "actividad_id_sg": null,
    "estado_civil_id_sg": "EC_SOLTERA_001",
    "provincia_id_sg": "PROV_CORDOBA_001",
    "pais_id_sg": "PAIS_AR_001",
    "situacion_iva_id_sg": "IVA_RI_001"
  }
}
```

**Nota:** `actividad_id_sg` es null porque la actividad (por ejemplo "9999") no existe en `Actividad.dbf`.

---

## Ejemplo 3: Socio Sin Datos AgilPagos

```json
{
  "Codigo": "3003",
  "Nombre": "Pedro López Martínez",
  "...otros campos...",
  
  "AgilPagos": {},
  
  "Datos_Integracion_AgilPagos": {
    "tipo_persona_id_sg": "PER_JUR_001",
    "actividad_id_sg": "ACT_5020_01",
    "estado_civil_id_sg": null,
    "provincia_id_sg": "PROV_SANTA_FE_001",
    "pais_id_sg": "PAIS_AR_001",
    "situacion_iva_id_sg": "IVA_MC_001"
  }
}
```

**Nota:** `AgilPagos` está vacío porque no hay registro en `sociosSG.dbf`.

---

## Ejemplo 4: Búsqueda por CUIT

### GET `/socio/20123456789`

Retorna la misma estructura que `/sociocodigo/{codigo}`:

```json
{
  "Codigo": "1001",
  "Nombre": "Juan Carlos García López",
  "CUIT": "20123456789",
  "...todos los datos del socio...",
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  },
  "Datos_Integracion_AgilPagos": {
    "tipo_persona_id_sg": "PER_FIS_001",
    "actividad_id_sg": "ACT_0147_02",
    "estado_civil_id_sg": "EC_CASADO_002",
    "provincia_id_sg": "PROV_BA_001",
    "pais_id_sg": "PAIS_AR_001",
    "situacion_iva_id_sg": "IVA_RI_001"
  }
}
```

---

## Ejemplo 5: Respuesta 404 - Socio no encontrado

### GET `/sociocodigo/9999` (no existe)

```json
{
  "detail": "Socio no encontrado"
}
```

HTTP Status: **404 Not Found**

---

## Estructura de Datos Completa

```
Socio (datos personales)
  │
  ├─ Datos básicos
  │  ├─ Codigo
  │  ├─ Nombre
  │  ├─ CUIT
  │  ├─ Domicilio
  │  └─ ... otros campos
  │
  ├─ AgilPagos (cuenta en AgilPagos)
  │  ├─ id_sg
  │  ├─ id_user
  │  ├─ cuentamutu
  │  └─ alta
  │
  └─ Datos_Integracion_AgilPagos (catálogos para sincronizar)
     ├─ tipo_persona_id_sg (UIFPersona)
     ├─ actividad_id_sg (Actividad)
     ├─ estado_civil_id_sg (EstCivil)
     ├─ provincia_id_sg (Provincias)
     ├─ pais_id_sg (Paises)
     └─ situacion_iva_id_sg (CodIva)
```

---

## Cómo Integrar con AgilPagos

### Paso 1: Obtener datos del socio
```python
import requests

response = requests.get('http://localhost:8000/sociocodigo/1001')
socio = response.json()
```

### Paso 2: Extraer datos para AgilPagos
```python
integracion = socio['Datos_Integracion_AgilPagos']

payload_agilpagos = {
    # Datos personales
    'nombre': socio['Nombre'],
    'cuit': socio['CUIT'],
    'email': socio['e-Mail'],
    'telefono': socio['Telefono'],
    'domicilio': socio['Domicilio'],
    
    # Catálogos
    'tipo_persona': integracion['tipo_persona_id_sg'],
    'actividad': integracion['actividad_id_sg'],
    'estado_civil': integracion['estado_civil_id_sg'],
    'provincia': integracion['provincia_id_sg'],
    'pais': integracion['pais_id_sg'],
    'situacion_iva': integracion['situacion_iva_id_sg'],
    
    # Datos AgilPagos
    'id_agilpagos': socio['AgilPagos']['id_sg'] if socio['AgilPagos'] else None
}
```

### Paso 3: Enviar a AgilPagos
```python
# Validar que todos los campos estén presente
if all(payload_agilpagos.values()):
    response = requests.post(
        'https://api.agilpagos.com/v1/socios',
        json=payload_agilpagos,
        headers={'Authorization': 'Bearer TOKEN'}
    )
    print(response.json())
else:
    print("Error: Faltan datos para enviar a AgilPagos")
```

---

## Validación de Datos

### Campos Requeridos para AgilPagos
```python
campos_requeridos = {
    'tipo_persona_id_sg': 'Tipo de Persona',
    'actividad_id_sg': 'Actividad Económica',
    'estado_civil_id_sg': 'Estado Civil',
    'provincia_id_sg': 'Provincia',
    'pais_id_sg': 'País',
    'situacion_iva_id_sg': 'Situación IVA'
}

integracion = socio['Datos_Integracion_AgilPagos']
errores = []

for campo, nombre in campos_requeridos.items():
    if integracion.get(campo) is None:
        errores.append(f"Falta {nombre} ({campo})")

if errores:
    print("Errores encontrados:")
    for error in errores:
        print(f"  - {error}")
else:
    print("✓ Todos los datos están presentes. Listo para AgilPagos")
```

---

## Tipos de Respuesta Posibles

### 200 OK - Socio encontrado con todos los datos
```json
{
  "Codigo": "1001",
  "Nombre": "...",
  "AgilPagos": { ... },
  "Datos_Integracion_AgilPagos": { ... }
}
```

### 200 OK - Socio encontrado con datos parciales
```json
{
  "Codigo": "2002",
  "Nombre": "...",
  "AgilPagos": {},
  "Datos_Integracion_AgilPagos": {
    "tipo_persona_id_sg": "...",
    "actividad_id_sg": null,
    "estado_civil_id_sg": "...",
    ...
  }
}
```

### 404 Not Found - Socio no existe
```json
{
  "detail": "Socio no encontrado"
}
```

---

## Casos Especiales

### Caso 1: Relación Compleja - Provincia
La provincia tiene una relación compleja a través de `horasacr`:

```
CODPOSTAL (ej: 1636)
    ↓
horasacr.CODIGO = 1636
    ↓
horasacr.inaescd = "06" (ejemplo)
    ↓
provincias.provincia = "06"
    ↓
provincias.id_sg = "PROV_BA_001"
```

**Nota:** Si algún paso falla, el resultado será `null`.

### Caso 2: Campo PAIS Faltante
Si `socios.PAIS` no tiene valor, `pais_id_sg` será `null`:

```python
if integracion['pais_id_sg'] is None:
    print("⚠️ Advertencia: País no está configurado en el sistema")
    # Usar valor por defecto de Argentina
    pais = "PAIS_AR_001"
```

---

**Versión:** 2.1  
**Fecha:** 2025-11-11  
**Última actualización:** Con integración completa de AgilPagos
