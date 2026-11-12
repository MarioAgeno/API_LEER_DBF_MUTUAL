"""
Script de prueba para verificar los nuevos campos en los endpoints de socios
Ejecutar con: python test_socios.py
"""

import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"

def test_socio_por_cuit(cuit: str):
    """Prueba el endpoint GET /socio/{cuit}"""
    print(f"\n{'='*60}")
    print(f"Probando: GET /socio/{cuit}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{BASE_URL}/socio/{cuit}")
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Respuesta exitosa (200)")
            print("\nDatos del Socio:")
            print(f"  • Código: {data.get('Codigo')}")
            print(f"  • Nombre: {data.get('Nombre')}")
            print(f"  • CUIT: {data.get('CUIT')}")
            print(f"  • Número DNI: {data.get('Numero Documento')}")
            print(f"  • Trámite DNI: {data.get('Tramite DNI')}")
            
            print("\nDatos de AgilPagos:")
            agilpagos = data.get('AgilPagos', {})
            if agilpagos:
                print(f"  • ID en AgilPagos: {agilpagos.get('id_sg')}")
                print(f"  • ID Usuario: {agilpagos.get('id_user')}")
                print(f"  • Cuenta en Mutual: {agilpagos.get('cuentamutu')}")
                print(f"  • Fecha de Alta: {agilpagos.get('alta')}")
            else:
                print("  (No hay datos de AgilPagos para este socio)")
            
            return True
        else:
            print(f"\n✗ Error {response.status_code}")
            print(f"  Detalle: {response.json()}")
            return False
    except Exception as e:
        print(f"\n✗ Excepción: {str(e)}")
        return False

def test_socio_por_codigo(codigo: str):
    """Prueba el endpoint GET /sociocodigo/{codigo_socio}"""
    print(f"\n{'='*60}")
    print(f"Probando: GET /sociocodigo/{codigo}")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{BASE_URL}/sociocodigo/{codigo}")
        if response.status_code == 200:
            data = response.json()
            print("\n✓ Respuesta exitosa (200)")
            print("\nDatos del Socio:")
            print(f"  • Código: {data.get('Codigo')}")
            print(f"  • Nombre: {data.get('Nombre')}")
            print(f"  • CUIT: {data.get('CUIT')}")
            print(f"  • Número DNI: {data.get('Numero Documento')}")
            print(f"  • Trámite DNI: {data.get('Tramite DNI')}")
            
            print("\nDatos de AgilPagos:")
            agilpagos = data.get('AgilPagos', {})
            if agilpagos:
                print(f"  • ID en AgilPagos: {agilpagos.get('id_sg')}")
                print(f"  • ID Usuario: {agilpagos.get('id_user')}")
                print(f"  • Cuenta en Mutual: {agilpagos.get('cuentamutu')}")
                print(f"  • Fecha de Alta: {agilpagos.get('alta')}")
            else:
                print("  (No hay datos de AgilPagos para este socio)")
            
            return True
        else:
            print(f"\n✗ Error {response.status_code}")
            print(f"  Detalle: {response.json()}")
            return False
    except Exception as e:
        print(f"\n✗ Excepción: {str(e)}")
        return False

def test_json_completo(cuit: Optional[str] = None, codigo: Optional[str] = None):
    """Muestra la respuesta JSON completa"""
    print(f"\n{'='*60}")
    print(f"Respuesta JSON Completa")
    print(f"{'='*60}\n")
    
    if cuit:
        try:
            response = requests.get(f"{BASE_URL}/socio/{cuit}")
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Excepción: {str(e)}")
    
    elif codigo:
        try:
            response = requests.get(f"{BASE_URL}/sociocodigo/{codigo}")
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=2, ensure_ascii=False))
            else:
                print(f"Error: {response.status_code}")
        except Exception as e:
            print(f"Excepción: {str(e)}")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("TEST DE NUEVOS CAMPOS EN ENDPOINTS DE SOCIOS")
    print("="*60)
    
    # Cambiar estos valores por datos reales de tu base de datos
    CUIT_PRUEBA = "20123456789"
    CODIGO_PRUEBA = "1001"
    
    print(f"\nNota: Asegúrate de que el API esté corriendo en {BASE_URL}")
    print(f"      Usa Ctrl+C para salir\n")
    
    # Pruebas
    test_socio_por_cuit(CUIT_PRUEBA)
    test_socio_por_codigo(CODIGO_PRUEBA)
    
    # Mostrar JSON completo (descomenta si lo necesitas)
    # test_json_completo(cuit=CUIT_PRUEBA)
    
    print("\n" + "="*60)
    print("FIN DE LAS PRUEBAS")
    print("="*60 + "\n")
