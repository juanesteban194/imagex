import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from app.Clases_principales.Editorimagen import EditorImagen


class InterfazEditor:

    def __init__(self):
        self.editor = EditorImagen()
        self.ventana = tk.Tk()
        self.ventana.title("Editor de Imágenes")
        self.ventana.geometry("600x400")

        # Botón para cargar imagen
        btn_cargar = tk.Button(self.ventana, text = " Cargar Imagen", command = self.cargar_imagen)
        btn_cargar.pack(pady=10)

        # Área para mostrar imagen
        self.label_imagen = tk.Label(self.ventana, text = " Imagen no cargada ")
        self.label_imagen.pack()

        self.ventana.mainloop()

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes = [("Imágenes", "*.jpg *.jpeg " )])
        if ruta:
            self.editor.cargar_imagen(ruta)
            img: ImageTk.PhotoImage = ImageTk.PhotoImage(self.editor.imagen_editada.resize((300, 300)))
            self.label_imagen.configure( image = img)
            self.label_imagen.image = img  #guarda referencia a la imagen o no se mostrará
        else:
            messagebox.showinfo("Aviso", "No se seleccionó ninguna imagen.")
