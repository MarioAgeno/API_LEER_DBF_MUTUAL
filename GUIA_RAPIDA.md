# 🚀 Guía Rápida de Uso - API Socios v2.0

## Inicio Rápido

### 1. Iniciar el API
```powershell
# Activar entorno virtual (si no está activado)
.\venv\Scripts\Activate.ps1

# Ejecutar el servidor
uvicorn main:app --reload
```

**Salida esperada:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 2. Acceder a la Documentación
Abre en tu navegador: **http://localhost:8000/docs**

---

## 📋 Nuevos Campos en Endpoints

### Endpoint 1: GET `/socio/{cuit}`
**URL:** `http://localhost:8000/socio/20123456789`

**Respuesta incluye:**
```json
{
  "Codigo": "1001",
  "Nombre": "Juan Perez",
  "...otros campos...",
  "Tramite DNI": "ABC123DEF456",
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  }
}
```

---

### Endpoint 2: GET `/sociocodigo/{codigo_socio}`
**URL:** `http://localhost:8000/sociocodigo/1001`

**Respuesta incluye:**
```json
{
  "Codigo": "1001",
  "Nombre": "Juan Perez",
  "...otros campos...",
  "Tramite DNI": "ABC123DEF456",
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  }
}
```

---

## 🧪 Probar los Nuevos Campos

### Opción 1: Script Automatizado (Recomendado)
```powershell
# Ejecutar pruebas
python test_socios.py
```

**Salida esperada:**
```
============================================================
TEST DE NUEVOS CAMPOS EN ENDPOINTS DE SOCIOS
============================================================

============================================================
Probando: GET /socio/20123456789
============================================================

✓ Respuesta exitosa (200)

Datos del Socio:
  • Código: 1001
  • Nombre: Juan Perez
  • CUIT: 20123456789
  • Número DNI: 12345678
  • Trámite DNI: ABC123DEF456

Datos de AgilPagos:
  • ID en AgilPagos: SGP001
  • ID Usuario: USR001
  • Cuenta en Mutual: 1001234567
  • Fecha de Alta: 2024-01-15
```

### Opción 2: Desde Swagger (Interfaz Web)
1. Abre: http://localhost:8000/docs
2. Busca `/socio/{cuit}` o `/sociocodigo/{codigo_socio}`
3. Click en "Try it out"
4. Ingresa un CUIT o código válido
5. Click en "Execute"
6. Ver la respuesta con los nuevos campos

### Opción 3: Con cURL
```bash
# Por CUIT
curl "http://localhost:8000/socio/20123456789"

# Por Código
curl "http://localhost:8000/sociocodigo/1001"
```

### Opción 4: Con Python/Requests
```python
import requests

# Consultar por CUIT
response = requests.get('http://localhost:8000/socio/20123456789')
data = response.json()

print(f"Trámite DNI: {data['Tramite DNI']}")
print(f"ID AgilPagos: {data['AgilPagos']['id_sg']}")

# Consultar por Código
response = requests.get('http://localhost:8000/sociocodigo/1001')
data = response.json()

print(f"Cuenta Mutual: {data['AgilPagos']['cuentamutu']}")
print(f"Fecha Alta: {data['AgilPagos']['alta']}")
```

---

## 📊 Interpretación de Datos

### Campo: `Tramite DNI`
- **¿Qué es?** Número de trámite del DNI del socio
- **¿Dónde viene?** De la tabla `Socios.dbf` campo `TRAMITEDNI`
- **¿Puede ser vacío?** Sí, si no está registrado
- **Ejemplo:** `"ABC123DEF456"` o `null`

### Campo: `AgilPagos` (Objeto)
- **¿Qué es?** Datos de integración con el sistema AgilPagos
- **¿Dónde viene?** De la tabla `sociosSG.dbf`
- **¿Puede estar vacío?** Sí, si no está registrado en AgilPagos
- **Subcampos:**
  - `id_sg`: ID único en AgilPagos
  - `id_user`: Usuario asociado en AgilPagos
  - `cuentamutu`: Número de cuenta en la mutual
  - `alta`: Fecha cuando se dio de alta en AgilPagos

---

## ⚠️ Casos Especiales

### Socio SIN datos en AgilPagos
Si el socio existe en `Socios.dbf` pero NO en `sociosSG.dbf`:
```json
{
  "Codigo": "1001",
  "Nombre": "Juan Perez",
  "...otros campos...",
  "Tramite DNI": "ABC123DEF456",
  "AgilPagos": {}
}
```

### Socio SIN Trámite DNI
Si no está registrado el campo `TRAMITEDNI`:
```json
{
  "Codigo": "1001",
  "Nombre": "Juan Perez",
  "...otros campos...",
  "Tramite DNI": null,
  "AgilPagos": {
    "id_sg": "SGP001",
    "id_user": "USR001",
    "cuentamutu": "1001234567",
    "alta": "2024-01-15"
  }
}
```

### Socio NO encontrado
```json
{
  "detail": "Socio no encontrado"
}
```

---

## 🔧 Requisitos DBF

La API espera los siguientes archivos DBF:

| Archivo | Uso | Campos Utilizados |
|---------|-----|-------------------|
| `Socios.dbf` | Datos del socio | CODIGO, CUIT, TRAMITEDNI, NOMBRE, etc. |
| `sociosSG.dbf` | Datos AgilPagos (OPCIONAL) | CODIGO, id_sg, id_user, cuentamutu, alta |

**Nota:** Si `sociosSG.dbf` no existe, el API sigue funcionando sin error.

---

## 🔄 Flujo de Consulta

```
1. Cliente solicita: GET /sociocodigo/1001
              ▼
2. API carga: Socios.dbf
              ▼
3. Busca socio con CODIGO = 1001
              ▼
4. Obtiene: Nombre, CUIT, TRAMITEDNI, etc.
              ▼
5. Intenta cargar: sociosSG.dbf
              ▼
6. Busca registro con CODIGO = 1001
              ▼
7. Si existe: Obtiene id_sg, id_user, cuentamutu, alta
   Si NO existe: Retorna {} vacío
              ▼
8. Retorna JSON con todos los datos
```

---

## 📚 Documentación Adicional

- **CAMBIOS.md** - Detalles técnicos de lo que cambió
- **EJEMPLO_RESPUESTA.md** - Más ejemplos de respuestas JSON
- **RESUMEN_ACTUALIZACION.md** - Resumen técnico completo
- **README.md** - Documentación del proyecto

---

## 🐛 Troubleshooting

### Problema: "Socio no encontrado" aunque existe
**Solución:** Verifica que el CUIT/Código sea correcto. El API normaliza números.

### Problema: `AgilPagos` siempre vacío
**Solución:** 
- Verifica que `sociosSG.dbf` existe en DBF_PATH
- Verifica que el socio está registrado en `sociosSG.dbf`
- Ejecuta: `python test_socios.py` para diagnosticar

### Problema: `Tramite DNI` siempre null
**Solución:** 
- Verifica que el campo `TRAMITEDNI` existe en `Socios.dbf`
- Verifica que el socio tiene valor en `TRAMITEDNI`

### Problema: Error de conexión
**Solución:** 
- Verifica que el API está corriendo: `uvicorn main:app --reload`
- Verifica que accedes a: `http://localhost:8000` (no 127.0.0.1:8000 desde otra máquina)
- Para red: usa la IP del servidor: `http://IP_SERVIDOR:8000`

---

## 📞 Contacto / Soporte

Si necesitas:
- Cambiar otros campos: ver `CAMBIOS.md`
- Ver ejemplo completo: ver `EJEMPLO_RESPUESTA.md`
- Detalles técnicos: ver `RESUMEN_ACTUALIZACION.md`

---

**Versión:** 2.0  
**Última actualización:** 2025-11-11
