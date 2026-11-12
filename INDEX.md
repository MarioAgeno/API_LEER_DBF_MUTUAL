# 📑 ÍNDICE - API Socios v2.0

## 🎯 Comienza Aquí

**¿Nuevo en este proyecto?** → Lee primero: [GUIA_RAPIDA.md](GUIA_RAPIDA.md)

**¿Necesitas ver ejemplos?** → Consulta: [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md)

**¿Quieres probar?** → Ejecuta: `python test_socios.py`

---

## 📚 Documentación Disponible

### Para Usuarios Finales

| Documento | Contenido | Para Quién |
|-----------|----------|----------|
| [GUIA_RAPIDA.md](GUIA_RAPIDA.md) | Cómo usar los nuevos campos, ejemplos de consultas | Usuarios finales |
| [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md) | Ejemplos JSON completos de respuestas | Integradores |
| [README.md](README.md) | Documentación general del proyecto | Todos |

### Para Desarrolladores

| Documento | Contenido | Para Quién |
|-----------|----------|----------|
| [CAMBIOS.md](CAMBIOS.md) | Detalles técnicos de modificaciones | Desarrolladores |
| [RESUMEN_ACTUALIZACION.md](RESUMEN_ACTUALIZACION.md) | Resumen ejecutivo de cambios | Leads técnicos |
| [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) | Ideas para futuras mejoras | Architects |

### Para Operaciones

| Documento | Contenido | Para Quién |
|-----------|----------|----------|
| [CHECKLIST_VERIFICACION.md](CHECKLIST_VERIFICACION.md) | Validaciones pre/post lanzamiento | DevOps/QA |
| [test_socios.py](test_socios.py) | Script de pruebas automatizadas | QA/Testing |

---

## 🚀 Inicio Rápido

### 1. Iniciar el API (3 pasos)
```powershell
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
# Acceder a: http://localhost:8000/docs
```

### 2. Probar Nuevos Campos (2 pasos)
```powershell
python test_socios.py
# O acceder a: http://localhost:8000/docs y probar desde ahí
```

### 3. Ver Ejemplos (1 paso)
Abre [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md) en tu navegador o editor

---

## 🆕 ¿Qué es Nuevo?

### Nuevos Campos
1. **Tramite DNI** (string | null)
   - Número de trámite del DNI
   - Fuente: `Socios.dbf`

2. **AgilPagos** (object)
   - Datos de integración con AgilPagos
   - Fuente: `sociosSG.dbf`
   - Subcampos: `id_sg`, `id_user`, `cuentamutu`, `alta`

### Endpoints Afectados
- `GET /socio/{cuit}`
- `GET /sociocodigo/{codigo_socio}`

---

## 📊 Estructura de Datos

```json
{
  "Codigo": "1001",
  "Nombre": "Juan Perez",
  // ... otros campos existentes ...
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

## 🔗 Tabla de Relaciones

```
Socios.dbf (CODIGO)
    ↓
    ├─→ Campos: TRAMITEDNI, NOMBRE, CUIT, etc.
    │
    └─→ sociosSG.dbf (CODIGO)
        └─→ Campos: id_sg, id_user, cuentamutu, alta
```

---

## 🧪 Testing

### Opción 1: Script Automatizado
```bash
python test_socios.py
```
**Tiempo:** ~2 minutos | **Resultado:** Reporte completo

### Opción 2: Web UI (Swagger)
```
Acceder a: http://localhost:8000/docs
```
**Tiempo:** Instantáneo | **Resultado:** Interfaz interactiva

### Opción 3: cURL
```bash
curl "http://localhost:8000/sociocodigo/1001" | python -m json.tool
```
**Tiempo:** < 1 segundo | **Resultado:** JSON formateado

### Opción 4: Python
```python
import requests
response = requests.get('http://localhost:8000/sociocodigo/1001')
print(response.json())
```
**Tiempo:** < 1 segundo | **Resultado:** Objeto Python

---

## ❓ Preguntas Frecuentes

### P: ¿Cómo funciona si no existe sociosSG.dbf?
**R:** El API sigue funcionando normalmente. El campo `AgilPagos` será `{}`

### P: ¿Se rompió la compatibilidad con clientes antiguos?
**R:** No. Todos los campos antiguos permanecen. Solo se agregaron nuevos.

### P: ¿Qué hago si `Tramite DNI` es null?
**R:** Es normal si no está registrado en Socios.dbf. Algunos socios no tienen este dato.

### P: ¿Cómo agrego más campos de sociosSG?
**R:** Ver [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) - Sección 1

### P: ¿Necesito hacer cambios en mi código?
**R:** No es obligatorio. Los nuevos campos son opcionales. Pero es recomendable usarlos.

---

## 🛠️ Tareas Comunes

### Quiero integrar esto en mi aplicación
→ Lee [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Sección "Integración Frontend"

### Necesito exportar datos en CSV
→ Ver [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) - Sección 4

### Quiero agregar más campos
→ Ver [CAMBIOS.md](CAMBIOS.md) - Sección "Notas Técnicas"

### Necesito buscar socios
→ Ver [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) - Sección 3

### Tengo un problema
→ Ver [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Sección "Troubleshooting"

---

## 📈 Roadmap

### Ya Completado ✅
- [x] Agregar campo `Tramite DNI`
- [x] Integrar datos de `sociosSG.dbf`
- [x] Documentación completa
- [x] Script de pruebas
- [x] Ejemplos JSON

### Próximas Versiones 🔜
- [ ] Búsqueda flexible por nombre
- [ ] Exportar a CSV/Excel
- [ ] Caché de búsquedas
- [ ] Auditoría de consultas
- [ ] Más campos de sociosSG

Ver [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) para más detalles.

---

## 📞 Soporte

### Si tienes dudas sobre...

| Tema | Consulta |
|------|----------|
| Cómo usar los nuevos campos | [GUIA_RAPIDA.md](GUIA_RAPIDA.md) |
| Ejemplos de respuestas | [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md) |
| Detalles técnicos | [CAMBIOS.md](CAMBIOS.md) |
| Próximas mejoras | [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) |
| Validación antes de producción | [CHECKLIST_VERIFICACION.md](CHECKLIST_VERIFICACION.md) |
| Configuración general | [README.md](README.md) |

---

## 📋 Checklist Rápido

- [ ] He leído [GUIA_RAPIDA.md](GUIA_RAPIDA.md)
- [ ] He ejecutado `python test_socios.py`
- [ ] Entiendo los nuevos campos
- [ ] He visto ejemplos en [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md)
- [ ] Sé cómo integrar en mi aplicación
- [ ] Estoy listo para producción

---

## 🎓 Material Educativo

### Entender el API
1. [README.md](README.md) - Base
2. [GUIA_RAPIDA.md](GUIA_RAPIDA.md) - Concepto
3. [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md) - Práctica
4. `test_socios.py` - Validación

### Para Desarrolladores
1. [CAMBIOS.md](CAMBIOS.md) - Técnica
2. [RESUMEN_ACTUALIZACION.md](RESUMEN_ACTUALIZACION.md) - Arquitectura
3. [PROXIMAS_EXPANSIONES.md](PROXIMAS_EXPANSIONES.md) - Evolución

---

## 🔐 Validación

✅ **Código**
- Compilación sin errores
- Sintaxis Python válida
- Manejo de excepciones

✅ **Funcionalidad**
- Nuevos campos presentes
- Datos correctos
- Compatibilidad hacia atrás

✅ **Documentación**
- 6 archivos de documentación
- Ejemplos completos
- Guías claras

✅ **Testing**
- Script de pruebas
- Checklist de verificación
- Casos de uso

---

## 📆 Versionado

| Versión | Cambios | Fecha |
|---------|---------|-------|
| 1.0 | Versión inicial | 2025-xx-xx |
| 2.0 | Nuevos campos sociosSG + Tramite DNI | 2025-11-11 |
| TBD | Próximas expansiones | TBD |

---

## 🚀 Lanzamiento

**Estado:** ✅ Listo para Producción

**Checklist:**
- ✅ Código probado
- ✅ Documentación completa
- ✅ Ejemplos disponibles
- ✅ Script de pruebas
- ✅ Guía de implementación

**Para activar:**
1. Revisar [CHECKLIST_VERIFICACION.md](CHECKLIST_VERIFICACION.md)
2. Ejecutar `python test_socios.py`
3. Iniciar servicio: `uvicorn main:app --host 0.0.0.0 --port 8000`
4. Verificar: http://IP:8000/docs

---

**Última actualización:** 2025-11-11  
**Versión:** 2.0  
**Mantenedor:** Copilot

---

### ¿Por dónde empiezo?

**Opción A - Soy usuario:** [GUIA_RAPIDA.md](GUIA_RAPIDA.md)  
**Opción B - Soy desarrollador:** [CAMBIOS.md](CAMBIOS.md)  
**Opción C - Soy QA/DevOps:** [CHECKLIST_VERIFICACION.md](CHECKLIST_VERIFICACION.md)  
**Opción D - Necesito ejemplos:** [EJEMPLO_RESPUESTA.md](EJEMPLO_RESPUESTA.md)
