import Tkinter as tk
import ttk
import tkMessageBox

class VirtualFileSystemExplorer:
    def __init__(self, master):
        self.master = master
        self.master.title("Explorador de Archivos - pyos")
        
        # Definir el sistema de archivos virtual
        self.filesystem = {
            "pyos": {
                "home": {
                    "user": {
                        "file1.txt": "Contenido de file1.txt",
                        "file2.txt": "Contenido de file2.txt"
                    }
                },
                "etc": {
                    "config.cfg": "Configuraciones del sistema"
                },
                "var": {
                    "log": {
                        "system.log": "Logs del sistema"
                    }
                }
            }
        }
        
        self.current_dir = self.filesystem['pyos']  # Comienza desde 'pyos'
        self.path = ['pyos']
        
        # Crear widgets
        self.create_widgets()
        
        # Cargar la lista de archivos y directorios
        self.update_listbox()

    def create_widgets(self):
        # Listbox para mostrar archivos y carpetas
        self.listbox = tk.Listbox(self.master, height=15, width=50)
        self.listbox.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
       
        self.back_button = tk.Button(self.master, text="Subir Nivel", command=self.go_up)
        self.back_button.grid(row=1, column=0, padx=10, pady=5)
        
        self.open_button = tk.Button(self.master, text="Abrir", command=self.open_item)
        self.open_button.grid(row=1, column=1, padx=10, pady=5)
        
        # Etiqueta para mostrar la ruta actual
        self.path_label = tk.Label(self.master, text="/pyos")
        self.path_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def update_listbox(self):
        # Limpiar la lista actual
        self.listbox.delete(0, tk.END)
        
        
        for item in self.current_dir:
            self.listbox.insert(tk.END, item)
        
        # Actualizar la etiqueta de la ruta
        self.path_label.config(text="/" + "/".join(self.path))

    def go_up(self):
        if len(self.path) > 1:
            self.path.pop()  
            self.current_dir = self.navigate_to_directory(self.filesystem, self.path)
            self.update_listbox()

    def open_item(self):
        
        selected = self.listbox.curselection()
        if selected:
            item = self.listbox.get(selected[0])
            if isinstance(self.current_dir[item], dict):  # Si es un directorio
                self.path.append(item)  # Bajar a este directorio
                self.current_dir = self.current_dir[item]
                self.update_listbox()
            else:  # Si es un archivo, mostrar contenido
                tkMessageBox.showinfo("Contenido de " + item, self.current_dir[item])

    def navigate_to_directory(self, start_dir, path):
        current = start_dir
        for p in path:
            current = current[p]
        return current

if __name__ == "__main__":
    root = tk.Tk()
    explorer = VirtualFileSystemExplorer(root)
    root.mainloop()
