# 🏦 Integración AgilPagos - Documentación Completa

## 📋 Descripción General

Se han agregado nuevos campos a los endpoints de consulta de socios para facilitar la integración con la billetera de AgilPagos del banco Coinag.

Todos los nuevos campos incluyen los `id_sg` (identificadores en AgilPagos) de las tablas relacionadas, permitiendo un mapeo directo con el sistema de AgilPagos.

---

## 🆕 Nuevos Campos Agregados

### Estructura Principal: `Datos_Integracion_AgilPagos`

```json
{
  "Datos_Integracion_AgilPagos": {
    "tipo_persona_id_sg": "...",
    "actividad_id_sg": "...",
    "estado_civil_id_sg": "...",
    "provincia_id_sg": "...",
    "pais_id_sg": "...",
    "situacion_iva_id_sg": "..."
  }
}
```

---

## 📊 Detalle de Cada Campo

### 1. **tipo_persona_id_sg** (Tipo de Persona)
| Propiedad | Valor |
|-----------|-------|
| Tabla Fuente | `UIFPersona.dbf` |
| Campo | `id_sg` |
| Relación | `UIFPersona.id = socios.TIPOPERS` |
| Tipo | String \| null |
| Descripción | Identifica si es persona física o jurídica en AgilPagos |
| Ejemplo | `"PER_FIS"`, `"PER_JUR"` |

**Cómo se obtiene:**
```
socios.TIPOPERS → UIFPersona.id → UIFPersona.id_sg
```

---

### 2. **actividad_id_sg** (Actividad Económica)
| Propiedad | Valor |
|-----------|-------|
| Tabla Fuente | `Actividad.dbf` |
| Campo | `id_sg` |
| Relación | `Actividad.CODIGO = socios.ACTIVIDAD` |
| Tipo | String \| null |
| Descripción | Código de actividad económica en AgilPagos |
| Ejemplo | `"ACT_0147"`, `"ACT_5020"` |

**Cómo se obtiene:**
```
socios.ACTIVIDAD → Actividad.CODIGO → Actividad.id_sg
```

---

### 3. **estado_civil_id_sg** (Estado Civil)
| Propiedad | Valor |
|-----------|-------|
| Tabla Fuente | `EstCivil.dbf` |
| Campo | `id_sg` |
| Relación | `EstCivil.id = socios.ESTCIVIL` |
| Tipo | String \| null |
| Descripción | Estado civil del socio en AgilPagos |
| Ejemplo | `"SOLT"`, `"CASA"`, `"DIVOR"` |

**Cómo se obtiene:**
```
socios.ESTCIVIL → EstCivil.id → EstCivil.id_sg
```

---

### 4. **provincia_id_sg** (Provincia/Localidad)
| Propiedad | Valor |
|-----------|-------|
| Tabla Fuente | `Provincias.dbf` |
| Campo | `id_sg` |
| Relación Compleja | Varias tablas relacionadas |
| Tipo | String \| null |
| Descripción | Provincia/localidad en AgilPagos |

**Cómo se obtiene (relación compleja):**
```
1. socios.CODPOSTAL 
   ↓
2. horasacr.CODIGO = socios.CODPOSTAL
   ↓
3. horasacr.inaescd (obtener valor)
   ↓
4. provincias.provincia = horasacr.inaescd
   ↓
5. provincias.id_sg (resultado final)
```

---

### 5. **pais_id_sg** (País)
| Propiedad | Valor |
|-----------|-------|
| Tabla Fuente | `Paises.dbf` |
| Campo | `id_sg` |
| Relación | `Paises.CODIGO = socios.PAIS` |
| Tipo | String \| null |
| Descripción | País del socio en AgilPagos |
| Ejemplo | `"AR"`, `"BR"`, `"UY"` |

**Cómo se obtiene:**
```
socios.PAIS → Paises.CODIGO → Paises.id_sg
```

---

### 6. **situacion_iva_id_sg** (Situación Fiscal/IVA)
| Propiedad | Valor |
|-----------|-------|
| Tabla Fuente | `CodIva.dbf` |
| Campo | `id_sg` |
| Relación | `CodIva.CODIGO = socios.SITIVA` |
| Tipo | String \| null |
| Descripción | Situación fiscal/IVA del socio en AgilPagos |
| Ejemplo | `"RI"`, `"MC"`, `"EX"` |

**Cómo se obtiene:**
```
socios.SITIVA → CodIva.CODIGO → CodIva.id_sg
```

---

## 📈 Ejemplo de Respuesta Completa

### GET `/sociocodigo/1001`

```json
{
  "Codigo": "1001",
  "Nombre": "Juan Carlos García López",
  "CUIT": "20123456789",
  "Numero Documento": "12345678",
  "Tramite DNI": "ABC123DEF456",
  "Domicilio": "Calle Principal 1234",
  "Codigo Postal": "1636",
  "Localidad": "San Isidro",
  "Estado Civil": "2",
  "Condicion Fiscal": "1",
  "Sujeto Obligado UIF": "No",
  "Residente": "Sí",
  "Fecha Nacimiento": "1980-05-15",
  "Fecha Ingreso": "2010-03-20",
  "Nacionalidad": "Argentina",
  "Telefono": "1123456789",
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
    "estado_civil_id_sg": "EC_CASADO",
    "provincia_id_sg": "PROV_BA",
    "pais_id_sg": "PAIS_AR",
    "situacion_iva_id_sg": "IVA_RI_001"
  }
}
```

---

## 🔗 Relaciones de Tablas - Diagrama

```
┌─────────────────────────────────────────────────────┐
│                    Socios.dbf                       │
│  (Tabla principal de socios)                        │
└─────────────────────────────────────────────────────┘
    │
    ├─→ TIPOPERS ──→ UIFPersona.dbf (id) ──→ UIFPersona.id_sg
    │                  [Tipo de Persona]
    │
    ├─→ ACTIVIDAD ──→ Actividad.dbf (CODIGO) ──→ Actividad.id_sg
    │                  [Actividad Económica]
    │
    ├─→ ESTCIVIL ──→ EstCivil.dbf (id) ──→ EstCivil.id_sg
    │                 [Estado Civil]
    │
    ├─→ CODPOSTAL ──→ horasacr.dbf (CODIGO) ──→ horasacr.inaescd
    │                 │                              │
    │                 └──→ provincias.dbf (provincia) ──→ provincias.id_sg
    │                      [Provincia]
    │
    ├─→ PAIS ──→ Paises.dbf (CODIGO) ──→ Paises.id_sg
    │             [País]
    │
    └─→ SITIVA ──→ CodIva.dbf (CODIGO) ──→ CodIva.id_sg
                   [Situación IVA]
```

---

## 📝 Funciones Implementadas

### 1. `get_tipo_persona_id_sg(tipopers)`
Obtiene el `id_sg` de `UIFPersona` para el tipo de persona.

**Parámetros:**
- `tipopers`: Valor de `socios.TIPOPERS`

**Retorna:**
- String con el `id_sg` o `None` si no existe

---

### 2. `get_actividad_id_sg(codigo_actividad)`
Obtiene el `id_sg` de `Actividad` para la actividad económica.

**Parámetros:**
- `codigo_actividad`: Valor de `socios.ACTIVIDAD`

**Retorna:**
- String con el `id_sg` o `None` si no existe

---

### 3. `get_estado_civil_id_sg(id_estcivil)`
Obtiene el `id_sg` de `EstCivil` para el estado civil.

**Parámetros:**
- `id_estcivil`: Valor de `socios.ESTCIVIL`

**Retorna:**
- String con el `id_sg` o `None` si no existe

---

### 4. `get_provincia_id_sg(codpostal)`
Obtiene el `id_sg` de `Provincias` usando la relación compleja con `horasacr`.

**Parámetros:**
- `codpostal`: Valor de `socios.CODPOSTAL`

**Proceso:**
1. Busca en `horasacr` donde `CODIGO = codpostal`
2. Obtiene `inaescd` de ese registro
3. Busca en `provincias` donde `provincia = inaescd`
4. Retorna `provincias.id_sg`

**Retorna:**
- String con el `id_sg` o `None` si no existe

---

### 5. `get_pais_id_sg(codigo_pais)`
Obtiene el `id_sg` de `Paises` para el país.

**Parámetros:**
- `codigo_pais`: Valor de `socios.PAIS`

**Retorna:**
- String con el `id_sg` o `None` si no existe

---

### 6. `get_situacion_iva_id_sg(codigo_iva)`
Obtiene el `id_sg` de `CodIva` para la situación fiscal.

**Parámetros:**
- `codigo_iva`: Valor de `socios.SITIVA`

**Retorna:**
- String con el `id_sg` o `None` si no existe

---

## 🧪 Cómo Probar

### Opción 1: Script Automatizado
```bash
python test_socios.py
```

### Opción 2: Swagger UI
```
http://localhost:8000/docs
→ GET /sociocodigo/{codigo_socio}
→ Ingresa un código válido
→ Ver respuesta con nuevo campo Datos_Integracion_AgilPagos
```

### Opción 3: cURL
```bash
curl "http://localhost:8000/sociocodigo/1001" | python -m json.tool
```

---

## ⚠️ Consideraciones Importantes

### Tablas Requeridas
| Tabla | Requerida | Descripción |
|-------|-----------|-------------|
| `UIFPersona.dbf` | Sí | Tipo de persona |
| `Actividad.dbf` | Sí | Actividades económicas |
| `EstCivil.dbf` | Sí | Estados civiles |
| `horasacr.dbf` | Sí | Relación para provincias |
| `provincias.dbf` | Sí | Provincias |
| `Paises.dbf` | Sí | Países |
| `CodIva.dbf` | Sí | Códigos de IVA |

### Si falta alguna tabla
- La API **NO** generará error
- El campo correspondiente será `null`
- El resto de la consulta funcionará normalmente

### Performance
- Las funciones usan `try/except` para manejar excepciones
- Si una tabla no existe, se captura gracefully
- No hay impacto significativo en la velocidad

---

## 🔄 Casos de Uso

### Caso 1: Integración con AgilPagos
```python
import requests

response = requests.get('http://localhost:8000/sociocodigo/1001')
data = response.json()

# Obtener datos para enviar a AgilPagos
agilpagos_data = {
    'tipo_persona': data['Datos_Integracion_AgilPagos']['tipo_persona_id_sg'],
    'actividad': data['Datos_Integracion_AgilPagos']['actividad_id_sg'],
    'estado_civil': data['Datos_Integracion_AgilPagos']['estado_civil_id_sg'],
    'provincia': data['Datos_Integracion_AgilPagos']['provincia_id_sg'],
    'pais': data['Datos_Integracion_AgilPagos']['pais_id_sg'],
    'situacion_iva': data['Datos_Integracion_AgilPagos']['situacion_iva_id_sg'],
}

# Enviar a AgilPagos
send_to_agilpagos(agilpagos_data)
```

### Caso 2: Verificar datos antes de enviar
```python
response = requests.get('http://localhost:8000/sociocodigo/1001')
data = response.json()

integracion = data['Datos_Integracion_AgilPagos']

# Validar que todos los campos necesarios existen
campos_requeridos = [
    'tipo_persona_id_sg',
    'actividad_id_sg',
    'estado_civil_id_sg',
    'provincia_id_sg',
    'pais_id_sg',
    'situacion_iva_id_sg'
]

for campo in campos_requeridos:
    if integracion[campo] is None:
        print(f"⚠️ Falta {campo} para {data['Nombre']}")
```

---

## 📞 Troubleshooting

### Problema: Campos siempre null
**Solución:** Verificar que las tablas DBF existen en DBF_PATH

### Problema: Valores inesperados
**Solución:** 
1. Verificar que los códigos en `Socios.dbf` coinciden
2. Revisar la estructura de las tablas relacionadas
3. Ejecutar `python test_socios.py` para diagnosticar

### Problema: Performance lento
**Solución:** Las búsquedas son lineales. Para mejorar se podría implementar caché (ver PROXIMAS_EXPANSIONES.md)

---

## 🔮 Próximas Mejoras

Ver [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) para:
- Implementar caché de búsquedas
- Agregar más campos de integración
- Exportar datos en formato AgilPagos
- Validación automática de datos

---

## 📋 Resumen de Cambios

| Elemento | Antes | Después |
|----------|-------|---------|
| Campos de integración | 1 (AgilPagos) | 7 (AgilPagos + 6 relacionales) |
| Funciones auxiliares | 1 | 7 |
| Tablas consultadas | 2 (Socios, sociosSG) | 9 (+ UIFPersona, Actividad, EstCivil, horasacr, provincias, Paises, CodIva) |
| Complejidad del mapeo | Baja | Alta (especialmente provincia) |
| Utilidad para AgilPagos | Parcial | Completa |

---

**Versión:** 2.1  
**Fecha:** 2025-11-11  
**Estado:** ✅ Completado y Testeado
