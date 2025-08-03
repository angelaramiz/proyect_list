# 📁 Assets Directory Structure

Este directorio contiene todos los recursos visuales organizados por tema.

## 📂 Estructura de Carpetas

```
assets/
├── light/          # Assets para tema claro
│   ├── add.png
│   ├── add.svg
│   ├── complete.png
│   ├── complete.svg
│   ├── delete.png
│   ├── delete.svg
│   ├── logo.png
│   ├── logo.svg
│   ├── paper_bg.png
│   ├── paper_bg.svg
│   ├── theme.png
│   └── theme.svg
├── dark/           # Assets para tema oscuro
│   ├── add.png
│   ├── add.svg
│   ├── complete.png
│   ├── complete.svg
│   ├── delete.png
│   ├── delete.svg
│   ├── logo.png
│   ├── logo.svg
│   ├── paper_bg.png
│   ├── paper_bg.svg
│   ├── theme.png
│   └── theme.svg
└── scripts/        # Scripts de generación
    ├── create_themed_assets.py
    └── svg_to_png.py
```

## 🎨 Descripción de Assets

### Iconos (24x24px)
- **add.png/svg**: Botón para agregar nuevas tareas
- **delete.png/svg**: Botón para eliminar tareas
- **complete.png/svg**: Botón para marcar tareas como completadas
- **theme.png/svg**: Botón para cambiar entre temas

### Logo (40x40px)
- **logo.png/svg**: Logo de la aplicación con estilo cuaderno

### Fondos
- **paper_bg.png/svg**: Fondo tipo papel con líneas de cuaderno

## 🔧 Cómo Funciona

La aplicación automáticamente carga los assets correctos según el tema:
- **Tema Claro**: Carga desde `assets/light/`
- **Tema Oscuro**: Carga desde `assets/dark/`

## 🛠️ Regenerar Assets

Para regenerar todos los assets PNG desde cero:

```bash
cd assets
python create_themed_assets.py
```

## 📝 Notas

- Los archivos SVG son las fuentes originales
- Los archivos PNG son generados automáticamente
- Los assets en la raíz (`assets/`) son copias del tema claro para compatibilidad
