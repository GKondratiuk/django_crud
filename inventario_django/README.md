# Sistema de Inventario Django

Sistema web de gestión de inventario desarrollado con Django para administrar gestorías y muebles. Permite crear, editar y eliminar registros de gestorías y muebles de manera intuitiva.

## 🚀 Características

- **Autenticación de usuarios**: Sistema de login/logout con protección de rutas
- **Gestión de Gestorías**: CRUD completo para administrar gestorías
- **Gestión de Muebles**: CRUD completo para administrar muebles asociados a gestorías
- **Control de acceso**: Usuarios solo pueden ver y editar sus propias gestorías
- **Interfaz moderna**: Diseño responsivo con Bootstrap 5
- **Panel de administración**: Acceso al panel administrativo de Django para superusuarios

## 📋 Requisitos Previos

- Python 3.12 o superior
- pip (gestor de paquetes de Python)
- Git (para clonar el repositorio)

## 🔧 Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/inventario_django.git
   cd inventario_django
   ```

2. **Crear un entorno virtual**
   ```bash
   python -m venv venv
   ```

3. **Activar el entorno virtual**
   
   En Linux/Mac:
   ```bash
   source venv/bin/activate
   ```
   
   En Windows:
   ```bash
   venv\Scripts\activate
   ```

4. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

5. **Realizar migraciones**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crear un superusuario** (opcional, para acceder al panel de administración)
   ```bash
   python manage.py createsuperuser
   ```

7. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```


## 🔐 Características de Seguridad

- Autenticación requerida para todas las operaciones
- Los usuarios solo pueden acceder a sus propias gestorías
- Protección CSRF en todos los formularios
- Los superusuarios pueden acceder a todas las gestorías

## 🛠️ Tecnologías Utilizadas

- **Django 5.2.7**: Framework web de Python
- **Bootstrap 5.3.2**: Framework CSS para el diseño
- **SQLite**: Base de datos
- **Python 3.12**: Lenguaje de programación

## 📝 Funcionalidades Principales

### Gestorías
- Crear nuevas gestorías
- Editar gestorías existentes
- Eliminar gestorías
- Ver lista de todas las gestorías
- Visualizar muebles asociados a cada gestoría

### Muebles
- Agregar muebles a una gestoría
- Editar información de muebles
- Eliminar muebles
- Ver inventario completo de muebles por gestoría

## 👥 Uso

1. **Crear cuenta**: Regístrese como usuario normal o como superusuario
2. **Iniciar sesión**: Acceda con sus credenciales
3. **Gestionar gestorías**: Cree y administre sus gestorías
4. **Gestionar muebles**: Agregue y administre muebles en cada gestoría

## 📞 Soporte

Para preguntas o sugerencias, por favor abra un issue en el repositorio.

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

