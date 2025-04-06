import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from PIL import ImageTk
from app.Clases_principales.Editorimagen import EditorImagen


class InterfazEditor:

    def __init__(self):
        self.img_tk = None
        self.editor = EditorImagen()
        self.ventana = tk.Tk()
        self.ventana.title("Editor de Imágenes")
        self.ventana.geometry("700x600")

        #  Frame superior para controles
        controles_frame = tk.Frame(self.ventana)
        controles_frame.pack(side="top", fill="x", padx=10, pady=5)

        # Botón para cargar imagen
        btn_cargar = tk.Button(controles_frame, text=" Cargar Imagen", command=self.cargar_imagen)
        btn_cargar.pack(side="left", padx=5)

        # Lista y menú desplegable de filtros
        self.opciones_filtro = ["grises", "invertir", "brillo", "contraste"]
        self.filtro_seleccionado = tk.StringVar(value=self.opciones_filtro[0])
        menu_filtros = tk.OptionMenu(controles_frame, self.filtro_seleccionado, *self.opciones_filtro)
        menu_filtros.pack(side="left", padx=5)

        # Botón aplicar filtro
        btn_aplicar_filtro = tk.Button(controles_frame, text = " Aplicar Filtro", command=self.aplicar_filtro_desde_interfaz)
        btn_aplicar_filtro.pack(side="left", padx=5)


        # Canvas para mostrar imagen
        self.canvas = tk.Canvas(self.ventana, bg="gray", width=500, height=500)
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
            self.mostrar_imagen()

        else:
            messagebox.showinfo("Aviso", "No se seleccionó ninguna imagen.")

    def mostrar_imagen(self):
        
        if self.editor.imagen_editada is None:
            print(" No hay imagen cargada para mostrar.")
            return
        imagen = self.editor.imagen_editada.resize((500, 500))# mejor tamaño
        self.img_tk: PhotoImage = ImageTk.PhotoImage(imagen)
        self.canvas.delete("all")# limpia canvas
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

        messagebox.showinfo("Recorte aplicado", "La imagen ha sido recortada correctamente.")

    def aplicar_filtro_desde_interfaz(self):
        tipo = self.filtro_seleccionado.get()
        self.editor.aplicar_filtro(tipo)
        self.mostrar_imagen()




