import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image, ImageDraw
from app.Clases_principales.Editorimagen import EditorImagen
from app.Clases_principales.dibujador import Dibujador
from app.Clases_principales.Recorte import Recorte
from app.api.api_manager import ApiManager
import os

class InterfazEditor:
    def __init__(self, api_manager: ApiManager, ruta_inicial: str = None):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.api_manager = api_manager
        self.editor = EditorImagen()
        self.dibujador = Dibujador()
        self.coordenadas_dibujo = []
        self.dibujando = False
        self.modo_recorte_activo = False

        self.ventana = ctk.CTk()
        self.ventana.title("Editor de Imágenes")
        self.ventana.geometry("1200x650")

        self.imagen_editada_backup = None

        main_frame = ctk.CTkFrame(self.ventana)
        main_frame.pack(fill="both", expand=True)

        frame_botones = ctk.CTkFrame(main_frame)
        frame_botones.pack(side="left", fill="y", padx=10, pady=10)

        btn_cargar = ctk.CTkButton(frame_botones, text="💻 Cargar Imagen", command=self.cargar_imagen)
        btn_cargar.pack(pady=5)

        ctk.CTkLabel(frame_botones, text="Filtros:", anchor="w").pack(pady=(20, 2), fill="x")
        self.opciones_filtro = ["grises", "invertir", "brillo", "contraste"]
        self.filtro_seleccionado = ctk.StringVar(value=self.opciones_filtro[0])
        menu_filtros = ctk.CTkOptionMenu(frame_botones, variable=self.filtro_seleccionado, values=self.opciones_filtro)
        menu_filtros.pack(pady=5)

        ctk.CTkButton(frame_botones, text="🎨 Aplicar Filtro", command=self.aplicar_filtro_desde_interfaz).pack(pady=5)

        ctk.CTkLabel(frame_botones, text="Recorte:", anchor="w").pack(pady=(20, 2), fill="x")
        ctk.CTkButton(frame_botones, text="✂️ Recortar", command=self.activar_recorte).pack(pady=(0, 10))

        frame_canvas = ctk.CTkFrame(main_frame, width=700, height=600)
        frame_canvas.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        frame_canvas.pack_propagate(False)

        frame_historial = ctk.CTkFrame(frame_canvas)
        frame_historial.pack(pady=5)

        self.btn_deshacer = ctk.CTkButton(frame_historial, text="⏪ Deshacer", command=self.deshacer_cambio)
        self.btn_deshacer.pack(side="left", padx=5)

        self.btn_rehacer = ctk.CTkButton(frame_historial, text="⏩ Rehacer", command=self.rehacer_cambio)
        self.btn_rehacer.pack(side="left", padx=5)

        ctk.CTkButton(frame_historial, text="🔄 Restaurar Imagen", command=self.restaurar_original).pack(side="left", padx=5)
        ctk.CTkButton(frame_historial, text="💾 Guardar Imagen", command=self.guardar_imagen).pack(side="left", padx=5)

        self.canvas = ctk.CTkCanvas(frame_canvas, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        frame_api = ctk.CTkFrame(main_frame, width=180)
        frame_api.pack(side="left", fill="y", padx=10, pady=10)
        ctk.CTkLabel(frame_api, text="Funciones API:", anchor="w").pack(pady=(5, 2), fill="x")
        ctk.CTkButton(frame_api, text="✨ Mejorar Calidad (API)", command=self.mejorar_calidad_api).pack(pady=3)
        ctk.CTkButton(frame_api, text="🧪 Restaurar Color (API)", command=self.restaurar_color_api).pack(pady=3)

        ctk.CTkLabel(frame_api, text="Dibujo:", anchor="w").pack(pady=(20, 2), fill="x")
        ctk.CTkButton(frame_api, text="✅ Activar Dibujo", command=self.activar_modo_dibujo).pack(pady=3)
        ctk.CTkButton(frame_api, text="❌ Desactivar Dibujo", command=self.desactivar_modo_dibujo).pack(pady=3)

        ctk.CTkLabel(frame_api, text="Color Lápiz:", anchor="w").pack(pady=(20, 2), fill="x")
        self.selector_color = ctk.CTkOptionMenu(frame_api, values=["black", "red", "green", "blue", "yellow", "white"], command=self.cambiar_color_lapiz)
        self.selector_color.set("black")
        self.selector_color.pack(pady=5)

        ctk.CTkLabel(frame_api, text="Grosor del lápiz:", anchor="w").pack(pady=(20, 2), fill="x")
        self.slider_grosor = ctk.CTkSlider(frame_api, from_=1, to=20, number_of_steps=19, command=self.cambiar_grosor_lapiz)
        self.slider_grosor.set(3)
        self.slider_grosor.pack(pady=5)

        self.rect_id = None
        self.inicio_x = 0
        self.inicio_y = 0

        self.canvas.bind("<ButtonPress-1>", self.evento_click)
        self.canvas.bind("<B1-Motion>", self.evento_mover)
        self.canvas.bind("<ButtonRelease-1>", self.evento_soltado)

        if ruta_inicial and os.path.exists(ruta_inicial):
            if self.editor.cargar_imagen(ruta_inicial):
                self.mostrar_imagen()

        self.ventana.mainloop()


    def mostrar_feedback(self, mensaje):
        messagebox.showinfo("Info", mensaje)

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imágenes JPG", "*.jpg *.jpeg")])
        if not ruta:
            return
        try:
            imagen = Image.open(ruta)
            self.editor.imagen_original = imagen
            self.editor.imagen_editada = imagen.copy()
            self.editor.actualizar_historial()
            self.imagen_editada_backup = self.editor.imagen_editada.copy()
            self.mostrar_imagen()
            self.mostrar_feedback("📷 Imagen cargada correctamente")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")

    def mostrar_imagen(self):
        if self.editor.imagen_editada:
            w, h = self.canvas.winfo_width(), self.canvas.winfo_height()
            if w == 1 and h == 1:
                w, h = 700, 600
            imagen = self.editor.imagen_editada.resize((w, h))
            self.img_tk = ImageTk.PhotoImage(imagen)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
            self.actualizar_botones_historial()

    def aplicar_filtro_desde_interfaz(self):
        self.editor.aplicar_filtro(self.filtro_seleccionado.get())
        self.imagen_editada_backup = self.editor.imagen_editada.copy()
        self.mostrar_imagen()
        self.mostrar_feedback("🎨 Filtro aplicado")

    def activar_modo_dibujo(self):
        self.dibujador.activar_modo_dibujo()
        self.modo_recorte_activo = False
        self.mostrar_feedback("🖊️ Dibujo activado")

    def desactivar_modo_dibujo(self):
        self.dibujador.desactivar_modo_dibujo()
        self.coordenadas_dibujo.clear()
        self.mostrar_feedback("❌ Dibujo desactivado")

    def cambiar_color_lapiz(self, color):
        self.dibujador.cambiar_color(color)

    def cambiar_grosor_lapiz(self, valor):
        self.dibujador.cambiar_grosor(int(float(valor)))

    def activar_recorte(self):
        self.dibujador.desactivar_modo_dibujo()
        self.modo_recorte_activo = True


    def deshacer_cambio(self):
        self.editor.deshacer_cambio()
        self.mostrar_imagen()

    def rehacer_cambio(self):
        nueva = self.editor.historial.rehacer()
        if nueva:
            self.editor.imagen_editada = nueva
            self.mostrar_imagen()

    def restaurar_original(self):
        self.imagen_editada_backup = self.editor.imagen_editada.copy()
        self.editor.restaurar_original()
        self.mostrar_imagen()
        self.mostrar_feedback("Imagen restaurada")

    def guardar_imagen(self):
        if self.editor.imagen_editada is None:
            messagebox.showwarning("Sin imagen", "No hay imagen cargada para guardar.")
            return
        ruta = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("Archivos JPG", "*.jpg *.jpeg")])
        if not ruta:
            return
        try:
            self.editor.guardar_imagen(ruta)
            messagebox.showinfo("Imagen guardada", f"La imagen se guardó correctamente en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo guardar la imagen:\n{e}")

    def restaurar_color_api(self):
        if self.editor.imagen_editada:
            try:
                nueva = self.api_manager.restaurar_color(self.editor.imagen_editada)
                self.editor.imagen_editada = nueva
                self.editor.actualizar_historial()
                self.mostrar_imagen()
                self.mostrar_feedback("Color restaurado")
            except Exception as e:
                messagebox.showerror("Error API", f"Error al usar la API:\n{e}")

    def mejorar_calidad_api(self):
        if self.editor.imagen_editada:
            try:
                nueva = self.api_manager.mejorar_calidad(self.editor.imagen_editada)
                self.editor.imagen_editada = nueva
                self.editor.actualizar_historial()
                self.mostrar_imagen()
                self.mostrar_feedback("Calidad mejorada")
            except Exception as e:
                messagebox.showerror("Error API", f"Error al mejorar calidad:\n{e}")

    def evento_click(self, e):
        if self.modo_recorte_activo:
            self.inicio_x, self.inicio_y = e.x, e.y
            self.rect_id = self.canvas.create_rectangle(e.x, e.y, e.x, e.y, outline="red")
        elif self.dibujador.modo_activo:
            self.coordenadas_dibujo = [(e.x, e.y)]
            self.dibujando = True

    def evento_mover(self, e):
        if self.modo_recorte_activo and self.rect_id:
            self.canvas.coords(self.rect_id, self.inicio_x, self.inicio_y, e.x, e.y)
        elif self.dibujador.modo_activo and self.dibujando:
            self.coordenadas_dibujo.append((e.x, e.y))
            if self.editor.imagen_editada and len(self.coordenadas_dibujo) >= 2:
                w_img, h_img = self.editor.imagen_editada.size
                w_canvas, h_canvas = self.canvas.winfo_width(), self.canvas.winfo_height()
                scale_x = w_img / w_canvas
                scale_y = h_img / h_canvas

                coords_img = [
                    (int(x * scale_x), int(y * scale_y))
                    for x, y in self.coordenadas_dibujo
                ]

                img_preview = self.editor.imagen_editada.copy()
                img_preview = self.dibujador.dibujar(
                    img_preview,
                    coordenadas=coords_img,
                    color=self.dibujador.color_lapiz,
                    grosor=self.dibujador.grosor_lapiz,
                    centrado=True
                )

                resized_preview = img_preview.resize((w_canvas, h_canvas))
                self.img_tk = ImageTk.PhotoImage(resized_preview)
                self.canvas.delete("all")
                self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)

    def evento_soltado(self, e):
        if self.dibujador.modo_activo and self.dibujando:
            self.dibujando = False
            if self.coordenadas_dibujo:
                w_img, h_img = self.editor.imagen_editada.size
                w_canvas, h_canvas = self.canvas.winfo_width(), self.canvas.winfo_height()
                scale_x = w_img / w_canvas
                scale_y = h_img / h_canvas

                coords_img = [
                    (int(x * scale_x), int(y * scale_y))
                    for x, y in self.coordenadas_dibujo
                ]

                nueva_img = self.dibujador.dibujar(
                    self.editor.imagen_editada,
                    coordenadas=coords_img,
                    color=self.dibujador.color_lapiz,
                    grosor=self.dibujador.grosor_lapiz,
                    centrado=True
                )
                self.editor.imagen_editada = nueva_img
                self.editor.actualizar_historial()
                self.mostrar_imagen()
                self.coordenadas_dibujo.clear()

        elif self.modo_recorte_activo:
            coords_canvas = (self.inicio_x, self.inicio_y, e.x, e.y)
            if self.editor.imagen_editada:
                w_img, h_img = self.editor.imagen_editada.size
                w_canvas, h_canvas = self.canvas.winfo_width(), self.canvas.winfo_height()

                scale_x = w_img / w_canvas
                scale_y = h_img / h_canvas

                x1, y1, x2, y2 = coords_canvas
                x1_img = int(x1 * scale_x)
                y1_img = int(y1 * scale_y)
                x2_img = int(x2 * scale_x)
                y2_img = int(y2 * scale_y)

                if self.editor.recortar_imagen((x1_img, y1_img, x2_img, y2_img)):
                    self.imagen_editada_backup = self.editor.imagen_editada.copy()
                    self.mostrar_imagen()

            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.modo_recorte_activo = False

    def actualizar_botones_historial(self):
        if hasattr(self, "btn_deshacer"):
            self.btn_deshacer.configure(state="normal" if not self.editor.historial.esta_vacio() else "disabled")
        if hasattr(self, "btn_rehacer"):
            estado = "normal" if hasattr(self.editor.historial, "futuros") and self.editor.historial.futuros else "disabled"
            self.btn_rehacer.configure(state=estado)
