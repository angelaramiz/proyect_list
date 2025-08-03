
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import os

# Paletas de colores para los temas
THEMES = {
    "light": {
        "bg": "#f0f0f0",
        "fg": "#000000",
        "entry_bg": "#ffffff",
        "listbox_bg": "#ffffff",
        "button_bg": "#dddddd",
        "highlight": "#a6a6a6"
    },
    "dark": {
        "bg": "#2d2d2d",
        "fg": "#ffffff",
        "entry_bg": "#3d3d3d",
        "listbox_bg": "#3d3d3d",
        "button_bg": "#5d5d5d",
        "highlight": "#7d7d7d"
    }
}


class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)
        
    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 30
        y = y + cy + self.widget.winfo_rooty() + 20
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1, font=("Segoe UI", 10))
        label.pack(ipadx=4)
        
    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()


class TaskApp:
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"
        self.assets_path = os.path.join(os.path.dirname(__file__), "assets")
        self.icons = self.load_icons()
        self.setup_ui()

    def load_icons(self):
        icons = {}
        self._icon_refs = []  # Mantener referencias vivas
        
        def png_to_imgtk(png_file, size=(24,24)):
            if not os.path.exists(png_file):
                print(f"[ERROR] No se encontró el archivo: {png_file}")
                img = ImageTk.PhotoImage(Image.new('RGBA', size, (255,0,0,128)))
                self._icon_refs.append(img)
                return img
            try:
                img = ImageTk.PhotoImage(Image.open(png_file).resize(size, Image.LANCZOS))
                self._icon_refs.append(img)
                return img
            except Exception as e:
                print(f"❌ Error al cargar {png_file}: {e}")
                img = ImageTk.PhotoImage(Image.new('RGBA', size, (255,0,0,128)))
                self._icon_refs.append(img)
                return img
        
        # Determinar carpeta del tema
        theme_folder = "dark" if self.current_theme == "dark" else "light"
        theme_path = os.path.join(self.assets_path, theme_folder)
        
        # Cargar iconos con tamaños más grandes para mejor visibilidad
        icons['logo'] = png_to_imgtk(os.path.join(theme_path, 'logo.png'), (40,40))
        icons['add'] = png_to_imgtk(os.path.join(theme_path, 'add.png'), (32,32))
        icons['delete'] = png_to_imgtk(os.path.join(theme_path, 'delete.png'), (32,32))
        icons['complete'] = png_to_imgtk(os.path.join(theme_path, 'complete.png'), (32,32))
        icons['theme'] = png_to_imgtk(os.path.join(theme_path, 'theme.png'), (32,32))
        
        return icons

    def setup_ui(self):
        self.root.title("Lista de Tareas - Temas")
        self.root.geometry("520x570")
        self.root.minsize(400, 500)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Fondo tipo hoja de papel (PNG) específico del tema
        theme_folder = "dark" if self.current_theme == "dark" else "light"
        bg_path = os.path.join(self.assets_path, theme_folder, 'paper_bg.png')
        if os.path.exists(bg_path):
            self.bg_img = ImageTk.PhotoImage(Image.open(bg_path).resize((520,570), Image.LANCZOS))
        else:
            print(f"[ERROR] No se encontró el fondo PNG: {bg_path}")
            self.bg_img = None
        if self.bg_img:
            self.bg_label = tk.Label(self.root, image=self.bg_img, borderwidth=0)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.bg_label.lower()  # Asegura que el fondo esté detrás de todo

        # Logo y título
        self.logo_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        self.logo_frame.grid(row=0, column=0, columnspan=2, pady=(10,0), sticky="ew")
        self.logo_label = tk.Label(self.logo_frame, image=self.icons['logo'], bg=THEMES[self.current_theme]["bg"])
        self.logo_label.pack(side="left", padx=(10,5))
        self.title_label = tk.Label(self.logo_frame, text="Lista de Tareas", font=("Segoe UI", 20, "bold"), bg=THEMES[self.current_theme]["bg"])
        self.title_label.pack(side="left", padx=5)

        # Entrada y botón añadir
        self.entry_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        self.entry_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(10,0))
        self.entry_frame.grid_columnconfigure(0, weight=1)
        self.task_entry = tk.Entry(self.entry_frame, font=("Segoe UI", 14), relief="flat", bd=2, bg=THEMES[self.current_theme]["entry_bg"], fg=THEMES[self.current_theme]["fg"])
        self.task_entry.grid(row=0, column=0, sticky="ew", padx=(0,5), ipady=4)
        self.placeholder_text = "Escribe una tarea..."
        
        self.add_button = tk.Button(self.entry_frame, image=self.icons['add'], command=self.add_task, relief="raised", bd=2, bg="#ffffff", padx=3, pady=3)
        self.add_button.grid(row=0, column=1, padx=(5,0), pady=2)
        ToolTip(self.add_button, "Añadir tarea")

        # Lista de tareas con scrollbar
        self.list_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        self.list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)
        
        # Fondo tipo hoja en el área de la lista específico del tema
        theme_folder = "dark" if self.current_theme == "dark" else "light"
        list_bg_path = os.path.join(self.assets_path, theme_folder, 'paper_bg.png')
        if os.path.exists(list_bg_path):
            self.list_bg_img = ImageTk.PhotoImage(Image.open(list_bg_path).resize((480,300), Image.LANCZOS))
            self.list_bg_label = tk.Label(self.list_frame, image=self.list_bg_img, borderwidth=0)
            self.list_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.list_bg_label.lower()
            
        self.task_listbox = tk.Listbox(self.list_frame, font=("Segoe UI", 14), relief="flat", selectmode=tk.SINGLE, activestyle="none", highlightthickness=1, bg=THEMES[self.current_theme]["listbox_bg"], fg=THEMES[self.current_theme]["fg"])
        self.task_listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Botones de acción
        self.btn_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        self.btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,5))
        self.btn_frame.grid_columnconfigure(0, weight=1)
        self.btn_frame.grid_columnconfigure(1, weight=1)
        
        self.delete_button = tk.Button(self.btn_frame, image=self.icons['delete'], command=self.delete_task, relief="raised", bd=2, bg="#ffffff", padx=3, pady=3)
        self.delete_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        ToolTip(self.delete_button, "Eliminar tarea seleccionada")
        
        self.complete_button = tk.Button(self.btn_frame, image=self.icons['complete'], command=self.mark_complete, relief="raised", bd=2, bg="#ffffff", padx=3, pady=3)
        self.complete_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(self.complete_button, "Marcar tarea como completada")
        
        self.btn_frame.lift()  # Asegura que los botones estén por encima de cualquier fondo

        # Botón de tema
        self.theme_button = tk.Button(self.root, image=self.icons['theme'], command=self.toggle_theme, relief="raised", bd=2, bg="#ffffff", padx=3, pady=3)
        self.theme_button.grid(row=4, column=0, columnspan=2, pady=(5,5))
        ToolTip(self.theme_button, "Cambiar tema claro/oscuro")

        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, anchor="w", font=("Segoe UI", 10), fg=THEMES[self.current_theme]["fg"], bg=THEMES[self.current_theme]["bg"])
        self.status_bar.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,5))
        
        # Inicializar status y placeholder después de crear todos los widgets
        self.update_status()
        self._setup_placeholder()
        self.apply_theme()

    def _setup_placeholder(self):
        """Configura el placeholder y los bindings del Entry"""
        self.task_entry.insert(0, self.placeholder_text)
        self.task_entry.config(fg="#888888")
        self.task_entry.bind("<FocusIn>", self._clear_placeholder)
        self.task_entry.bind("<FocusOut>", self._add_placeholder)
        self.task_entry.bind("<FocusIn>", self._highlight_entry, add='+')
        self.task_entry.bind("<FocusOut>", self._unhighlight_entry, add='+')
        
    def _clear_placeholder(self, event):
        if self.task_entry.get() == self.placeholder_text:
            self.task_entry.delete(0, tk.END)
            self.task_entry.config(fg=THEMES[self.current_theme]["fg"])

    def _add_placeholder(self, event):
        if not self.task_entry.get():
            self.task_entry.insert(0, self.placeholder_text)
            self.task_entry.config(fg="#888888")

    def _highlight_entry(self, event):
        self.task_entry.config(highlightthickness=2, highlightbackground=THEMES[self.current_theme]["highlight"], highlightcolor=THEMES[self.current_theme]["highlight"])

    def _unhighlight_entry(self, event):
        self.task_entry.config(highlightthickness=0)

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        self.root.config(bg=theme["bg"])
        
        # Cambiar fondo de frames y labels principales
        self.logo_frame.config(bg=theme["bg"])
        self.logo_label.config(bg=theme["bg"])
        self.title_label.config(bg=theme["bg"], fg=theme["fg"])
        self.entry_frame.config(bg=theme["bg"])
        self.list_frame.config(bg=theme["bg"])
        self.btn_frame.config(bg=theme["bg"])
        
        # Cambiar fondo y color de widgets principales
        self.task_entry.config(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
        self.task_listbox.config(bg=theme["listbox_bg"], fg=theme["fg"], selectbackground=theme["highlight"], highlightbackground=theme["highlight"])
        
        # Mantener fondo blanco en botones con iconos para mejor contraste
        for btn in [self.add_button, self.delete_button, self.complete_button, self.theme_button]:
            btn.config(bg="#ffffff", activebackground=theme["highlight"], activeforeground=theme["fg"])
            
        self.status_bar.config(bg=theme["bg"], fg=theme["fg"])

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.icons = self.load_icons()  # recargar íconos para el nuevo tema si es necesario
        
        # Actualizar imágenes de los botones y logo
        self.add_button.config(image=self.icons['add'])
        self.delete_button.config(image=self.icons['delete'])
        self.complete_button.config(image=self.icons['complete'])
        self.theme_button.config(image=self.icons['theme'])
        self.logo_label.config(image=self.icons['logo'])
        
        # Actualizar fondos de papel
        self._update_backgrounds()
        
        self.apply_theme()

    def _update_backgrounds(self):
        """Actualiza los fondos de papel según el tema actual"""
        theme_folder = "dark" if self.current_theme == "dark" else "light"
        
        # Actualizar fondo principal
        bg_path = os.path.join(self.assets_path, theme_folder, 'paper_bg.png')
        if os.path.exists(bg_path):
            self.bg_img = ImageTk.PhotoImage(Image.open(bg_path).resize((520,570), Image.LANCZOS))
            self.bg_label.config(image=self.bg_img)
        
        # Actualizar fondo de la lista
        if hasattr(self, 'list_bg_label'):
            list_bg_path = os.path.join(self.assets_path, theme_folder, 'paper_bg.png')
            if os.path.exists(list_bg_path):
                self.list_bg_img = ImageTk.PhotoImage(Image.open(list_bg_path).resize((480,300), Image.LANCZOS))
                self.list_bg_label.config(image=self.list_bg_img)

    # Funciones de la lista de tareas
    def add_task(self):
        task = self.task_entry.get().strip()
        if task and task != self.placeholder_text:
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
            self._add_placeholder(None)
            self.update_status()
        else:
            messagebox.showwarning("Error", "¡Ingresa una tarea!")

    def delete_task(self):
        try:
            self.task_listbox.delete(self.task_listbox.curselection()[0])
            self.update_status()
        except IndexError:
            messagebox.showwarning("Error", "Selecciona una tarea para eliminar")

    def mark_complete(self):
        try:
            idx = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(idx)
            if not task.startswith("✓ "):
                self.task_listbox.delete(idx)
                self.task_listbox.insert(idx, f"✓ {task}")
                self.task_listbox.itemconfig(idx, fg="gray")
                self.update_status()
        except IndexError:
            messagebox.showwarning("Error", "Selecciona una tarea para marcar")

    def update_status(self):
        total = self.task_listbox.size()
        completadas = sum(1 for i in range(total) if self.task_listbox.get(i).startswith("✓ "))
        self.status_var.set(f"Tareas: {total}  |  Completadas: {completadas}")


# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
