import os
from dbfread import DBF
from dotenv import load_dotenv

load_dotenv()
dbf_path = os.getenv('DBF_PATH')

def check_table(filename):
    filepath = os.path.join(dbf_path, filename)
    try:
        dbf = DBF(filepath, encoding='latin-1')
        # Get field names
        field_names = [f.name for f in dbf.fields]
        
        # Get first record
        reg = next(iter(dbf), None)
        
        print(f"\n{filename}:")
        print(f"  Fields: {field_names}")
        if reg:
            for key in sorted(field_names):
                val = reg.get(key)
                print(f"    {key}: {val} ({type(val).__name__})")
        return True
    except Exception as e:
        print(f"\n{filename}: ERROR - {e}")
        return False

# Check each table
check_table('EstCivil.dbf')
check_table('Paises.dbf')
check_table('CodIva.dbf')
check_table('horasacr.dbf')
check_table('provincias.dbf')
check_table('UIFPersona.dbf')
check_table('Actividad.dbf')

# List available DBF files
print("\n" + "="*60)
print("Archivos DBF disponibles:")
import glob
files = glob.glob(os.path.join(dbf_path, '*.dbf'))
for f in sorted(files):
    print(f"  {os.path.basename(f).upper()}")
