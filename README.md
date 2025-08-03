# � Project List - Aplicación de Lista de Tareas

Una aplicación Python de lista de tareas con soporte para temas claro y oscuro.

## 📂 Estructura del Proyecto

```
proyect_list/
├── README.md           # Este archivo
├── requirements.txt    # Dependencias del proyecto
├── run.py             # Archivo principal de la aplicación
└── assets/            # Recursos visuales
    ├── light/         # Assets para tema claro (solo PNG)
    │   ├── add.png
    │   ├── complete.png
    │   ├── delete.png
    │   ├── logo.png
    │   ├── paper_bg.png
    │   └── theme.png
    └── dark/          # Assets para tema oscuro (solo PNG)
        ├── add.png
        ├── complete.png
        ├── delete.png
        ├── logo.png
        ├── paper_bg.png
        └── theme.png
```

## 🚀 Instalación y Configuración

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/angelaramiz/proyect_list.git
   cd proyect_list
   ```

2. **Crea un entorno virtual:**
   ```bash
   python -m venv env
   ```

3. **Activa el entorno virtual:**
   - En Windows:
     ```bash
     env\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source env/bin/activate
     ```

4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Ejecuta la aplicación:**
   ```bash
   python run.py
   ```

## 🎨 Recursos Visuales

La aplicación incluye assets optimizados para ambos temas:

### Iconos (24x24px)
- **add.png**: Botón para agregar nuevas tareas
- **delete.png**: Botón para eliminar tareas
- **complete.png**: Botón para marcar tareas como completadas
- **theme.png**: Botón para cambiar entre temas

### Logo (40x40px)
- **logo.png**: Logo de la aplicación con estilo cuaderno

### Fondos
- **paper_bg.png**: Fondo tipo papel con líneas de cuaderno

## ⚡ Características

- ✅ Gestión completa de tareas (crear, eliminar, completar)
- 🎨 Soporte para temas claro y oscuro
- 📱 Interfaz intuitiva y fácil de usar
- 🖼️ Assets optimizados para cada tema
- 💾 Persistencia de datos local

## � Cómo Funciona

La aplicación automáticamente carga los assets correctos según el tema seleccionado:
- **Tema Claro**: Carga desde `assets/light/`
- **Tema Oscuro**: Carga desde `assets/dark/`
