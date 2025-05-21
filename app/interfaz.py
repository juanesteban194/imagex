import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from app.Clases_principales.Editorimagen import EditorImagen
from app.Clases_principales.Dibujador import Dibujador
from app.Clases_principales.Recorte import Recorte
import os


class InterfazEditor:

    def __init__(self, ruta_inicial: str = None):
        self.editor = EditorImagen()
        self.dibujador = Dibujador()
        self.coordenadas_dibujo = []
        self.recorteador = Recorte()

        self.ventana = tk.Tk()
        self.ventana.title("Editor de Imágenes")
        self.ventana.geometry("700x600")

        # Frame de botones
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=10)

        # Botones principales
        tk.Button(frame_botones, text="📂 Cargar Imagen", command=self.cargar_imagen).pack(side="left", padx=5)

        self.opciones_filtro = ["grises", "invertir", "brillo", "contraste"]
        self.filtro_seleccionado = tk.StringVar(value=self.opciones_filtro[0])
        tk.OptionMenu(frame_botones, self.filtro_seleccionado, *self.opciones_filtro).pack(side="left", padx=5)
        tk.Button(frame_botones, text="🎨 Aplicar Filtro", command=self.aplicar_filtro_desde_interfaz).pack(side="left", padx=5)
        tk.Button(frame_botones, text="✏️ Dibujar", command=self.activar_dibujo).pack(side="left", padx=5)

        # Canvas
        frame_canvas = tk.Frame(self.ventana)
        frame_canvas.pack()
        self.canvas = tk.Canvas(frame_canvas, bg="gray", width=500, height=500)
        self.canvas.pack()

        # Variables para recorte
        self.rect_id = None
        self.inicio_x = 0
        self.inicio_y = 0

        # Eventos del mouse
        self.canvas.bind("<ButtonPress-1>", self.manejar_click)
        self.canvas.bind("<B1-Motion>", self.manejar_movimiento)
        self.canvas.bind("<ButtonRelease-1>", self.manejar_liberacion)

        if ruta_inicial and os.path.exists(ruta_inicial):
            if self.editor.cargar_imagen(ruta_inicial):
                self.mostrar_imagen()

        self.ventana.mainloop()

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imágenes", "*.jpg *.jpeg *.png")])
        if not ruta:
            return
        try:
            imagen = Image.open(ruta)
            self.editor.imagen_original = imagen
            self.editor.imagen_editada = imagen.copy()
            self.editor.actualizar_historial()
            self.mostrar_imagen()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")

    def mostrar_imagen(self):
        if self.editor.imagen_editada:
            imagen = self.editor.imagen_editada.resize((500, 500))
            self.img_tk = ImageTk.PhotoImage(imagen)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

    def aplicar_filtro_desde_interfaz(self):
        tipo = self.filtro_seleccionado.get()
        self.editor.aplicar_filtro(tipo)
        self.mostrar_imagen()

    def activar_dibujo(self):
        self.dibujador.modo_activo = not self.dibujador.modo_activo
        print("Modo dibujo:", "Activado" if self.dibujador.modo_activo else "Desactivado")

    def manejar_click(self, evento):
        if self.dibujador.modo_activo:
            self.coordenadas_dibujo = [(evento.x, evento.y)]
        else:
            self.inicio_recorte(evento)

    def manejar_movimiento(self, evento):
        if self.dibujador.modo_activo:
            self.coordenadas_dibujo.append((evento.x, evento.y))
            if len(self.coordenadas_dibujo) >= 2:
                nueva_img = self.dibujador.dibujar(
                    self.editor.imagen_editada,
                    self.coordenadas_dibujo,
                    self.dibujador.color_lapiz,
                    self.dibujador.grosor_lapiz
                )
                if nueva_img:
                    self.editor.imagen_editada = nueva_img
                    self.coordenadas_dibujo = [self.coordenadas_dibujo[-1]]
                    self.mostrar_imagen()
        else:
            self.dibujar_rectangulo(evento)

    def manejar_liberacion(self, evento):
        if not self.dibujador.modo_activo:
            self.aplicar_recorte(evento)

    def inicio_recorte(self, evento):
        self.inicio_x = evento.x
        self.inicio_y = evento.y
        self.rect_id = self.canvas.create_rectangle(self.inicio_x, self.inicio_y, self.inicio_x, self.inicio_y, outline="red")

    def dibujar_rectangulo(self, evento):
        self.canvas.coords(self.rect_id, self.inicio_x, self.inicio_y, evento.x, evento.y)

    def aplicar_recorte(self, evento):
        x1, y1 = self.inicio_x, self.inicio_y
        x2, y2 = evento.x, evento.y
        coords = (x1, y1, x2, y2)
        imagen = self.editor.imagen_editada
        if imagen:
            nueva = self.recorteador.recortar(imagen, coords)
            if nueva:
                self.editor.imagen_editada = nueva
                self.mostrar_imagen()
