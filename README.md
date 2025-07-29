# 📝 **Task List App - Ubuntu**  

Aplicación de lista de tareas con **interfaz gráfica (Tkinter)**, cambio de temas (claro/oscuro) y diseño responsive.  
Desarrollada en Python para **Ubuntu** (compatible con otras distribuciones Linux).  

---

## 🚀 **Características**  
✔️ **Añadir, eliminar y marcar tareas** como completadas.  
✔️ **Temas personalizables**: Claro y oscuro (con botón de alternancia).  
✔️ **Interfaz adaptable**: Redimensionable y bien organizada.  
✔️ **Compatibilidad**: Funciona en **Ubuntu** (y otros sistemas con Python + Tkinter).  
✔️ **Emojis y símbolos**: Mejora la experiencia de usuario (opcional).  

---

## 📦 **Requisitos**  
- **Python 3.8+** (incluido en Ubuntu por defecto).  
- **Tkinter**: Biblioteca estándar (verifica si está instalada).  

### 🔍 **Verificar Tkinter en Ubuntu**  
Ejecuta en la terminal:  
```bash
python3 -m tkinter
```
Si no aparece una ventana de prueba, instala Tkinter:  
```bash
sudo apt-get install python3-tk
```

---

## 🛠️ **Instalación y Ejecución**  
1. **Clona o descarga** el repositorio:  
   ```bash
   git clone https://github.com/tu-usuario/task-list-app.git
   cd task-list-app
   ```

2. **Ejecuta la aplicación**:  
   ```bash
   python3 task_app.py
   ```

   *(O usa `python` si tu sistema lo requiere).*  

---

## 🎨 **Personalización**  
### **Cambiar temas**  
- Haz clic en el botón **🌓 Tema Oscuro/Claro** para alternar entre modos.  

### **Modificar colores**  
Edita el diccionario `THEMES` en el código para ajustar los colores:  
```python
THEMES = {
    "light": {
        "bg": "#f0f0f0",  # Fondo de la ventana
        "fg": "#000000",   # Color del texto
        # ... más colores
    },
    "dark": {
        "bg": "#2d2d2d",
        "fg": "#ffffff",
        # ... más colores
    }
}
```
---

## ❓ **Solución de Problemas**  
### **1. Emojis no se muestran (□)**  
- **Causa**: Fuentes incompatibles en Ubuntu.  
- **Solución**:  
  ```bash
  sudo apt-get install fonts-noto-color-emoji
  ```
  Luego, reinicia la aplicación.  

### **2. Error `ModuleNotFoundError: No module named 'tkinter'`**  
- **Solución**: Instala Tkinter:  
  ```bash
  sudo apt-get install python3-tk
  ```

---

**🎉 ¡Organiza tus tareas con estilo en Ubuntu!** 🎉  

--- 

### 📂 **Estructura del Proyecto**  
```
proyect_list/
├── run.py       # Código principal
├── README.md         # Este archivo
└── requirements.txt  # (Opcional) Dependencias
```  
