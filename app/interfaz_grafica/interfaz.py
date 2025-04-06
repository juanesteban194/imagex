import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from PIL import ImageTk, Image
from app.Clases_principales.Editorimagen import EditorImagen
import os


class InterfazEditor:

    def __init__(self, ruta_inicial: str = None):
        self.editor = EditorImagen()
        self.ventana = tk.Tk()
        self.ventana.title("Editor de Imágenes")
        self.ventana.geometry("700x600")

        # 🟩 Frame superior para botones
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)

        # Botón cargar imagen
        btn_cargar = tk.Button(frame_botones, text="📂 Cargar Imagen", command=self.cargar_imagen)
        btn_cargar.pack(side="left", padx=5)

        # Menú desplegable de filtros
        self.opciones_filtro = ["grises", "invertir", "brillo", "contraste"]
        self.filtro_seleccionado = tk.StringVar(value=self.opciones_filtro[0])
        menu_filtros = tk.OptionMenu(frame_botones, self.filtro_seleccionado, *self.opciones_filtro)
        menu_filtros.pack(side="left", padx=5)

        # Botón aplicar filtro
        btn_aplicar_filtro = tk.Button(frame_botones, text="🎨 Aplicar Filtro",
                                       command=self.aplicar_filtro_desde_interfaz)
        btn_aplicar_filtro.pack(side="left", padx=5)

        # Frame para el canvas (zona inferior)
        frame_canvas = tk.Frame(self.ventana)
        frame_canvas.pack()

        self.canvas = tk.Canvas(frame_canvas, bg="gray", width=500, height=500)
        self.canvas.pack()

        # Eventos de recorte
        self.rect_id = None
        self.inicio_x = 0
        self.inicio_y = 0

        self.canvas.bind("<ButtonPress-1>", self.inicio_recorte)
        self.canvas.bind("<B1-Motion>", self.dibujar_rectangulo)
        self.canvas.bind("<ButtonRelease-1>", self.aplicar_recorte)

        # Cargar imagen automática si se dio ruta
        if ruta_inicial and os.path.exists(ruta_inicial):
            cargada = self.editor.cargar_imagen(ruta_inicial)
            if cargada:
                self.mostrar_imagen()

        self.ventana.mainloop()

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Selecciona una imagen", filetypes=[("Imágenes JPG", "*.jpg *.jpeg")] )

        if not ruta:
            messagebox.showinfo("Aviso", "No seleccionaste una imagen.")
            return

        try:
            imagen = Image.open(ruta)
            imagen = imagen.resize((500, 500))
            self.img_tk = ImageTk.PhotoImage(imagen)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")


    def mostrar_imagen(self):
        if self.editor.imagen_editada is not None:
            imagen = self.editor.imagen_editada.resize((500, 500))
            self.img_tk = ImageTk.PhotoImage(imagen)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
        else:
            print("No hay imagen cargada para mostrar.")

    def inicio_recorte(self, evento_mouse):
        self.inicio_x = evento_mouse.x
        self.inicio_y = evento_mouse.y
        self.rect_id = self.canvas.create_rectangle(self.inicio_x, self.inicio_y, self.inicio_x, self.inicio_y, outline="red")

    def dibujar_rectangulo(self, evento_mouse):
        self.canvas.coords(self.rect_id, self.inicio_x, self.inicio_y, evento_mouse.x, evento_mouse.y)

    def aplicar_recorte(self, evento_mouse):
        x1, y1 = self.inicio_x, self.inicio_y
        x2, y2 = evento_mouse.x, evento_mouse.y
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        self.editor.recortar_imagen((x1, y1, x2, y2))
        self.mostrar_imagen()

    def aplicar_filtro_desde_interfaz(self):
        tipo = self.filtro_seleccionado.get()
        self.editor.aplicar_filtro(tipo)
        self.mostrar_imagen()
