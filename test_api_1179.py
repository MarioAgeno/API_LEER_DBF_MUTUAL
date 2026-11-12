"""Script para probar el endpoint de la API con socio 1179"""
import requests
import json
import time

# Esperar a que la API esté lista
time.sleep(3)

try:
    # Probar el endpoint /sociocodigo/1179
    url = "http://127.0.0.1:8000/sociocodigo/1179"
    print(f"Realizando GET {url}")
    
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("\n" + "=" * 80)
        print("RESPUESTA DEL API - SOCIO 1179")
        print("=" * 80)
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        # Verificar campos de integración
        print("\n" + "=" * 80)
        print("CAMPOS DE INTEGRACION AGILPAGOS")
        print("=" * 80)
        
        if 'Datos_Integracion_AgilPagos' in data:
            campos = data['Datos_Integracion_AgilPagos']
            print(f"tipo_persona_id_sg:     {campos.get('tipo_persona_id_sg')}")
            print(f"actividad_id_sg:        {campos.get('actividad_id_sg')}")
            print(f"estado_civil_id_sg:     {campos.get('estado_civil_id_sg')}")
            print(f"provincia_id_sg:        {campos.get('provincia_id_sg')}")
            print(f"pais_id_sg:             {campos.get('pais_id_sg')}")
            print(f"situacion_iva_id_sg:    {campos.get('situacion_iva_id_sg')}")
            
            # Verificar que ninguno sea null
            valores = list(campos.values())
            if all(v is not None for v in valores):
                print("\nOK - TODOS LOS CAMPOS TIENEN VALORES")
            else:
                nulos = [k for k, v in campos.items() if v is None]
                print(f"\nADVERTENCIA - CAMPOS NULL: {nulos}")
        else:
            print("ERROR - Campo 'Datos_Integracion_AgilPagos' no encontrado en respuesta")
    else:
        print(f"ERROR: Status code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
