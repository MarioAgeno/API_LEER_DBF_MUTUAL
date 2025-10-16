# API_LEER_DBF_MUTUAL

API desarrollada en FastAPI para consultar información de socios desde archivos DBF (FoxPro), con autenticación por header y estructura de respuesta compatible con Banco BICA.

---

## 🚀 Características

- Lectura directa de archivos `.dbf` (FoxPro)
- Endpoint POST para Banco BICA con estructura específica
- Autenticación por header (`auth-key`)
- Cálculo dinámico del número de cuenta
- Configuración por archivo `.env`
- Desplegable como servicio en Windows usando NSSM

---

## 📦 Requisitos

- Python 3.11+
- FastAPI
- Uvicorn
- dbfread
- python-dotenv

🧪 Ejecución local
uvicorn main:app --host 0.0.0.0 --port 8112

🔐 Seguridad
Opción A: Header fijo
El endpoint /bica/cuentas-mutual requiere el header:

auth-key: 1234567890ABCDEF

Opción B: Token JWT (opcional)
- POST /bica/token con application/x-www-form-urlencoded
- Parámetros: grant_type, Username, Password
- Devuelve un JWT válido por 1 hora
- Usar en Authorization: Bearer <token> en llamadas posteriores

Me encantaría ayudarte con eso, Mario, pero no tengo acceso directo para subir archivos o modificar repositorios en GitHub. Sin embargo, te dejo el contenido listo para que lo copies y pegues en tu archivo  dentro del repositorio :

📄 README.md


⚙️ Configuración
Crear un archivo  en la raíz del proyecto con los siguientes valores:


🧪 Ejecución local


🔐 Seguridad
Opción A: Header fijo
El endpoint  requiere el header:

Opción B: Token JWT (opcional)
• 	POST  con 
• 	Parámetros: , , 
• 	Devuelve un JWT válido por 1 hora
• 	Usar en  en llamadas posteriores

📡 Despliegue como servicio en Windows (NSSM)
1. 	Instalar NSSM desde https://nssm.cc/download
2. 	Crear servicio:

• 	Path: 
• 	Startup directory: 
• 	Arguments: 
3. 	Iniciar servicio:


📥 Ejemplo de request
Entrada
Headers
Respuesta (si existe)
{
  "Existe": true,
  "Convenio": 1234,
  "CuentasMutual": [
    {
      "TipoCuenta": "CA",
      "NumeroCuenta": 123456789
    }
  ]
}

📁 Estructura del proyecto
API_LEER_DBF_MUTUAL/
├── main.py
├── bica_api.py
├── .env
├── README.md

🧠 Autor
Mario Ageno
San Justo, Santa Fe, Argentina
github.com/MarioAgeno
