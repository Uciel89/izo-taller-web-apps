# Proyecto Final

Este proyecto es una aplicación backend desarrollada con FastAPI y SQLAlchemy.

## Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)


### Creación de entorno virtual y configuración

Para crear un entorno virtual, ejecuta el siguiente comando:

- En Windows:
  ```sh
  python -m venv venv
    ```
- En Linux:
```
python3 -m venv venv
```
Activar Entorno VirtualPara activar el entorno virtual, usa el siguiente comando:
- En Windows:
```
venv\Scripts\activate
```
- En Linux:
```
source venv/bin/activate
```
Instalar DependenciasCon el entorno virtual activado, instala los paquetes necesarios ejecutando:
```
pip install -r requirements.txt
```
#### Configuración de la Base de Datos

Crea un directorio uploads dentro del backend y un archivo .env en la raíz del proyecto con la variable DB_PATH. Ejemplo:
```
DB_PATH='seminario.db'
```
Ejecución del ProyectoPara ejecutar el proyecto, sigue estos pasos:
- Navega al directorio del backend:
```
cd proyecto-final/backend
```
- Inicia la aplicación con Hypercorn:
```
hypercorn main:app
```