from fastapi import FastAPI, HTTPException
from dbfread import DBF
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()
DBF_PATH = os.getenv("DBF_PATH")

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
    socios = DBF(os.path.join(DBF_PATH, 'Socios.dbf'), load=True)
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
    prestamos = DBF(os.path.join(DBF_PATH, 'Movae01.dbf'), load=True)
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
    prestamos = DBF(os.path.join(DBF_PATH, 'Movae01.dbf'), load=True)
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
    cuotas = DBF(os.path.join(DBF_PATH, 'Cuotas.dbf'), load=True)
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
    socios = DBF(os.path.join(DBF_PATH, 'Socios.dbf'), load=True)
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

# Funcion para consultar saldos de cuentas
def get_saldos_cuentas(cuenta_socio):
    saldos = DBF(os.path.join(DBF_PATH, 'sdoca01.dbf'), load=True)
    comprobantes = DBF(os.path.join(DBF_PATH, 'comprobantes.dbf'), load=True)
    # Crear un diccionario para buscar rápido el nombre de comprobantes por ID
    comprobantes_dict = {
        row['IDCOMPRO']: row['NOMBRE']
        for row in comprobantes
        if row['MODULO'] == 'AMV'
    }
    saldos_cuenta = [
        {
            'Cuenta': cuenta['CUENTA'],
            'Tipo': cuenta['TIPO'],
            'Nombre': comprobantes_dict.get('AMV' + cuenta['TIPO'], ''),
            'Saldo': cuenta['SALDO'],
            'Cuenta_WEB': cuenta['CUENTAWEB']
        }
        for cuenta in saldos if cuenta['CUENTA'] == cuenta_socio
    ]
    return saldos_cuenta

# Funcion para consultar movimientos del mes de las caja de ahorros
def get_movimientos_cuentas(cuenta, tipo):
    movimiento_ca = DBF(os.path.join(DBF_PATH, 'movca01.dbf'), load=True)
    amvcpto = DBF(os.path.join(DBF_PATH, 'amvcpto.dbf'), load=True)
    # Crear un diccionario para buscar rápido el nombre por código
    amvcpto_dict = {
        row['CODIGO']: {
            'NOMBRE': row['NOMBRE'],
            'MULTIPLICA': row['MULTIPLICA']
        }
       for row in amvcpto
    }    
    saldo_acumulado = 0
    resumen = []
    for mov in movimiento_ca:
        if mov['CUENTA'] == cuenta and mov['TIPO'] == tipo:
            importe = mov['MOVIMI'] * amvcpto_dict.get(mov['CODMOV'], {}).get('MULTIPLICA', 1)
            saldo_acumulado += importe
            resumen.append({
                'Fecha': mov['FECHA'],
                'Numero': mov['NUMERO'],
                'Concepto': mov['CODMOV'],
                'Nombre_Concepto': amvcpto_dict.get(mov['CODMOV'], {}).get('NOMBRE', ''),
                'Importe': importe,
                'Saldo': round(saldo_acumulado, 2),
                'Observacion': mov['OBSERVA']
            })
    return resumen

# Funcion para consultar movimientos de las caja de ahorros historicos
import datetime
def get_movimientos_cuentas_historicos(cuenta, tipo):
    movimiento_ca = DBF(os.path.join(DBF_PATH, 'movca01.dbf'), load=True)
    amvcpto = DBF(os.path.join(DBF_PATH, 'amvcpto.dbf'), load=True)
    amvcpto_dict = {row['CODIGO']: row['NOMBRE'] for row in amvcpto}

    # Calcular rango de fechas
    hoy = datetime.date.today()
    primer_dia_mes_actual = hoy.replace(day=1)
    mes_inicio = primer_dia_mes_actual.month - 3
    anio_inicio = primer_dia_mes_actual.year
    while mes_inicio <= 0:
        mes_inicio += 12
        anio_inicio -= 1
    fecha_inicio = datetime.date(anio_inicio, mes_inicio, 1)
    if primer_dia_mes_actual.month == 12:
        fecha_fin = datetime.date(primer_dia_mes_actual.year + 1, 1, 1) - datetime.timedelta(days=1)
    else:
        fecha_fin = datetime.date(primer_dia_mes_actual.year, primer_dia_mes_actual.month + 1, 1) - datetime.timedelta(days=1)

    resumen = []
    for mov in movimiento_ca:
        if mov['CUENTA'] == cuenta and mov['TIPO'] == tipo:
            fecha_mov = mov.get('FECHA')
            try:
                if isinstance(fecha_mov, datetime.date):
                    pass
                elif isinstance(fecha_mov, str):
                    try:
                        fecha_mov = datetime.datetime.strptime(fecha_mov, "%Y-%m-%d").date()
                    except Exception:
                        try:
                            fecha_mov = datetime.datetime.strptime(fecha_mov, "%d/%m/%Y").date()
                        except Exception:
                            continue
                else:
                    continue
                if fecha_mov is None:
                    continue
                if fecha_inicio <= fecha_mov <= fecha_fin:
                    resumen.append({
                        'Fecha': mov['FECHA'],
                        'Numero': mov['NUMERO'],
                        'Concepto': mov['CODMOV'],
                        'Importe': mov['MOVIMI'],
                        'Nombre_Concepto': amvcpto_dict.get(mov['CODMOV'], ''),
                        'Observacion': mov['OBSERVA']
                    })
            except Exception:
                continue
    return resumen

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
    
@app.get("/saldos/{cuenta}")
def obtener_saldos(cuenta: int):
    saldos = get_saldos_cuentas(cuenta)
    if saldos:
        return saldos
    else:
        raise HTTPException(status_code=404, detail="No se encontraron cuentas para este socio")

@app.get("/resumen_cuenta/{cuenta}/{tipo}")
def obtener_resumen_cuenta_mes(cuenta: int, tipo: str):
    resumen = get_movimientos_cuentas(cuenta, tipo)
    if resumen:
        return resumen
    else:
        raise HTTPException(status_code=404, detail="No se encontraron movimientos para esta cuentas")

@app.get("/resumen_cuenta_historico/{cuenta}/{tipo}")
def obtener_resumen_cuenta_mes_historico(cuenta: int, tipo: str):
    resumen = get_movimientos_cuentas_historicos(cuenta, tipo)
    if resumen:
        return resumen
    else:
        raise HTTPException(status_code=404, detail="No se encontraron movimientos historicos para esta cuentas")

   
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
