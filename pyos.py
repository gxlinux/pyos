import os

class VirtualFile:
    def __init__(self, name, content=""):
        self.name = name
        self.content = content

class VirtualDirectory:
    def __init__(self, name):
        self.name = name
        self.files = {}

class VirtualFileSystem:
    def __init__(self):
        self.root = VirtualDirectory("root")
        self.current_dir = self.root
        self.path = ["root"]
    
    def lst(self):
        for name in self.current_dir.files:
            print(name)
    
    def gto(self, directory):
        if directory == "..":
            if len(self.path) > 1:
                self.path.pop()
                self.current_dir = self.navigate_to_directory(self.root, self.path[1:])
            else:
                print("Already at root directory")
        elif directory in self.current_dir.files and isinstance(self.current_dir.files[directory], VirtualDirectory):
            self.current_dir = self.current_dir.files[directory]
            self.path.append(directory)
        else:
            print("Directory not found")
        print("Current directory: /" + "/".join(self.path))
    
    def navigate_to_directory(self, start_dir, path):
        current = start_dir
        for p in path:
            if p in current.files and isinstance(current.files[p], VirtualDirectory):
                current = current.files[p]
            else:
                print("Error navigating: Directory not found.")
                return start_dir
        return current
    
    def new(self, directory_name):
        if directory_name in self.current_dir.files:
            print("Directory already exists")
        else:
            self.current_dir.files[directory_name] = VirtualDirectory(directory_name)
            print("Directory created:", directory_name)
    
    def rmv(self, name):
        if name in self.current_dir.files:
            del self.current_dir.files[name]
            print("Removed:", name)
        else:
            print("File or directory not found")
    
    def show(self, file_name):
        if file_name in self.current_dir.files and isinstance(self.current_dir.files[file_name], VirtualFile):
            print("Content of", file_name, ":\n", self.current_dir.files[file_name].content)
        else:
            print("File not found or not a valid file")
    
    def cpy(self, src, dest):
        if src in self.current_dir.files and isinstance(self.current_dir.files[src], VirtualFile):
            self.current_dir.files[dest] = VirtualFile(dest, self.current_dir.files[src].content)
            print("File copied:", src, "->", dest)
        else:
            print("Source file not found or not a valid file")
    
    def mvx(self, src, dest):
        if src in self.current_dir.files:
            self.current_dir.files[dest] = self.current_dir.files[src]
            del self.current_dir.files[src]
            print("Moved or renamed:", src, "->", dest)
        else:
            print("File or directory not found")

    def create_file(self, file_name, content=""):
        if file_name in self.current_dir.files:
            print("File already exists")
        else:
            self.current_dir.files[file_name] = VirtualFile(file_name, content)
            print("File created:", file_name)

    def helpme(self):
        print("""
Comandos disponibles:

lst        : Listar archivos y directorios en el directorio actual.
gto <dir>  : Cambiar al directorio especificado o usar '..' para subir un nivel.
new <dir>  : Crear un nuevo directorio en el directorio actual.
rmv <name> : Eliminar un archivo o directorio.
show <file>: Mostrar el contenido de un archivo.
cpy <src> <dest>: Copiar un archivo.
mvx <src> <dest>: Mover o renombrar un archivo o directorio.
create <file> [content]: Crear un archivo con un contenido opcional.
helpme     : Mostrar esta ayuda.
exit       : Salir de la shell.
        """)

def shell():
    vfs = VirtualFileSystem()
    while True:
        command = raw_input(">>> ").split()
        if len(command) == 0:
            continue
        
        cmd = command[0]
        if cmd == "lst":
            vfs.lst()
        elif cmd == "gto" and len(command) > 1:
            vfs.gto(command[1])
        elif cmd == "new" and len(command) > 1:
            vfs.new(command[1])
        elif cmd == "rmv" and len(command) > 1:
            vfs.rmv(command[1])
        elif cmd == "show" and len(command) > 1:
            vfs.show(command[1])
        elif cmd == "cpy" and len(command) > 2:
            vfs.cpy(command[1], command[2])
        elif cmd == "mvx" and len(command) > 2:
            vfs.mvx(command[1], command[2])
        elif cmd == "create" and len(command) > 1:
            content = " ".join(command[2:]) if len(command) > 2 else ""
            vfs.create_file(command[1], content)
        elif cmd == "helpme":
            vfs.helpme()
        elif cmd == "exit":
            print("Exiting shell...")
            break
        else:
            print("Unrecognized command. Use 'helpme' to see available commands.")

if __name__ == "__main__":
    shell()
