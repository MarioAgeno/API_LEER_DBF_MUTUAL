"""Script para debuggear socio 1179 y verificar campos en tablas relacionadas"""
import os
from dbfread import DBF
from dotenv import load_dotenv

load_dotenv()
dbf_path = os.getenv('DBF_PATH')

def load_dbf(filename):
    """Carga un archivo DBF"""
    filepath = os.path.join(dbf_path, filename)
    try:
        return DBF(filepath, encoding='latin-1')
    except Exception as e:
        print(f"Error cargando {filename}: {e}")
        return None

def normalize_id(id_value):
    """Normaliza IDs para comparación"""
    if id_value is None:
        return None
    if isinstance(id_value, str):
        return id_value.strip().lower()
    return str(id_value).strip().lower()

def ids_match(id1, id2):
    """Compara IDs normalizados"""
    return normalize_id(id1) == normalize_id(id2)

print("=" * 80)
print("DEBUGGING SOCIO 1179 - Verificar campos en tablas relacionadas")
print("=" * 80)

# 1. Buscar socio 1179
print("\n[1] Buscando Socio 1179 en Socios.dbf...")
socios = load_dbf('Socios.dbf')
socio_1179 = None
if socios:
    for i, registro in enumerate(socios):
        if ids_match(registro.get('CODIGO'), '1179'):
            socio_1179 = registro
            print(f"OK - Socio encontrado en registro {i}")
            break

if socio_1179:
    print("\nCampos del Socio 1179:")
    print("-" * 80)
    for key in sorted(socio_1179.keys()):
        value = socio_1179.get(key)
        print(f"  {key:20} = {value}")
    
    # Campos clave para relaciones
    print("\n" + "=" * 80)
    print("CAMPOS CLAVE PARA RELACIONES:")
    print("=" * 80)
    tipopers = socio_1179.get('TIPOPERS')
    actividad = socio_1179.get('ACTIVIDAD')
    estcivil = socio_1179.get('ESTCIVIL')
    codpostal = socio_1179.get('CODPOSTAL')
    pais = socio_1179.get('PAIS')
    sitiva = socio_1179.get('SITIVA')
    
    print(f"TIPOPERS    = {tipopers} (tipo: {type(tipopers).__name__})")
    print(f"ACTIVIDAD   = {actividad} (tipo: {type(actividad).__name__})")
    print(f"ESTCIVIL    = {estcivil} (tipo: {type(estcivil).__name__})")
    print(f"CODPOSTAL   = {codpostal} (tipo: {type(codpostal).__name__})")
    print(f"PAIS        = {pais} (tipo: {type(pais).__name__})")
    print(f"SITIVA      = {sitiva} (tipo: {type(sitiva).__name__})")
else:
    print("ERROR - Socio 1179 NO encontrado")
    exit(1)

# 2. Verificar UIFPersona
print("\n" + "=" * 80)
print("[2] TABLA: UIFPersona.dbf")
print("=" * 80)
uif_persona = load_dbf('UIFPersona.dbf')
if uif_persona:
    reg_list = list(uif_persona)
    print(f"Total registros: {len(reg_list)}")
    uif_persona = load_dbf('UIFPersona.dbf')  # Recargar
    
    # Mostrar estructura de primer registro
    for i, reg in enumerate(uif_persona):
        if i == 0:
            print("\nCampos disponibles en UIFPersona:")
            for key in sorted(reg.keys()):
                print(f"  - {key}")
        
        # Buscar el que coincida con tipopers
        if tipopers and ids_match(reg.get('id'), tipopers):
            print(f"\nOK - Encontrado registro para TIPOPERS={tipopers}")
            for key in sorted(reg.keys()):
                print(f"  {key:20} = {reg.get(key)}")
            break
        
        if i >= 50:  # Mostrar algunos registros
            break
    
    # Si no encontró, mostrar algunos valores de 'id' disponibles
    uif_persona = load_dbf('UIFPersona.dbf')  # Recargar
    print("\nPrimeros 10 valores de 'id' en UIFPersona:")
    for i, reg in enumerate(uif_persona):
        if i < 10:
            print(f"  id={reg.get('id')}, id_sg={reg.get('id_sg')}")
        else:
            break

# 3. Verificar Actividad
print("\n" + "=" * 80)
print("[3] TABLA: Actividad.dbf")
print("=" * 80)
actividades = load_dbf('Actividad.dbf')
if actividades:
    reg_list = list(actividades)
    print(f"Total registros: {len(reg_list)}")
    actividades = load_dbf('Actividad.dbf')  # Recargar
    
    # Mostrar estructura
    for i, reg in enumerate(actividades):
        if i == 0:
            print("\nCampos disponibles en Actividad:")
            for key in sorted(reg.keys()):
                print(f"  - {key}")
        
        # Buscar el que coincida
        if actividad and ids_match(reg.get('CODIGO'), actividad):
            print(f"\nOK - Encontrado registro para ACTIVIDAD={actividad}")
            for key in sorted(reg.keys()):
                print(f"  {key:20} = {reg.get(key)}")
            break
        
        if i >= 50:
            break
    
    # Mostrar algunos valores disponibles
    actividades = load_dbf('Actividad.dbf')  # Recargar
    print("\nPrimeros 10 valores de 'CODIGO' en Actividad:")
    for i, reg in enumerate(actividades):
        if i < 10:
            print(f"  CODIGO={reg.get('CODIGO')}, id_sg={reg.get('id_sg')}")
        else:
            break

# 4. Verificar EstCivil
print("\n" + "=" * 80)
print("[4] TABLA: EstCivil.dbf")
print("=" * 80)
estcivil_dbf = load_dbf('EstCivil.dbf')
if estcivil_dbf:
    reg_list = list(estcivil_dbf)
    print(f"Total registros: {len(reg_list)}")
    estcivil_dbf = load_dbf('EstCivil.dbf')  # Recargar
    
    # Mostrar estructura
    for i, reg in enumerate(estcivil_dbf):
        if i == 0:
            print("\nCampos disponibles en EstCivil:")
            for key in sorted(reg.keys()):
                print(f"  - {key}")
        
        # Buscar el que coincida
        if estcivil and ids_match(reg.get('id'), estcivil):
            print(f"\nOK - Encontrado registro para ESTCIVIL={estcivil}")
            for key in sorted(reg.keys()):
                print(f"  {key:20} = {reg.get(key)}")
            break
        
        if i >= 50:
            break
    
    # Mostrar algunos valores
    estcivil_dbf = load_dbf('EstCivil.dbf')  # Recargar
    print("\nTodos los registros en EstCivil:")
    for i, reg in enumerate(estcivil_dbf):
        print(f"  id={reg.get('id')}, id_sg={reg.get('id_sg')}, descripcion={reg}")

# 5. Verificar horasacr y provincias
print("\n" + "=" * 80)
print("[5] TABLA: horasacr.dbf y provincias.dbf")
print("=" * 80)
horasacr = load_dbf('horasacr.dbf')
if horasacr:
    reg_list = list(horasacr)
    print(f"Total registros en horasacr: {len(reg_list)}")
    horasacr = load_dbf('horasacr.dbf')  # Recargar
    
    # Mostrar estructura
    for i, reg in enumerate(horasacr):
        if i == 0:
            print("\nCampos disponibles en horasacr:")
            for key in sorted(reg.keys()):
                print(f"  - {key}")
        
        # Buscar el que coincida con codpostal
        if codpostal and ids_match(reg.get('CODIGO'), codpostal):
            print(f"\nOK - Encontrado en horasacr para CODPOSTAL={codpostal}")
            for key in sorted(reg.keys()):
                print(f"  {key:20} = {reg.get(key)}")
            
            # Ahora buscar en provincias
            inaescd = reg.get('inaescd')
            print(f"\nBuscando en provincias con provincia={inaescd}...")
            provincias = load_dbf('provincias.dbf')
            if provincias:
                for prov_reg in provincias:
                    if ids_match(prov_reg.get('provincia'), inaescd):
                        print(f"OK - Encontrado en provincias:")
                        for key in sorted(prov_reg.keys()):
                            print(f"  {key:20} = {prov_reg.get(key)}")
                        break
            break
        
        if i >= 50:
            break
    
    # Mostrar primeros registros
    horasacr = load_dbf('horasacr.dbf')  # Recargar
    print("\nPrimeros 5 registros de horasacr:")
    for i, reg in enumerate(horasacr):
        if i < 5:
            print(f"  CODIGO={reg.get('CODIGO')}, inaescd={reg.get('inaescd')}")
        else:
            break

# 6. Verificar Paises
print("\n" + "=" * 80)
print("[6] TABLA: Paises.dbf")
print("=" * 80)
paises = load_dbf('Paises.dbf')
if paises:
    reg_list = list(paises)
    print(f"Total registros: {len(reg_list)}")
    paises = load_dbf('Paises.dbf')  # Recargar
    
    # Mostrar estructura
    for i, reg in enumerate(paises):
        if i == 0:
            print("\nCampos disponibles en Paises:")
            for key in sorted(reg.keys()):
                print(f"  - {key}")
        
        # Buscar el que coincida
        if pais and ids_match(reg.get('CODIGO'), pais):
            print(f"\nOK - Encontrado registro para PAIS={pais}")
            for key in sorted(reg.keys()):
                print(f"  {key:20} = {reg.get(key)}")
            break
        
        if i >= 50:
            break
    
    # Mostrar algunos valores
    paises = load_dbf('Paises.dbf')  # Recargar
    print("\nPrimeros 5 valores en Paises:")
    for i, reg in enumerate(paises):
        if i < 5:
            print(f"  CODIGO={reg.get('CODIGO')}, id_sg={reg.get('id_sg')}")
        else:
            break

# 7. Verificar CodIva
print("\n" + "=" * 80)
print("[7] TABLA: CodIva.dbf")
print("=" * 80)
codiva = load_dbf('CodIva.dbf')
if codiva:
    reg_list = list(codiva)
    print(f"Total registros: {len(reg_list)}")
    codiva = load_dbf('CodIva.dbf')  # Recargar
    
    # Mostrar estructura
    for i, reg in enumerate(codiva):
        if i == 0:
            print("\nCampos disponibles en CodIva:")
            for key in sorted(reg.keys()):
                print(f"  - {key}")
        
        # Buscar el que coincida
        if sitiva and ids_match(reg.get('CODIGO'), sitiva):
            print(f"\nOK - Encontrado registro para SITIVA={sitiva}")
            for key in sorted(reg.keys()):
                print(f"  {key:20} = {reg.get(key)}")
            break
        
        if i >= 50:
            break
    
    # Mostrar algunos valores
    codiva = load_dbf('CodIva.dbf')  # Recargar
    print("\nPrimeros 5 valores en CodIva:")
    for i, reg in enumerate(codiva):
        if i < 5:
            print(f"  CODIGO={reg.get('CODIGO')}, id_sg={reg.get('id_sg')}")
        else:
            break

print("\n" + "=" * 80)
print("FIN DEL DEBUG")
print("=" * 80)
