import os
import tarfile
import tkinter as tk
from tkinter import filedialog, messagebox

def descomprimir_mbz():
    archivo_mbz = filedialog.askopenfilename(title="Seleccionar archivo .mbz", filetypes=[("MBZ files", "*.mbz")])
    if not archivo_mbz:
        return
    
    # Crear carpeta de salida
    carpeta_destino = os.path.splitext(archivo_mbz)[0] + "_extracted"
    os.makedirs(carpeta_destino, exist_ok=True)
    
    try:
        # Descomprimir .mbz (que es un .tar.gz)
        with tarfile.open(archivo_mbz, "r:gz") as tar:
            tar.extractall(carpeta_destino)
        messagebox.showinfo("Éxito", f"Archivo descomprimido en:\n{carpeta_destino}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo descomprimir:\n{str(e)}")

def comprimir_mbz():
    carpeta_origen = filedialog.askdirectory(title="Seleccionar carpeta para comprimir")
    if not carpeta_origen:
        return
    
    archivo_mbz = filedialog.asksaveasfilename(title="Guardar como .mbz", defaultextension=".mbz", filetypes=[("MBZ files", "*.mbz")])
    if not archivo_mbz:
        return
    
    try:
        # Comprimir a .tar.gz y renombrar a .mbz
        with tarfile.open(archivo_mbz, "w:gz") as tar:
            tar.add(carpeta_origen, arcname=os.path.basename(carpeta_origen))
        messagebox.showinfo("Éxito", f"Archivo .mbz creado:\n{archivo_mbz}")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo comprimir:\n{str(e)}")

# Interfaz gráfica simple
root = tk.Tk()
root.title("Editor MBZ")
root.geometry("300x100")

btn_descomprimir = tk.Button(root, text="Descomprimir MBZ", command=descomprimir_mbz)
btn_descomprimir.pack(pady=5)

btn_comprimir = tk.Button(root, text="Comprimir a MBZ", command=comprimir_mbz)
btn_comprimir.pack(pady=5)

root.mainloop()