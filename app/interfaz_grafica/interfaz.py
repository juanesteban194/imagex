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
        self.ventana.geometry("800x600")

        self.imagen_editada_backup = None

        main_frame = ctk.CTkFrame(self.ventana)
        main_frame.pack(fill="both", expand=True)

        frame_botones = ctk.CTkFrame(main_frame)
        frame_botones.pack(side="left", fill="y", padx=10, pady=10)

        btn_cargar = ctk.CTkButton(frame_botones, text="💻 Cargar Imagen", command=self.cargar_imagen)
        btn_cargar.pack(pady=5)

        self.opciones_filtro = ["grises", "invertir", "brillo", "contraste"]
        self.filtro_seleccionado = ctk.StringVar(value=self.opciones_filtro[0])
        menu_filtros = ctk.CTkOptionMenu(frame_botones, variable=self.filtro_seleccionado, values=self.opciones_filtro)
        menu_filtros.pack(pady=5)

        btn_aplicar_filtro = ctk.CTkButton(frame_botones, text="🎨 Aplicar Filtro", command=self.aplicar_filtro_desde_interfaz)
        btn_aplicar_filtro.pack(pady=5)

        btn_mejorar_api = ctk.CTkButton(frame_botones, text="✨ Mejorar Calidad (API)", command=self.mejorar_calidad_api)
        btn_mejorar_api.pack(pady=5)

        btn_restaurar_api = ctk.CTkButton(frame_botones, text="🧪 Restaurar Color (API)", command=self.restaurar_color_api)
        btn_restaurar_api.pack(pady=5)

        btn_activar_dibujo = ctk.CTkButton(frame_botones, text="🖊️ Activar Dibujo", command=self.activar_modo_dibujo)
        btn_activar_dibujo.pack(pady=5)

        btn_desactivar_dibujo = ctk.CTkButton(frame_botones, text="❌ Desactivar Dibujo", command=self.desactivar_modo_dibujo)
        btn_desactivar_dibujo.pack(pady=5)

        ctk.CTkLabel(frame_botones, text="🎨 Color del lápiz:").pack(pady=(10, 0))
        self.selector_color = ctk.CTkOptionMenu(frame_botones, values=["black", "red", "green", "blue", "yellow", "white"],
                                                command=self.cambiar_color_lapiz)
        self.selector_color.set("black")
        self.selector_color.pack(pady=5)

        ctk.CTkLabel(frame_botones, text="✏️ Grosor del lápiz:").pack(pady=(10, 0))
        self.slider_grosor = ctk.CTkSlider(frame_botones, from_=1, to=20, number_of_steps=19, command=self.cambiar_grosor_lapiz)
        self.slider_grosor.set(3)
        self.slider_grosor.pack(pady=5)

        ctk.CTkLabel(frame_botones, text="").pack(expand=True, fill="both")
        btn_recortar = ctk.CTkButton(frame_botones, text="✂️ Recortar", command=self.activar_recorte)
        btn_recortar.pack(pady=5, side="bottom")

        frame_canvas = ctk.CTkFrame(main_frame, width=700, height=600)
        frame_canvas.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        frame_canvas.pack_propagate(False)

        frame_historial = ctk.CTkFrame(frame_canvas)
        frame_historial.pack(pady=5)

        self.btn_deshacer = ctk.CTkButton(frame_historial, text="⏪ Deshacer", command=self.deshacer_cambio)
        self.btn_deshacer.pack(side="left", padx=5)

        self.btn_rehacer = ctk.CTkButton(frame_historial, text="⏩ Rehacer", command=self.rehacer_cambio)
        self.btn_rehacer.pack(side="left", padx=5)

        btn_restaurar_original = ctk.CTkButton(frame_historial, text="🔄 Restaurar Imagen", command=self.restaurar_original)
        btn_restaurar_original.pack(side="left", padx=5)

        btn_guardar = ctk.CTkButton(frame_historial, text="💾 Guardar Imagen", command=self.guardar_imagen)
        btn_guardar.pack(side="left", padx=5)

        self.canvas = ctk.CTkCanvas(frame_canvas, bg="gray")
        self.canvas.pack(fill="both", expand=True)

        self.rect_id = None
        self.inicio_x = 0
        self.inicio_y = 0

        self.canvas.bind("<ButtonPress-1>", self.evento_click)
        self.canvas.bind("<B1-Motion>", self.evento_mover)
        self.canvas.bind("<ButtonRelease-1>", self.evento_soltado)

        if ruta_inicial and os.path.exists(ruta_inicial):
            cargada = self.editor.cargar_imagen(ruta_inicial)
            if cargada:
                self.mostrar_imagen()

        self.ventana.mainloop()

    def cargar_imagen(self):
        ruta = filedialog.askopenfilename(title="Selecciona una imagen", filetypes=[("Imágenes JPG", "*.jpg *.jpeg")])
        if not ruta:
            messagebox.showinfo("Aviso", "No seleccionaste una imagen.")
            return
        try:
            imagen = Image.open(ruta)
            self.editor.imagen_original = imagen
            self.editor.imagen_editada = imagen.copy()
            self.editor.actualizar_historial()
            self.imagen_editada_backup = self.editor.imagen_editada.copy()
            print("[INFO] Imagen cargada correctamente")
            self.mostrar_imagen()
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{error}")

    def aplicar_filtro_desde_interfaz(self):
        tipo = self.filtro_seleccionado.get()
        self.editor.aplicar_filtro(tipo)
        self.imagen_editada_backup = self.editor.imagen_editada.copy()
        self.mostrar_imagen()

    def mostrar_imagen(self):
        if self.editor.imagen_editada is not None:
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            if canvas_width == 1 and canvas_height == 1:
                canvas_width, canvas_height = 700, 600
            imagen = self.editor.imagen_editada.resize((canvas_width, canvas_height))
            self.img_tk = ImageTk.PhotoImage(imagen)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, anchor="nw", image=self.img_tk)
            self.actualizar_botones_historial()

    def restaurar_color_api(self):
        print("[API] Restaurando color...")
        if self.editor.imagen_editada is None:
            messagebox.showwarning("Sin imagen", "Carga una imagen antes de aplicar el API.")
            return
        try:
            nueva = self.api_manager.restaurar_color(self.editor.imagen_editada)
            print("[API] Restauración completada.")
            self.editor.imagen_editada = nueva
            self.editor.actualizar_historial()
            self.mostrar_imagen()
        except Exception as e:
            print(f"[API] Error en restaurar_color: {e}")
            messagebox.showerror("Error API", f"Error al usar la API:\n{e}")

    def mejorar_calidad_api(self):
        print("[API] Mejorando calidad...")
        if self.editor.imagen_editada is None:
            messagebox.showwarning("Sin imagen", "Carga una imagen antes de mejorar calidad.")
            return
        try:
            nueva = self.api_manager.mejorar_calidad(self.editor.imagen_editada)
            print("[API] Mejora completada.")
            self.editor.imagen_editada = nueva
            self.editor.actualizar_historial()
            self.mostrar_imagen()
        except Exception as e:
            print(f"[API] Error en mejorar_calidad: {e}")
            messagebox.showerror("Error API", f"Error al mejorar calidad:\n{e}")

    def activar_modo_dibujo(self):
        self.dibujador.activar_modo_dibujo()
        self.modo_recorte_activo = False
        messagebox.showinfo("Modo Dibujo", "Modo dibujo activado. Usa el mouse para dibujar sobre la imagen.")

    def desactivar_modo_dibujo(self):
        self.dibujador.desactivar_modo_dibujo()
        self.coordenadas_dibujo.clear()
        messagebox.showinfo("Modo Dibujo", "Modo dibujo desactivado.")

    def cambiar_color_lapiz(self, color):
        self.dibujador.cambiar_color(color)

    def cambiar_grosor_lapiz(self, valor):
        self.dibujador.cambiar_grosor(int(float(valor)))

    def activar_recorte(self):
        self.dibujador.desactivar_modo_dibujo()
        self.modo_recorte_activo = True
        messagebox.showinfo("Modo Recorte", "Selecciona un área con el mouse para recortar.")

    def deshacer_cambio(self):
        self.editor.deshacer_cambio()
        self.mostrar_imagen()

    def rehacer_cambio(self):
        nueva = self.editor.historial.rehacer()
        if nueva:
            self.editor.imagen_editada = nueva
            self.mostrar_imagen()
        else:
            messagebox.showinfo("Rehacer", "No hay cambios para rehacer.")

    def restaurar_original(self):
        self.imagen_editada_backup = self.editor.imagen_editada.copy()
        self.editor.restaurar_original()
        self.mostrar_imagen()

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

    def evento_click(self, evento):
        if self.modo_recorte_activo:
            self.inicio_x = evento.x
            self.inicio_y = evento.y
            self.rect_id = self.canvas.create_rectangle(self.inicio_x, self.inicio_y, self.inicio_x, self.inicio_y, outline="red")
        elif self.dibujador.modo_activo:
            self.coordenadas_dibujo = [(evento.x, evento.y)]
            self.dibujando = True

    def evento_mover(self, evento):
        if self.modo_recorte_activo and self.rect_id is not None:
            self.canvas.coords(self.rect_id, self.inicio_x, self.inicio_y, evento.x, evento.y)
        elif self.dibujador.modo_activo and self.dibujando:
            self.coordenadas_dibujo.append((evento.x, evento.y))
            if len(self.coordenadas_dibujo) >= 2:
                nueva_imagen = self.dibujador.dibujar(self.editor.imagen_editada, self.coordenadas_dibujo[-2:])
                if nueva_imagen:
                    self.editor.imagen_editada = nueva_imagen
                    self.mostrar_imagen()

    def evento_soltado(self, evento):
        if self.modo_recorte_activo:
            x1, y1 = self.inicio_x, self.inicio_y
            x2, y2 = evento.x, evento.y
            coordenadas = (x1, y1, x2, y2)
            nueva = Recorte.recortar(self.editor.imagen_editada, coordenadas)
            if nueva:
                self.editor.imagen_editada = nueva
                self.editor.actualizar_historial()
                self.imagen_editada_backup = nueva.copy()
                self.mostrar_imagen()
            self.canvas.delete(self.rect_id)
            self.rect_id = None
            self.modo_recorte_activo = False

        elif self.dibujador.modo_activo and self.dibujando:
            self.dibujando = False
            self.coordenadas_dibujo.clear()
            self.editor.actualizar_historial()

    def actualizar_botones_historial(self):
        if hasattr(self, "btn_deshacer"):
            self.btn_deshacer.configure(state="normal" if not self.editor.historial.esta_vacio() else "disabled")
        if hasattr(self, "btn_rehacer"):
            estado = "normal" if hasattr(self.editor.historial, "futuros") and self.editor.historial.futuros else "disabled"
            self.btn_rehacer.configure(state=estado)