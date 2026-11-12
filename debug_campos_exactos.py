"""Script para ver la estructura exacta de campos en cada tabla"""
import os
from dbfread import DBF
from dotenv import load_dotenv

load_dotenv()
dbf_path = os.getenv('DBF_PATH')

def load_dbf(filename):
    filepath = os.path.join(dbf_path, filename)
    try:
        return DBF(filepath, encoding='latin-1')
    except Exception as e:
        print(f"Error: {filename}: {e}")
        return None

print("=" * 100)
print("ESTRUCTURA EXACTA DE CAMPOS EN TABLAS")
print("=" * 100)

# 1. EstCivil
print("\n[1] EstCivil.dbf:")
estcivil = load_dbf('EstCivil.dbf')
if estcivil:
    for i, reg in enumerate(estcivil):
        if i == 0:
            print(f"Campo fields: {estcivil.fields}")
            print(f"\nPrimer registro:")
            for key, value in reg.items():
                print(f"  '{key}': '{value}' (type: {type(value).__name__})")
            break

# 2. Paises
print("\n" + "=" * 100)
print("[2] Paises.dbf:")
paises = load_dbf('Paises.dbf')
if paises:
    for i, reg in enumerate(paises):
        if i == 0:
            print(f"Campo fields: {paises.fields}")
            print(f"\nPrimer registro:")
            for key, value in reg.items():
                print(f"  '{key}': '{value}' (type: {type(value).__name__})")
            break

# 3. CodIva
print("\n" + "=" * 100)
print("[3] CodIva.dbf:")
codiva = load_dbf('CodIva.dbf')
if codiva:
    for i, reg in enumerate(codiva):
        if i == 0:
            print(f"Campo fields: {codiva.fields}")
            print(f"\nPrimer registro:")
            for key, value in reg.items():
                print(f"  '{key}': '{value}' (type: {type(value).__name__})")
            break

# 4. horasacr
print("\n" + "=" * 100)
print("[4] horasacr.dbf:")
horasacr = load_dbf('horasacr.dbf')
if horasacr:
    for i, reg in enumerate(horasacr):
        if i == 0:
            print(f"Campo fields: {horasacr.fields}")
            print(f"\nPrimer registro:")
            for key, value in reg.items():
                print(f"  '{key}': '{value}' (type: {type(value).__name__})")
            break

# 5. provincias
print("\n" + "=" * 100)
print("[5] provincias.dbf:")
provincias = load_dbf('provincias.dbf')
if provincias:
    for i, reg in enumerate(provincias):
        if i == 0:
            print(f"Campo fields: {provincias.fields}")
            print(f"\nPrimer registro:")
            for key, value in reg.items():
                print(f"  '{key}': '{value}' (type: {type(value).__name__})")
            break

# 6. UIFPersona
print("\n" + "=" * 100)
print("[6] UIFPersona.dbf:")
uif = load_dbf('UIFPersona.dbf')
if uif:
    for i, reg in enumerate(uif):
        if i == 0:
            print(f"Campo fields: {uif.fields}")
            print(f"\nPrimer registro:")
            for key, value in reg.items():
                print(f"  '{key}': '{value}' (type: {type(value).__name__})")
            break

# 7. Actividad - si existe
print("\n" + "=" * 100)
print("[7] Actividad.dbf:")
actividad = load_dbf('Actividad.dbf')
if actividad:
    for i, reg in enumerate(actividad):
        if i == 0:
            print(f"Campo fields: {actividad.fields}")
            print(f"\nPrimer registro:")
            for key, value in reg.items():
                print(f"  '{key}': '{value}' (type: {type(value).__name__})")
            break
else:
    print("TABLA NO ENCONTRADA - listar archivos disponibles en DBF_PATH:")
    import glob
    files = glob.glob(os.path.join(dbf_path, '*.dbf'))
    print(f"Total archivos: {len(files)}")
    for f in sorted(files):
        print(f"  {os.path.basename(f)}")
