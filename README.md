# Gestor de Pacientes Web

Aplicación web para gestionar pacientes, inspirada en la versión Python de escritorio. Permite:  

- Registro de pacientes con datos detallados (provincia, municipio, nombre, edad, grupo dispensarial, escolaridad, ocupación, color de piel, factores de riesgo, enfermedades, discapacidades, lactante, mujer en edad fértil, etc.)  
- Búsqueda rápida y resaltado de resultados  
- Filtro avanzado de registros  
- Eliminación de pacientes  
- Exportación de la base de datos a Excel  

La aplicación utiliza **Flask** y **SQLite** como backend, y HTML/CSS/JS en frontend.

---

## Estructura del proyecto

```text
GestorPacientesWeb/
├─ app.py
├─ pacientes.db      # Se crea automáticamente al ejecutar la app
├─ requirements.txt
├─ templates/
│  └─ index.html
└─ static/
   ├─ style.css
   └─ script.js
```
---

## Requisitos

- Python 3.8 o superior  
- Pip  

Instala dependencias con:

```bash
pip install -r requirements.txt
```

requirements.txt debe incluir:
Flask==2.3.3
pandas==2.1.1
openpyxl==3.1.2

---

1. Ejecutar la aplicación

Desde la carpeta del proyecto:

Crear y activar un entorno virtual (opcional pero recomendado):

Linux / Mac:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar la aplicación:
```bash
python app.py
```

Por defecto se ejecutará en:
```cpp
http://0.0.0.0:5000
```

---

Acceso desde dispositivos en la misma red

1. Asegúrate de que tu computadora y tu móvil estén conectados al mismo router.

2. Encuentra tu IP local (ejemplo en Linux/Mac: ifconfig o ip a, en Windows: ipconfig).
Ejemplo: 192.168.1.100

3. Desde el navegador del móvil ingresa:
```cpp
http://192.168.1.100:5000
```

Ahora podrás ver el formulario y la tabla de pacientes en tu móvil.

---

Funcionalidades

* Agregar paciente: Completa el formulario y presiona "Agregar paciente".

* Lactante y mujer en edad fértil: Se calculan automáticamente según la edad y el sexo.

* Búsqueda rápida: Escribe cualquier texto y la tabla se filtrará y resaltará automáticamente.

* Filtro avanzado: Permite seleccionar múltiples criterios para filtrar los pacientes.

* Eliminar paciente: Presiona el botón "Eliminar" en la fila correspondiente.

* Exportar a Excel: Descarga todos los registros en formato .xlsx.

---

Notas importantes

* No es necesario subir pacientes.db al repositorio; se creará automáticamente al ejecutar app.py.

* Los campos que permiten múltiples valores (factor de riesgo, enfermedades, discapacidades, riesgo preconcepcional) deben separarse por comas ,.

* La aplicación está lista para pruebas en red local. Para un entorno productivo, se recomienda desplegar en un servidor web interno o externo seguro.

---

Licencia

Este proyecto está bajo la licencia MIT.
Este proyecto es para uso educativo y profesional dentro de entornos médicos.
