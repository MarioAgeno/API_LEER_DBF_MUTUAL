# 🔮 Próximas Expansiones Sugeridas

## Expansiones Recomendadas

### 1. Agregar Más Campos de sociosSG
**Estado:** Fácil | **Impacto:** Alto | **Tiempo:** 5 min

Actualmente se traen: `id_sg`, `id_user`, `cuentamutu`, `alta`

**Posibles campos adicionales:**
- Estado del socio en AgilPagos
- Última actividad
- Saldo disponible
- Crédito pre-aprobado
- Datos de contacto alternativos

**Implementación:**
1. Ver qué campos tiene `sociosSG.dbf`
2. En función `get_socio_sg_data()` agregar los campos deseados
3. Actualizar diccionario de retorno

**Ejemplo:**
```python
def get_socio_sg_data(codigo):
    try:
        sociosSG = load_dbf('sociosSG.dbf')
        for registro in sociosSG:
            if ids_match(registro.get('CODIGO'), codigo):
                return {
                    'id_sg': registro.get('id_sg'),
                    'id_user': registro.get('id_user'),
                    'cuentamutu': registro.get('cuentamutu'),
                    'alta': registro.get('alta'),
                    'estado': registro.get('estado'),  # NUEVO
                    'credito_disponible': registro.get('credito_disponible')  # NUEVO
                }
    except Exception:
        pass
    return None
```

---

### 2. Nuevo Endpoint: GET `/socio/detalles/{codigo}`
**Estado:** Moderado | **Impacto:** Alto | **Tiempo:** 10 min

Endpoint consolidado que retorna toda la información disponible de un socio:

**Características:**
- Datos básicos de `Socios.dbf`
- Datos de `sociosSG.dbf`
- Últimos préstamos
- Saldo de cuotas pendientes
- Estado de cuenta

**Ejemplo de Implementación:**
```python
@app.get("/socio/detalles/{codigo_socio}")
def obtener_socio_detalles(codigo_socio: str):
    socio = get_socio_by_codigo(codigo_socio)
    if not socio:
        raise HTTPException(status_code=404, detail="Socio no encontrado")
    
    # Agregar datos adicionales
    prestamos = get_prestamos_by_socio(codigo_socio)
    cuotas = get_cuotas_sociales_pendientes(codigo_socio)
    
    return {
        **socio,  # Todos los datos de socio
        'prestamos_activos': prestamos[:3],  # Últimos 3
        'cuotas_pendientes': cuotas
    }
```

---

### 3. Búsqueda Flexible: GET `/buscar/socio`
**Estado:** Moderado | **Impacto:** Alto | **Tiempo:** 15 min

Endpoint con parámetros de búsqueda para filtrar socios:

**Parámetros opcionales:**
- `nombre` - Búsqueda por nombre (parcial)
- `cuit` - Búsqueda exacta
- `codigo` - Búsqueda exacta
- `localidad` - Búsqueda por localidad
- `limite` - Máximo de resultados (default 10)

**URL de Ejemplo:**
```
GET /buscar/socio?nombre=juan&localidad=san%20isidro&limite=5
```

**Implementación:**
```python
@app.get("/buscar/socio")
def buscar_socios(nombre: str = None, cuit: str = None, 
                  codigo: str = None, localidad: str = None, 
                  limite: int = 10):
    socios = load_dbf('Socios.dbf')
    resultados = []
    
    for socio in socios:
        if nombre and nombre.lower() not in socio['NOMBRE'].lower():
            continue
        if cuit and not ids_match(socio['CUIT'], cuit):
            continue
        if codigo and not ids_match(socio['CODIGO'], codigo):
            continue
        if localidad and localidad.lower() not in socio['LOCALI'].lower():
            continue
        
        resultados.append(get_socio_by_codigo(socio['CODIGO']))
        if len(resultados) >= limite:
            break
    
    return resultados if resultados else {"detalle": "No se encontraron socios"}
```

---

### 4. Exportar Datos: GET `/export/socios/{formato}`
**Estado:** Fácil | **Impacto:** Medio | **Tiempo:** 20 min

Exportar lista de socios en diferentes formatos:

**Formatos soportados:**
- `csv` - Valores separados por comas
- `json` - Formato JSON
- `xml` - Formato XML

**URL de Ejemplo:**
```
GET /export/socios/csv
GET /export/socios/json?filtro=activos
```

**Librería recomendada:**
```bash
pip install pandas openpyxl
```

---

### 5. Caché de Búsquedas
**Estado:** Avanzado | **Impacto:** Alto | **Tiempo:** 30 min

Implementar caché para acelerar búsquedas frecuentes:

```python
from functools import lru_cache
import time

# Cache con expiración
class CacheConExpiracion:
    def __init__(self, expiracion_segundos=300):
        self.cache = {}
        self.expiracion = expiracion_segundos
    
    def get(self, key):
        if key in self.cache:
            valor, timestamp = self.cache[key]
            if time.time() - timestamp < self.expiracion:
                return valor
            else:
                del self.cache[key]
        return None
    
    def set(self, key, valor):
        self.cache[key] = (valor, time.time())

cache = CacheConExpiracion()

@app.get("/sociocodigo/{codigo_socio}")
def socio_por_codigo(codigo_socio: str):
    # Revisar cache
    cached = cache.get(f"socio_{codigo_socio}")
    if cached:
        return cached
    
    # Si no está en cache, consultar
    socio = get_socio_by_codigo(codigo_socio)
    if socio:
        cache.set(f"socio_{codigo_socio}", socio)
        return socio
    
    raise HTTPException(status_code=404, detail="Socio no encontrado")
```

---

### 6. Validación y Auditoría
**Estado:** Moderado | **Impacto:** Medio | **Tiempo:** 25 min

Registrar todas las consultas para auditoría:

```python
import logging
from datetime import datetime

# Configurar logging
logging.basicConfig(filename='api_audit.log', level=logging.INFO)

def log_consulta(endpoint, parametro, resultado, ip_cliente):
    logging.info(f"{datetime.now()} | {ip_cliente} | {endpoint} | {parametro} | {resultado}")

@app.get("/sociocodigo/{codigo_socio}")
def socio_por_codigo(codigo_socio: str, request):
    try:
        socio = get_socio_by_codigo(codigo_socio)
        log_consulta("/sociocodigo", codigo_socio, "SUCCESS", request.client.host)
        if socio:
            return socio
        else:
            log_consulta("/sociocodigo", codigo_socio, "NOT_FOUND", request.client.host)
            raise HTTPException(status_code=404, detail="Socio no encontrado")
    except Exception as e:
        log_consulta("/sociocodigo", codigo_socio, "ERROR", request.client.host)
        raise
```

---

### 7. Documentación Interactiva
**Estado:** Fácil | **Impacto:** Bajo | **Tiempo:** 10 min

Mejorar la documentación en Swagger:

```python
@app.get("/socio/{cuit}", tags=["Socios"], summary="Obtener socio por CUIT")
def obtener_socio(
    cuit: int = Query(..., description="CUIT del socio (ej: 20123456789)")
):
    """
    Obtiene los datos de un socio consultando por su CUIT.
    
    ## Parámetros
    - **cuit**: CUIT del socio (número de 11 dígitos)
    
    ## Respuesta exitosa (200)
    Retorna objeto con todos los datos del socio incluyendo:
    - Datos personales
    - Documento
    - Contacto
    - Información AgilPagos
    - Trámite de DNI
    
    ## Errores posibles
    - **404**: Socio no encontrado
    - **500**: Error interno del servidor
    
    ## Ejemplo de uso
    ```
    GET /socio/20123456789
    ```
    """
    # ... implementación ...
```

---

### 8. Relaciones con Otros Datos
**Estado:** Avanzado | **Impacto:** Alto | **Tiempo:** 45 min

Expandir las relaciones entre tablas:

**Posibles relaciones:**
- Socio → Cuentas Bancarias
- Socio → Tarjetas de Crédito
- Socio → Seguros
- Socio → Garantías
- Socio → Documentos

**Ejemplo:**
```python
def get_socio_completo(codigo_socio):
    socio = get_socio_by_codigo(codigo_socio)
    if not socio:
        return None
    
    return {
        **socio,
        'cuentas': get_cuentas_socio(codigo_socio),
        'tarjetas': get_tarjetas_socio(codigo_socio),
        'prestamos': get_prestamos_by_socio(codigo_socio),
        'seguros': get_seguros_socio(codigo_socio)
    }
```

---

## 📋 Plan de Expansión Sugerido

### Fase 1: Corto Plazo (1-2 semanas)
1. ✅ Agregar más campos de sociosSG
2. ✅ Nuevo endpoint `/socio/detalles/{codigo}`
3. ✅ Búsqueda flexible

### Fase 2: Mediano Plazo (2-4 semanas)
4. Exportar datos en múltiples formatos
5. Implementar caché
6. Mejorar documentación

### Fase 3: Largo Plazo (1-2 meses)
7. Auditoría y logging
8. Relaciones con otras tablas
9. Panel de estadísticas

---

## 🛠️ Herramientas Recomendadas

```bash
# Para exportar datos
pip install pandas openpyxl

# Para búsqueda avanzada
pip install elasticsearch

# Para caché distribuido
pip install redis

# Para logging y monitoreo
pip install python-json-logger

# Para tests
pip install pytest pytest-asyncio httpx
```

---

## 📊 Estimación de Esfuerzo

| Expansión | Dificultad | Horas | Prioridad |
|-----------|-----------|-------|-----------|
| Más campos sociosSG | Fácil | 0.5 | 🔴 Alta |
| Endpoint detalles | Moderado | 1 | 🟠 Alta |
| Búsqueda flexible | Moderado | 1.5 | 🟠 Alta |
| Exportar datos | Fácil | 2 | 🟡 Media |
| Caché | Avanzado | 3 | 🟡 Media |
| Auditoría | Moderado | 2 | 🟢 Baja |
| Documentación | Fácil | 1 | 🟢 Baja |
| Relaciones | Avanzado | 4 | 🔴 Alta |

---

## 🎯 Próximas Funciones por Demanda

**¿Necesitas agregar campos a otro endpoint?**
El patrón es similar al de `sociosSG`. Contáctame y lo hacemos rápido.

**¿Necesitas un endpoint completamente nuevo?**
Define qué datos necesitas y de qué tablas DBF vienen.

**¿Necesitas exportar datos?**
Podemos agregar exportación a CSV, Excel, PDF, etc.

---

**Actualizado:** 2025-11-11  
**Versión API:** 2.0
