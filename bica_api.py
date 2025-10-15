# por el momento no se usa
from fastapi import FastAPI, HTTPException, Header, Depends, Request, Form
from pydantic import BaseModel
from typing import List
from dbfread import DBF
import os
import jwt
import time
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


app = FastAPI()

DBF_PATH = os.getenv("DBF_PATH")
SECRET_KEY = os.getenv("BICA_SECRET_KEY", "clave-secreta")

router = APIRouter(prefix="/bica", tags=["BICA"])

@app.post("/token")
def generar_token(
    grant_type: str = Form(...),
    Username: str = Form(...),
    Password: str = Form(...)
):
    if grant_type != "password" or Username != "bica" or Password != "segura":
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    payload = {
        "sub": Username,
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600  # 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# Modelo de entrada
class CuentaRequest(BaseModel):
    CUIT: str

# Modelo de salida
class CuentaMutual(BaseModel):
    TipoCuenta: str
    NumeroCuenta: int

class CuentaResponse(BaseModel):
    Existe: bool
    Convenio: int
    CuentasMutual: List[CuentaMutual]

# Función para buscar cuentas por CUIT
def buscar_cuentas_por_cuit(cuit: str) -> CuentaResponse:
    cuentas_dbf = DBF(os.path.join(DBF_PATH, 'Socios.dbf'), load=True)

    cuentas_encontradas = []
    convenio = os.getenv("BICA_CONVENIO", "0")
    tipo_cuenta = os.getenv("BICA_TIPO_CUENTA", "CA") 

    for cuenta in cuentas_dbf:
        if str(cuenta['CUIT']).strip() == str(cuit).strip():
            cuentas_encontradas.append(CuentaMutual(
                TipoCuenta=tipo_cuenta,
                NumeroCuenta=int(cuenta['SUCURSAL']) * 1_000_000 + int(cuenta['CODIGO'])
            ))
            convenio = convenio

    if cuentas_encontradas:
        return CuentaResponse(Existe=True, Convenio=convenio, CuentasMutual=cuentas_encontradas)
    else:
        return CuentaResponse(Existe=False, Convenio=0, CuentasMutual=[])


@app.post("/cuentamutual", response_model=CuentaResponse)
def obtener_info_cuenta(request: CuentaRequest, auth_key: str = Header(...)):
    expected_key = os.getenv("BICA_AUTH_KEY", "")
    if auth_key != expected_key:
        raise HTTPException(status_code=401, detail="No autorizado")
    return buscar_cuentas_por_cuit(request.CUIT)

security = HTTPBearer()
@app.post("/cuentamutual2", response_model=CuentaResponse)
def obtener_info_cuenta(
    request: CuentaRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")

    return buscar_cuentas_por_cuit(request.CUIT)
