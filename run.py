
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
        self.apply_theme()

    def load_icons(self):
        icons = {}
        def svg_to_imgtk(svg_file, size=(24,24)):
            # Convert SVG to PNG in memory using Pillow (requires cairosvg for real SVG, here we use PNG fallback)
            # For simplicity, we use PNG fallback (Pillow can't open SVG directly)
            # You can convert SVG to PNG manually if needed
            # For now, just return a blank image if SVG not supported
            try:
                from cairosvg import svg2png
                import io
                with open(svg_file, 'rb') as f:
                    png_data = svg2png(bytestring=f.read(), output_width=size[0], output_height=size[1])
                return ImageTk.PhotoImage(Image.open(io.BytesIO(png_data)).resize(size, Image.LANCZOS))
            except Exception:
                # fallback: try to open as PNG if exists
                png_file = svg_file.replace('.svg', '.png')
                if os.path.exists(png_file):
                    return ImageTk.PhotoImage(Image.open(png_file).resize(size, Image.LANCZOS))
                # fallback: blank
                return ImageTk.PhotoImage(Image.new('RGBA', size, (200,200,200,0)))
        icons['logo'] = svg_to_imgtk(os.path.join(self.assets_path, 'logo.svg'), (40,40))
        icons['add'] = svg_to_imgtk(os.path.join(self.assets_path, 'add.svg'))
        icons['delete'] = svg_to_imgtk(os.path.join(self.assets_path, 'delete.svg'))
        icons['complete'] = svg_to_imgtk(os.path.join(self.assets_path, 'complete.svg'))
        icons['theme'] = svg_to_imgtk(os.path.join(self.assets_path, 'theme.svg'))
        return icons


    def setup_ui(self):
        self.root.title("Lista de Tareas - Temas")
        self.root.geometry("520x570")
        self.root.minsize(400, 500)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Fondo tipo hoja de papel
        try:
            from cairosvg import svg2png
            import io
            svg_path = os.path.join(self.assets_path, 'paper_bg.svg')
            with open(svg_path, 'rb') as f:
                png_data = svg2png(bytestring=f.read(), output_width=520, output_height=570)
            self.bg_img = ImageTk.PhotoImage(Image.open(io.BytesIO(png_data)))
        except Exception:
            # fallback: fondo blanco
            self.bg_img = None
        if self.bg_img:
            self.bg_label = tk.Label(self.root, image=self.bg_img, borderwidth=0)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Logo y título
        logo_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        logo_frame.grid(row=0, column=0, columnspan=2, pady=(10,0), sticky="ew")
        logo_label = tk.Label(logo_frame, image=self.icons['logo'], bg=THEMES[self.current_theme]["bg"])
        logo_label.pack(side="left", padx=(10,5))
        title_label = tk.Label(logo_frame, text="Lista de Tareas", font=("Segoe UI", 20, "bold"), bg=THEMES[self.current_theme]["bg"])
        title_label.pack(side="left", padx=5)

        # Entrada y botón añadir
        entry_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        entry_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(10,0))
        entry_frame.grid_columnconfigure(0, weight=1)
        self.task_entry = tk.Entry(entry_frame, font=("Segoe UI", 14), relief="flat", bd=2)
        self.task_entry.grid(row=0, column=0, sticky="ew", padx=(0,5), ipady=4)
        self.add_button = tk.Button(entry_frame, image=self.icons['add'], command=self.add_task, relief="flat", bd=0, width=36, height=36, bg=THEMES[self.current_theme]["button_bg"])
        self.add_button.grid(row=0, column=1, padx=(0,0))
        ToolTip(self.add_button, "Añadir tarea")

        # Lista de tareas con scrollbar
        list_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        list_frame.grid_rowconfigure(0, weight=1)
        list_frame.grid_columnconfigure(0, weight=1)
        self.task_listbox = tk.Listbox(list_frame, font=("Segoe UI", 14), relief="flat", selectmode=tk.SINGLE, activestyle="none", highlightthickness=1)
        self.task_listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Botones de acción
        btn_frame = tk.Frame(self.root, bg=THEMES[self.current_theme]["bg"])
        btn_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,5))
        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)
        self.delete_button = tk.Button(btn_frame, image=self.icons['delete'], command=self.delete_task, relief="flat", bd=0, width=36, height=36, bg=THEMES[self.current_theme]["button_bg"])
        self.delete_button.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        ToolTip(self.delete_button, "Eliminar tarea seleccionada")
        self.complete_button = tk.Button(btn_frame, image=self.icons['complete'], command=self.mark_complete, relief="flat", bd=0, width=36, height=36, bg=THEMES[self.current_theme]["button_bg"])
        self.complete_button.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        ToolTip(self.complete_button, "Marcar tarea como completada")

        # Botón de tema
        self.theme_button = tk.Button(self.root, image=self.icons['theme'], command=self.toggle_theme, relief="flat", bd=0, width=36, height=36, bg=THEMES[self.current_theme]["button_bg"])
        self.theme_button.grid(row=4, column=0, columnspan=2, pady=(0,5))
        ToolTip(self.theme_button, "Cambiar tema claro/oscuro")

        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, anchor="w", font=("Segoe UI", 10), bg=THEMES[self.current_theme]["bg"], fg=THEMES[self.current_theme]["fg"])
        self.status_bar.grid(row=5, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,5))
        self.update_status()

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        self.root.config(bg=theme["bg"])
        # Actualizar widgets
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame) or isinstance(widget, tk.Label):
                widget.config(bg=theme["bg"])
        self.task_entry.config(bg=theme["entry_bg"], fg=theme["fg"], insertbackground=theme["fg"])
        self.task_listbox.config(bg=theme["listbox_bg"], fg=theme["fg"], selectbackground=theme["highlight"], highlightbackground=theme["highlight"])
        for btn in [self.add_button, self.delete_button, self.complete_button, self.theme_button]:
            btn.config(bg=theme["button_bg"], activebackground=theme["highlight"], activeforeground=theme["fg"])
        self.status_bar.config(bg=theme["bg"], fg=theme["fg"])

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.icons = self.load_icons()  # recargar íconos para el nuevo tema si es necesario
        self.apply_theme()

    # Funciones de la lista de tareas
    def add_task(self):
        if task := self.task_entry.get().strip():
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
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
