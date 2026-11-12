"""Test para verificar que las relaciones funcionan con socio 1179"""
import os
import sys
from dbfread import DBF
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv

load_dotenv()
dbf_path = os.getenv('DBF_PATH')

def load_dbf(filename):
    filepath = os.path.join(dbf_path, filename)
    try:
        return DBF(filepath, encoding='latin-1')
    except Exception as e:
        print(f"Error: {e}")
        return None

def normalize_id(value):
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.replace(',', '.')
    try:
        decimal_value = Decimal(text)
        if decimal_value == decimal_value.to_integral_value():
            text = str(int(decimal_value))
        else:
            text = format(decimal_value.normalize(), 'f').rstrip('0').rstrip('.')
    except (InvalidOperation, ValueError):
        pass
    return text.lstrip('0') or '0'

def ids_match(db_value, query_value):
    return normalize_id(db_value) == normalize_id(query_value)

# ===== Funciones de relacion (CORREGIDAS) =====

def get_tipo_persona_id_sg(tipopers):
    try:
        uif_persona = load_dbf('UIFPERSONA.dbf')
        for registro in uif_persona:
            if ids_match(registro.get('ID'), tipopers):
                return registro.get('ID_SG')
    except Exception as e:
        print(f"Error en get_tipo_persona_id_sg: {e}")
    return None

def get_actividad_id_sg(codigo_actividad):
    try:
        actividades = load_dbf('ACTIVIDA.dbf')
        for registro in actividades:
            if ids_match(registro.get('CODIGO'), codigo_actividad):
                return registro.get('ID_SG')
    except Exception as e:
        print(f"Error en get_actividad_id_sg: {e}")
    return None

def get_estado_civil_id_sg(id_estcivil):
    try:
        estcivil = load_dbf('ESTCIVIL.dbf')
        for registro in estcivil:
            if ids_match(registro.get('CODIGO'), id_estcivil):
                return registro.get('ID_SG')
    except Exception as e:
        print(f"Error en get_estado_civil_id_sg: {e}")
    return None

def get_provincia_id_sg(codpostal):
    try:
        horasacr = load_dbf('HORASACR.dbf')
        provincias = load_dbf('PROVINCIAS.dbf')
        
        for reg_horasacr in horasacr:
            if ids_match(reg_horasacr.get('CODIGO'), codpostal):
                inaescd = reg_horasacr.get('INAESCD')
                print(f"  Encontrado en horasacr: CODIGO={codpostal} -> INAESCD={inaescd}")
                
                for reg_provincia in provincias:
                    if ids_match(reg_provincia.get('PROVINCIA'), inaescd):
                        id_sg = reg_provincia.get('ID_SG')
                        print(f"  Encontrado en provincias: PROVINCIA={inaescd} -> ID_SG={id_sg}")
                        return id_sg
                print(f"  NO encontrado en provincias el INAESCD={inaescd}")
                return None
        print(f"  NO encontrado en horasacr el CODIGO={codpostal}")
    except Exception as e:
        print(f"Error en get_provincia_id_sg: {e}")
    return None

def get_pais_id_sg(codigo_pais):
    try:
        paises = load_dbf('PAISES.dbf')
        for registro in paises:
            if ids_match(registro.get('CODIGO'), codigo_pais):
                return registro.get('ID_SG')
    except Exception as e:
        print(f"Error en get_pais_id_sg: {e}")
    return None

def get_situacion_iva_id_sg(codigo_iva):
    try:
        codiva = load_dbf('CODIVA.dbf')
        for registro in codiva:
            if ids_match(registro.get('CODIGO'), codigo_iva):
                return registro.get('ID_SG')
    except Exception as e:
        print(f"Error en get_situacion_iva_id_sg: {e}")
    return None

# ===== TEST =====

print("=" * 80)
print("TEST DE RELACIONES - SOCIO 1179")
print("=" * 80)

# Buscar socio 1179
socios = load_dbf('SOCIOS.dbf')
socio = None
for reg in socios:
    if ids_match(reg.get('CODIGO'), '1179'):
        socio = reg
        break

if not socio:
    print("ERROR: Socio 1179 no encontrado")
    sys.exit(1)

print("\nCampos del Socio 1179:")
print(f"  TIPOPERS  = {socio.get('TIPOPERS')}")
print(f"  ACTIVIDAD = {socio.get('ACTIVIDAD')}")
print(f"  ESTCIVIL  = {socio.get('ESTCIVIL')}")
print(f"  CODPOSTAL = {socio.get('CODPOSTAL')}")
print(f"  PAIS      = {socio.get('PAIS')}")
print(f"  SITIVA    = {socio.get('SITIVA')}")

print("\n" + "=" * 80)
print("PROBANDO FUNCIONES DE RELACION")
print("=" * 80)

# Tipo Persona
print("\n[1] get_tipo_persona_id_sg({})".format(socio.get('TIPOPERS')))
tipo_persona = get_tipo_persona_id_sg(socio.get('TIPOPERS'))
print(f"    Resultado: {tipo_persona}")

# Actividad
print("\n[2] get_actividad_id_sg({})".format(socio.get('ACTIVIDAD')))
actividad = get_actividad_id_sg(socio.get('ACTIVIDAD'))
print(f"    Resultado: {actividad}")

# Estado Civil
print("\n[3] get_estado_civil_id_sg({})".format(repr(socio.get('ESTCIVIL'))))
estado_civil = get_estado_civil_id_sg(socio.get('ESTCIVIL'))
print(f"    Resultado: {estado_civil}")

# Provincia
print("\n[4] get_provincia_id_sg({})".format(socio.get('CODPOSTAL')))
provincia = get_provincia_id_sg(socio.get('CODPOSTAL'))
print(f"    Resultado: {provincia}")

# Pais
print("\n[5] get_pais_id_sg({})".format(repr(socio.get('PAIS'))))
pais = get_pais_id_sg(socio.get('PAIS'))
print(f"    Resultado: {pais}")

# Situacion IVA
print("\n[6] get_situacion_iva_id_sg({})".format(repr(socio.get('SITIVA'))))
situacion_iva = get_situacion_iva_id_sg(socio.get('SITIVA'))
print(f"    Resultado: {situacion_iva}")

print("\n" + "=" * 80)
print("RESULTADO FINAL")
print("=" * 80)
print(f"tipo_persona_id_sg:     {tipo_persona}")
print(f"actividad_id_sg:        {actividad}")
print(f"estado_civil_id_sg:     {estado_civil}")
print(f"provincia_id_sg:        {provincia}")
print(f"pais_id_sg:             {pais}")
print(f"situacion_iva_id_sg:    {situacion_iva}")

if all([tipo_persona, actividad, estado_civil, provincia, pais, situacion_iva]):
    print("\nOK - TODAS LAS RELACIONES FUNCIONANDO CORRECTAMENTE")
else:
    print("\nERROR - ALGUNAS RELACIONES NO FUNCIONAN")
