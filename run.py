import tkinter as tk
from tkinter import messagebox

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

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.current_theme = "light"
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        # Configuración de la ventana
        self.root.title("Lista de Tareas - Temas")
        self.root.geometry("500x500")
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Widgets
        self.task_entry = tk.Entry(self.root, font=("Arial", 14))
        self.task_entry.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.add_button = tk.Button(self.root, text="+ Añadir", command=self.add_task)
        self.add_button.grid(row=0, column=1, padx=5, pady=10)

        self.task_listbox = tk.Listbox(self.root, font=("Arial", 14))
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")

        self.delete_button = tk.Button(self.root, text="X Eliminar", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=5, pady=10, sticky="ew")

        self.complete_button = tk.Button(self.root, text="✓ Completar", command=self.mark_complete)
        self.complete_button.grid(row=2, column=1, padx=5, pady=10, sticky="ew")

        # Botón para cambiar tema
        self.theme_button = tk.Button(
            self.root, 
            text="🌓 Tema Oscuro", 
            command=self.toggle_theme
        )
        self.theme_button.grid(row=3, column=0, columnspan=2, pady=5)

    def apply_theme(self):
        theme = THEMES[self.current_theme]
        # Aplicar colores a la ventana y widgets
        self.root.config(bg=theme["bg"])
        self.task_entry.config(
            bg=theme["entry_bg"], 
            fg=theme["fg"], 
            insertbackground=theme["fg"]
        )
        self.task_listbox.config(
            bg=theme["listbox_bg"], 
            fg=theme["fg"], 
            selectbackground=theme["highlight"]
        )
        for button in [self.add_button, self.delete_button, self.complete_button, self.theme_button]:
            button.config(
                bg=theme["button_bg"], 
                fg=theme["fg"], 
                activebackground=theme["highlight"],
                activeforeground=theme["fg"]
            )

    def toggle_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.theme_button.config(
            text="🌓 Tema Claro" if self.current_theme == "dark" else "🌓 Tema Oscuro"
        )
        self.apply_theme()

    # Funciones de la lista de tareas
    def add_task(self):
        if task := self.task_entry.get():
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Error", "¡Ingresa una tarea!")

    def delete_task(self):
        try:
            self.task_listbox.delete(self.task_listbox.curselection()[0])
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
        except IndexError:
            messagebox.showwarning("Error", "Selecciona una tarea para marcar")

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
