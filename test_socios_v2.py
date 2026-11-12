"""
Script de prueba para verificar los nuevos campos en los endpoints de socios - v2
Incluye pruebas de los campos de integración con AgilPagos
Ejecutar con: python test_socios_v2.py
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
            print("\nDatos Básicos del Socio:")
            print(f"  • Código: {data.get('Codigo')}")
            print(f"  • Nombre: {data.get('Nombre')}")
            print(f"  • CUIT: {data.get('CUIT')}")
            print(f"  • Número DNI: {data.get('Numero Documento')}")
            print(f"  • Trámite DNI: {data.get('Tramite DNI')}")
            
            print("\nDatos de AgilPagos (Cuenta):")
            agilpagos = data.get('AgilPagos', {})
            if agilpagos:
                print(f"  • ID en AgilPagos: {agilpagos.get('id_sg')}")
                print(f"  • ID Usuario: {agilpagos.get('id_user')}")
                print(f"  • Cuenta en Mutual: {agilpagos.get('cuentamutu')}")
                print(f"  • Fecha de Alta: {agilpagos.get('alta')}")
            else:
                print("  (No hay datos de AgilPagos para este socio)")
            
            print("\nDatos de Integración AgilPagos (Catálogos):")
            integracion = data.get('Datos_Integracion_AgilPagos', {})
            if integracion:
                print(f"  • Tipo de Persona (id_sg): {integracion.get('tipo_persona_id_sg')}")
                print(f"  • Actividad (id_sg): {integracion.get('actividad_id_sg')}")
                print(f"  • Estado Civil (id_sg): {integracion.get('estado_civil_id_sg')}")
                print(f"  • Provincia (id_sg): {integracion.get('provincia_id_sg')}")
                print(f"  • País (id_sg): {integracion.get('pais_id_sg')}")
                print(f"  • Situación IVA (id_sg): {integracion.get('situacion_iva_id_sg')}")
            else:
                print("  (No hay datos de integración disponibles)")
            
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
            print("\nDatos Básicos del Socio:")
            print(f"  • Código: {data.get('Codigo')}")
            print(f"  • Nombre: {data.get('Nombre')}")
            print(f"  • CUIT: {data.get('CUIT')}")
            print(f"  • Número DNI: {data.get('Numero Documento')}")
            print(f"  • Trámite DNI: {data.get('Tramite DNI')}")
            
            print("\nDatos de AgilPagos (Cuenta):")
            agilpagos = data.get('AgilPagos', {})
            if agilpagos:
                print(f"  • ID en AgilPagos: {agilpagos.get('id_sg')}")
                print(f"  • ID Usuario: {agilpagos.get('id_user')}")
                print(f"  • Cuenta en Mutual: {agilpagos.get('cuentamutu')}")
                print(f"  • Fecha de Alta: {agilpagos.get('alta')}")
            else:
                print("  (No hay datos de AgilPagos para este socio)")
            
            print("\nDatos de Integración AgilPagos (Catálogos):")
            integracion = data.get('Datos_Integracion_AgilPagos', {})
            if integracion:
                print(f"  • Tipo de Persona (id_sg): {integracion.get('tipo_persona_id_sg')}")
                print(f"  • Actividad (id_sg): {integracion.get('actividad_id_sg')}")
                print(f"  • Estado Civil (id_sg): {integracion.get('estado_civil_id_sg')}")
                print(f"  • Provincia (id_sg): {integracion.get('provincia_id_sg')}")
                print(f"  • País (id_sg): {integracion.get('pais_id_sg')}")
                print(f"  • Situación IVA (id_sg): {integracion.get('situacion_iva_id_sg')}")
            else:
                print("  (No hay datos de integración disponibles)")
            
            return True
        else:
            print(f"\n✗ Error {response.status_code}")
            print(f"  Detalle: {response.json()}")
            return False
    except Exception as e:
        print(f"\n✗ Excepción: {str(e)}")
        return False

def validar_campos_agilpagos(codigo: str):
    """Valida que todos los campos de integración están presentes"""
    print(f"\n{'='*60}")
    print(f"Validación: Campos de Integración AgilPagos")
    print(f"{'='*60}")
    
    try:
        response = requests.get(f"{BASE_URL}/sociocodigo/{codigo}")
        if response.status_code == 200:
            data = response.json()
            integracion = data.get('Datos_Integracion_AgilPagos', {})
            
            campos_esperados = [
                'tipo_persona_id_sg',
                'actividad_id_sg',
                'estado_civil_id_sg',
                'provincia_id_sg',
                'pais_id_sg',
                'situacion_iva_id_sg'
            ]
            
            campos_presentes = 0
            campos_completos = 0
            
            for campo in campos_esperados:
                if campo in integracion:
                    campos_presentes += 1
                    valor = integracion[campo]
                    if valor is not None:
                        campos_completos += 1
                        print(f"  ✓ {campo}: {valor}")
                    else:
                        print(f"  ⚠ {campo}: NULL (no encontrado en tabla)")
                else:
                    print(f"  ✗ {campo}: FALTA")
            
            print(f"\nResumen: {campos_presentes}/6 campos presentes, {campos_completos}/6 con valor")
            return campos_completos == 6
        else:
            print(f"Error {response.status_code}")
            return False
    except Exception as e:
        print(f"Excepción: {str(e)}")
        return False

def test_json_completo(codigo: Optional[str] = None, cuit: Optional[str] = None):
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
    print("TEST DE INTEGRACIÓN AGILPAGOS - ENDPOINTS DE SOCIOS v2")
    print("="*60)
    
    # Cambiar estos valores por datos reales de tu base de datos
    CUIT_PRUEBA = "20123456789"
    CODIGO_PRUEBA = "1001"
    
    print(f"\nNota: Asegúrate de que el API esté corriendo en {BASE_URL}")
    print(f"      Usa Ctrl+C para salir\n")
    
    # Pruebas
    test_socio_por_cuit(CUIT_PRUEBA)
    test_socio_por_codigo(CODIGO_PRUEBA)
    validar_campos_agilpagos(CODIGO_PRUEBA)
    
    # Mostrar JSON completo (descomenta si lo necesitas)
    # test_json_completo(codigo=CODIGO_PRUEBA)
    
    print("\n" + "="*60)
    print("FIN DE LAS PRUEBAS")
    print("="*60 + "\n")
