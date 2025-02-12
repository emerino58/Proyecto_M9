# ⚽ Aplicación Dash - Campeonato ANFP Zona Central Sub-16

## 📌 Descripción
Esta aplicación web, desarrollada con **Python y Dash**, permite visualizar estadísticas futbolísticas y antropométricas de los jugadores del **Campeonato ANFP Zona Central Sub-16**.

## 🚀 Funcionalidades
✔ **Inicio de sesión** con validación de usuario y contraseña.  
✔ **Tabla de posiciones** ordenada por puntos, con opción de visualización gráfica.  
✔ **Estadísticas de jugadores**, incluyendo comparaciones y gráficos interactivos.  
✔ **Datos antropométricos**, con gráficos y tablas interactivas.  
✔ **Exportación a PDF e impresión** de dashboards.  

## 📂 Estructura del Proyecto
Campeonato_ANFP_Sub16/
│── app.py  # Archivo principal que ejecuta la aplicación
│── requirements.txt  # Librerías necesarias para la app
│── assets/  # Archivos CSS, imágenes y scripts JS
│   ├── style.css  # Estilos para la app
│   ├── logo.png  # Logo federativo
│── data/  # Archivos de datos
│   ├── tabla_puntajes_futbol.xlsx
│   ├── DataSets_Sub16.xlsx
│   ├── Data_Antropometrica.xlsx
│   ├── Usuarios.xlsx
│── modules/  # Módulos de la aplicación
│   ├── login.py  # Módulo de autenticación
│   ├── mod_tabla_posiciones.py  # Tabla de posiciones
│   ├── mod_estadisticas.py  # Estadísticas de jugadores
│   ├── mod_antropometria.py  # Datos antropométricos
│── templates/  # Documentación y archivos para despliegue
│   ├── readme.md
│   ├── deployment_guide.docx
