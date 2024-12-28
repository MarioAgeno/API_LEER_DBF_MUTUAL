from fastapi import FastAPI, HTTPException
from dbfread import DBF
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "MAASoft - API Consultas de Prestamos !!!"

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen (puedes restringir esto según el dominio)
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP
    allow_headers=["*"],  # Permitir todos los encabezados
)


# Funcion para consultar un Socio por su CUIT
def get_socio_by_cuit(cuit):
    socios = DBF('D:/CLIENTES/mtl/DATA/Socios.dbf', load=True)
    for socio in socios:
        if socio['CUIT'] == cuit:
            return {
                'Codigo': socio['CODIGO'],
                'Nombre': socio['NOMBRE'],
                'Domicilio': socio['DOMICI'],
                'Tipo Documento': socio['TIPODOC'],
                'Numero': socio['NRODOC'],
                'CUIT': socio['CUIT']
            }
    return None

# Funcion para consultar los prestamos de un Socio por su codigo
def get_prestamos_by_socio(codigo_socio):
    prestamos = DBF('D:/CLIENTES/mtl/DATA/MOVAE01.dbf', load=True)
    prestamos_socio = [
        {
            'Ayuda': prestamo['AYUDA'],
            'fecha': prestamo['FECHA'],
            'TEM': prestamo['TEM'],
            'TEA': prestamo['TEA'],
            'TNA': prestamo['TNA'],
            'CFT': prestamo['CFT'],
            'Plazo': prestamo['PLAZO'],
            'Cuotas': prestamo['CUOTAS'],
            'Capital': prestamo['MONTO'],
            'Devengamientos': prestamo['INTERE'],
            'Gastos': prestamo['GASTOS'],
            'Seguro': prestamo['SEGURO'],
            'Total': prestamo['TOTAL'],
            'Linea': prestamo['COMPRO'],
            'Tipo': prestamo['TIPO']
        }
        for prestamo in prestamos if prestamo['SOCIO'] == codigo_socio
    ]
    return prestamos_socio

# Funcion para consultar un prestamo por su numero
def get_prestamos_by_ayuda(ayuda):
    prestamos = DBF('D:/CLIENTES/mtl/DATA/MOVAE01.dbf', load=True)
    for prestamo in prestamos:
        if prestamo['AYUDA'] == ayuda:
            return {
                'Ayuda': prestamo['AYUDA'],
                'fecha': prestamo['FECHA'],
                'TEM': prestamo['TEM'],
                'TEA': prestamo['TEA'],
                'TNA': prestamo['TNA'],
                'CFT': prestamo['CFT'],
                'Plazo': prestamo['PLAZO'],
                'Cuotas': prestamo['CUOTAS'],
                'Capital': prestamo['MONTO'],
                'Devengamientos': prestamo['INTERE'],
                'Gastos': prestamo['GASTOS'],
                'Seguro': prestamo['SEGURO'],
                'Total': prestamo['TOTAL'],
                'Linea': prestamo['COMPRO'],
                'Tipo': prestamo['TIPO']
            }
    return None

# Funcion para consultar las cuotas de un prestamos por el numero
def get_cuotas_by_ayuda(ayuda):
    cuotas = DBF('D:/CLIENTES/mtl/DATA/CUOTAS.dbf', load=True)
    cuotas_ayuda = [
        {
            'Ayuda': prestamo['AYUDA'],
            'Socio': prestamo['SOCIO'],
            'Vencimiento': prestamo['FECVTO'],
            'Nro.Cuota': prestamo['NROCTA'],
            'Deuda': prestamo['DEUDA'],
            'Capital': prestamo['AMORTI'],
            'Interes': prestamo['INTERE'],
            'Interes2': prestamo['INTERE2'],
            'Gastos': prestamo['GASTOS'],
            'Varios': prestamo['VARIOS'],
            'Otros': prestamo['OTROS'],
            'Seguro': prestamo['SEGURO'],
            'Improte Cuota': prestamo['VALCTA'],
            'Amortizado': prestamo['TOTAMO'],
            'Linea': prestamo['MONEDA']
        }
        for prestamo in cuotas if prestamo['AYUDA'] == ayuda
    ]
    return cuotas_ayuda

# Funcion para consultar datos del socio por el Codigo (lo uso en sistema WEB de Tarjetas)
def get_socio_by_codigo(codigo_socio):
    socios = DBF('D:/CLIENTES/mtl/DATA/Socios.dbf', load=True)
    for socio in socios:
        if socio['CODIGO'] == codigo_socio:
            return {
                'Nombre': socio['NOMBRE'],
                'Domicilio': socio['DOMICI'],
                'Codigo Postal': socio['CODPOSTAL'],
                'CUIT': socio['CUIT'],
                'Fecha Nacimiento': socio['FECNAC'],
                'Fecha Ingreso': socio['FECING'],
                'Es PEP': socio['PEP'],
                'Nacionalidad': socio['NACION'],
                'Telefono': socio['TELEFO'],
                'Telefono 2': socio['FAX'],
                'Movil': socio['CELULAR'],
                'e-Mail': socio['MAIL'],
                'Codigo Actividad': socio['ACTIVIDAD']
            }
    return None


@app.get("/socio/{cuit}")
def obtener_socio(cuit: int):
    socio = get_socio_by_cuit(cuit)
    if socio:
        return socio
    else:
        raise HTTPException(status_code=404, detail="Socio no encontrado")

@app.get("/prestamos/{codigo_socio}")
def obtener_prestamos(codigo_socio: int):
    prestamos = get_prestamos_by_socio(codigo_socio)
    if prestamos:
        return prestamos
    else:
        raise HTTPException(status_code=404, detail="No se encontraron préstamos")

@app.get("/ayuda/{ayuda}")
def obtener_ayuda(ayuda: int):
    prestamos = get_prestamos_by_ayuda(ayuda)
    if prestamos:
        return prestamos
    else:
        raise HTTPException(status_code=404, detail="No se encontraron préstamos")

@app.get("/cuotas/{ayuda}")
def obtener_cuotas(ayuda: int):
    cuotas = get_cuotas_by_ayuda(ayuda)
    if cuotas:
        return cuotas
    else:
        raise HTTPException(status_code=404, detail="No se encontraron préstamos")
    
@app.get("/sociocodigo/{codigo_socio}")
def socio_por_codigo(codigo_socio: int):
    socio = get_socio_by_codigo(codigo_socio)
    if socio:
        return socio
    else:
        raise HTTPException(status_code=404, detail="Socio no encontrado")

# Ruta personalizada para la documentación
@app.get("/docs", response_class=HTMLResponse, include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Documentación")

# Ruta personalizada para la especificación OpenAPI
@app.get("/openapi.json", include_in_schema=False)
async def get_custom_openapi():
    return JSONResponse(get_openapi(title="API Documentation", version="1.0.0", routes=app.routes))


@app.get('/', response_class=HTMLResponse, tags=['Inicio'])
async def mensage():
    return '''
    <h1><a href='http://www.maasoft.com.ar'>MAASoft WEB</a></h1>
    <a href='http://localhost:8000/docs'>Documentacion</a>
    '''

# -- Para Ejecutar desde consola solo llamando py main.py
'''
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
'''
