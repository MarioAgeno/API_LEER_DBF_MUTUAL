# Ejemplos de Respuesta de la API - Endpoints de Socios

## 1. GET `/socio/{cuit}` - Búsqueda por CUIT

### Solicitud
```
GET http://localhost:8000/socio/20123456789
```

### Respuesta (200 OK)
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
  "Estado Civil": "Casado",
  "Condicion Fiscal": "Responsable Inscripto",
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
  }
}
```

## 2. GET `/sociocodigo/{codigo_socio}` - Búsqueda por Código

### Solicitud
```
GET http://localhost:8000/sociocodigo/1001
```

### Respuesta (200 OK)
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
  "Estado Civil": "Casado",
  "Condicion Fiscal": "Responsable Inscripto",
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
  }
}
```

## 3. Socio sin datos en AgilPagos

Si un socio no existe en la tabla `sociosSG`, el campo `AgilPagos` será un objeto vacío:

```json
{
  "Codigo": "2002",
  "Nombre": "María José Rodríguez",
  "...otros campos...",
  "Tramite DNI": "XYZ789ABC123",
  "AgilPagos": {}
}
```

## 4. Respuesta 404 - Socio no encontrado

### Solicitud
```
GET http://localhost:8000/socio/20999999999
```

### Respuesta (404 Not Found)
```json
{
  "detail": "Socio no encontrado"
}
```

## Campos Nuevos Agregados

### `Tramite DNI`
- **Tipo**: String o null
- **Descripción**: Número de trámite del DNI del socio
- **Fuente**: Campo `TRAMITEDNI` de la tabla `Socios.dbf`

### `AgilPagos`
- **Tipo**: Object
- **Descripción**: Información de integración con AgilPagos
- **Subcampos**:
  - **id_sg**: Identificador único en el sistema AgilPagos
  - **id_user**: ID de usuario en AgilPagos
  - **cuentamutu**: Número de cuenta del socio en la mutual
  - **alta**: Fecha de alta del socio en AgilPagos (formato YYYY-MM-DD)

## Integración Frontend

Para acceder a estos datos en tu aplicación frontend:

```javascript
// JavaScript/Fetch
fetch('/sociocodigo/1001')
  .then(response => response.json())
  .then(data => {
    console.log('Datos del Socio:', data);
    console.log('Trámite DNI:', data['Tramite DNI']);
    console.log('ID en AgilPagos:', data.AgilPagos.id_sg);
    console.log('Cuenta en Mutual:', data.AgilPagos.cuentamutu);
    console.log('Fecha de Alta:', data.AgilPagos.alta);
  });
```

```python
# Python/Requests
import requests

response = requests.get('http://localhost:8000/sociocodigo/1001')
data = response.json()

print(f"Trámite DNI: {data['Tramite DNI']}")
print(f"ID AgilPagos: {data['AgilPagos']['id_sg']}")
print(f"Cuenta Mutual: {data['AgilPagos']['cuentamutu']}")
print(f"Fecha Alta: {data['AgilPagos']['alta']}")
```
