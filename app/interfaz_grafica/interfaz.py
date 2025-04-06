import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from PIL import ImageTk
from app.Clases_principales.Editorimagen import EditorImagen


class InterfazEditor:

    def __init__(self):
        self.editor = EditorImagen()
        self.ventana = tk.Tk()
        self.ventana.title("Editor de Imágenes")
        self.ventana.geometry("700x500")

        # Botón para cargar imagen
        btn_cargar = tk.Button(self.ventana, text = " Cargar Imagen", command = self.cargar_imagen)
        btn_cargar.pack()

        # Área para mostrar imagen
        self.label_imagen = tk.Label(self.ventana, text = " Imagen no cargada ")
        self.label_imagen.pack()


        # Canvas para mostrar imagen
        self.canvas = tk.Canvas(self.ventana, bg="gray", width=400, height=400)
        self.canvas.pack(pady=10)

        # Variables para selección de recorte
        self.rect_id = None
        self.inicio_x = 0
        self.inicio_y = 0

        # Eventos del mouse en el canvas
        self.canvas.bind("<ButtonPress-1>", self.inicio_recorte)
        self.canvas.bind("<B1-Motion>", self.dibujar_rectangulo)
        self.canvas.bind("<ButtonRelease-1>", self.aplicar_recorte)

        self.ventana.mainloop()

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(filetypes = [("Imágenes JPG", "*.jpg *.jpeg " )])
        if ruta:
            self.editor.cargar_imagen(ruta)
            img: ImageTk.PhotoImage = ImageTk.PhotoImage(self.editor.imagen_editada.resize((300, 300)))
            self.label_imagen.configure( image = img)
            self.label_imagen.image = img  #guarda referencia a la imagen o no se mostrará
        else:
            messagebox.showinfo("Aviso", "No se seleccionó ninguna imagen.")

    def mostrar_imagen(self):
        imagen = self.editor.imagen_editada.resize((400, 400))
        self.img_tk: PhotoImage = ImageTk.PhotoImage(imagen)
        self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)


    def inicio_recorte(self, evento_mouse):
        self.inicio_x = evento_mouse.x
        self.inicio_y = evento_mouse.y
        self.rect_id = self.canvas.create_rectangle(self.inicio_x, self.inicio_y, self.inicio_x, self.inicio_y, outline="red")


    def dibujar_rectangulo(self, evento_mouse):
        self.canvas.coords(self.rect_id, self.inicio_x, self.inicio_y, evento_mouse.x, evento_mouse.y)


    def aplicar_recorte(self, evento_mouse):

        x1 = self.inicio_x
        y1 = self.inicio_y
        x2 = evento_mouse.x
        y2 = evento_mouse.y

        # Ordenar coordenadas para evitar recortes incorrectos
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])

        self.editor.recortar_imagen((x1, y1, x2, y2))
        self.mostrar_imagen()



