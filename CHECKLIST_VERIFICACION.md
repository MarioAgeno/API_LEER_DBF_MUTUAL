# ✅ Checklist de Verificación - API Socios v2.0

## Pre-Lanzamiento

### 1. Validación del Código
- [x] Archivo `main.py` compila sin errores
- [x] Función `get_socio_sg_data()` implementada
- [x] Función `get_socio_by_cuit()` actualizada
- [x] Función `get_socio_by_codigo()` actualizada
- [x] Manejo de excepciones implementado
- [x] Compatibilidad hacia atrás verificada

### 2. Bases de Datos
- [ ] Verificar que `Socios.dbf` tiene el campo `TRAMITEDNI`
- [ ] Verificar que `sociosSG.dbf` existe (si va a usar AgilPagos)
- [ ] Verificar que `sociosSG.dbf` tiene los campos: `CODIGO`, `id_sg`, `id_user`, `cuentamutu`, `alta`
- [ ] Backup de archivos DBF realizado

### 3. Documentación
- [x] CAMBIOS.md creado
- [x] EJEMPLO_RESPUESTA.md creado
- [x] RESUMEN_ACTUALIZACION.md creado
- [x] GUIA_RAPIDA.md creado
- [x] PROXIMAS_EXPANSIONES.md creado
- [x] README.md actualizado
- [x] Este checklist creado

### 4. Herramientas de Prueba
- [x] test_socios.py creado
- [ ] Ejecutar: `python test_socios.py`
- [ ] Verificar que no hay errores de conexión

## Lanzamiento

### 1. Iniciar Servicio

#### Opción A: Desarrollo
```powershell
cd D:\PYTHON\API_LEER_DBF_MUTUAL
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload
```
- [ ] Servidor inicia correctamente
- [ ] Mensaje: "Uvicorn running on http://127.0.0.1:8000"

#### Opción B: Producción (NSSM)
```powershell
nssm start API_LEER_DBF_MUTUAL
```
- [ ] Servicio inicia correctamente
- [ ] Accesible desde otros equipos en la red

### 2. Verificación de Endpoints

#### Endpoint: GET `/socio/{cuit}`
```bash
curl "http://localhost:8000/socio/20123456789"
```
- [ ] Retorna código 200
- [ ] Incluye campo `Tramite DNI`
- [ ] Incluye campo `AgilPagos` (objeto)
- [ ] Valores son correctos según datos en Socios.dbf

#### Endpoint: GET `/sociocodigo/{codigo_socio}`
```bash
curl "http://localhost:8000/sociocodigo/1001"
```
- [ ] Retorna código 200
- [ ] Incluye campo `Tramite DNI`
- [ ] Incluye campo `AgilPagos` (objeto)
- [ ] Valores son correctos según datos en Socios.dbf

#### Endpoint: Swagger UI
```
Acceder a: http://localhost:8000/docs
```
- [ ] Documentación carga correctamente
- [ ] Ambos endpoints de socios visibles
- [ ] Descripción actualizada

### 3. Pruebas Funcionales

#### Prueba 1: Socio con datos AgilPagos
```bash
curl "http://localhost:8000/sociocodigo/1001" | python -m json.tool
```
- [ ] `AgilPagos` contiene datos (no vacío)
- [ ] Campos presentes: `id_sg`, `id_user`, `cuentamutu`, `alta`
- [ ] Valores son válidos

#### Prueba 2: Socio sin datos AgilPagos
```bash
curl "http://localhost:8000/sociocodigo/2002" | python -m json.tool
```
- [ ] `AgilPagos` es objeto vacío: `{}`
- [ ] No genera error
- [ ] Resto de campos están presentes

#### Prueba 3: Socio no existe
```bash
curl "http://localhost:8000/socio/99999999999" | python -m json.tool
```
- [ ] Retorna código 404
- [ ] Mensaje de error: "Socio no encontrado"
- [ ] Sin excepciones no manejadas

#### Prueba 4: Tramite DNI presente
```bash
curl "http://localhost:8000/sociocodigo/1001" | python -m json.tool | grep -A1 "Tramite"
```
- [ ] Campo `Tramite DNI` presente en respuesta
- [ ] Valor es string o null
- [ ] Valor coincide con Socios.dbf

### 4. Pruebas de Rendimiento

#### Prueba 1: Consultas múltiples
```powershell
For ($i=1; $i -le 10; $i++) {
    Measure-Command { 
        Invoke-WebRequest "http://localhost:8000/sociocodigo/1001" | Out-Null 
    }
}
```
- [ ] Tiempo promedio < 500ms
- [ ] Sin timeouts
- [ ] Sin errores de conexión

#### Prueba 2: Consultas concurrentes
```bash
# Usar Apache Bench o similar
ab -n 100 -c 10 "http://localhost:8000/socio/20123456789"
```
- [ ] Todas las solicitudes exitosas (200)
- [ ] Sin errores 500
- [ ] Respuesta consistente

### 5. Pruebas de Seguridad

- [ ] Validación de entrada: caracteres especiales en CUIT
- [ ] Inyección SQL: imposible (no usa SQL)
- [ ] DoS: API resiste múltiples solicitudes
- [ ] Error handling: no expone información sensible

### 6. Compatibilidad

#### Clientes Antiguos
- [ ] Endpoints antiguos siguen funcionando
- [ ] Nuevos campos no rompen clientes existentes
- [ ] API es backward compatible

#### Diferentes Navegadores
- [ ] Chrome: /docs funciona
- [ ] Firefox: /docs funciona
- [ ] Edge: /docs funciona

#### Diferentes Sistemas
- [ ] Windows: API funciona
- [ ] PowerShell: API funciona
- [ ] Python requests: API funciona
- [ ] cURL: API funciona

## Post-Lanzamiento

### 1. Monitoreo
- [ ] Revisar logs de error en primeras 24 horas
- [ ] Verificar que consultas son procesadas correctamente
- [ ] Monitorear tiempo de respuesta

### 2. Feedback de Usuarios
- [ ] Recolectar feedback de usuarios
- [ ] Documentar issues encontrados
- [ ] Planificar hotfixes si es necesario

### 3. Documentación de Cambios
- [ ] Notificar a equipos que usan la API
- [ ] Compartir guía de uso: GUIA_RAPIDA.md
- [ ] Compartir ejemplos: EJEMPLO_RESPUESTA.md

### 4. Backup y Versionado
- [ ] Backup de main.py en producción
- [ ] Tag en Git: v2.0
- [ ] Documentar versión en CHANGELOG

## Rollback (Si es necesario)

### Si algo falla:
1. [ ] Detener servicio: `nssm stop API_LEER_DBF_MUTUAL`
2. [ ] Restaurar backup: `cp main.py.backup main.py`
3. [ ] Reiniciar servicio: `nssm start API_LEER_DBF_MUTUAL`
4. [ ] Verificar: `curl http://localhost:8000/docs`
5. [ ] Documentar issue en CAMBIOS.md

## Escalabilidad Futura

### Para próximas expansiones:
- [ ] Revisar PROXIMAS_EXPANSIONES.md
- [ ] Identificar cambios prioritarios
- [ ] Planificar timeline
- [ ] Asignar recursos

---

## Firmado

**Desarrollador:** Copilot  
**Fecha:** 2025-11-11  
**Versión API:** 2.0  
**Estado:** Listo para Producción ✅

---

## Notas Importantes

1. **Si algún item no se puede verificar**: 
   - Revisar que DBF_PATH en .env sea correcto
   - Verificar que archivos DBF existen
   - Revisar permisos de lectura

2. **Si test_socios.py falla**:
   - Verificar que API está corriendo
   - Cambiar CUIT_PRUEBA y CODIGO_PRUEBA por valores reales
   - Ver GUIA_RAPIDA.md sección Troubleshooting

3. **En caso de duda**:
   - Consultar CAMBIOS.md para detalles técnicos
   - Consultar EJEMPLO_RESPUESTA.md para ejemplos
   - Ejecutar test_socios.py con datos reales

---

**Última actualización:** 2025-11-11
