
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import ImageTk, Image
from app.Clases_principales.Editorimagen import EditorImagen
import os


class InterfazEditor:

    def __init__(self, ruta_inicial: str = None):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.editor = EditorImagen()
        self.ventana = ctk.CTk()
        self.ventana.title("Editor de Imágenes")
        self.ventana.geometry("800x600")

        self.imagen_editada_backup = None

        # Frame principal con layout horizontal (izquierda: botones, derecha: canvas)
        main_frame = ctk.CTkFrame(self.ventana)
        main_frame.pack(fill="both", expand=True)

        # Frame izquierdo para botones
        frame_botones = ctk.CTkFrame(main_frame)
        frame_botones.pack(side="left", fill="y", padx=10, pady=10)

        # Botón cargar imagen
        btn_cargar = ctk.CTkButton(frame_botones, text="💻 Cargar Imagen", command=self.cargar_imagen)
        btn_cargar.pack(pady=5)

        # Menú desplegable de filtros
        self.opciones_filtro = ["grises", "invertir", "brillo", "contraste"]
        self.filtro_seleccionado = ctk.StringVar(value=self.opciones_filtro[0])
        menu_filtros = ctk.CTkOptionMenu(frame_botones, variable=self.filtro_seleccionado, values=self.opciones_filtro)
        menu_filtros.pack(pady=5)

        # Botón aplicar filtro
        btn_aplicar_filtro = ctk.CTkButton(frame_botones, text="🎨 Aplicar Filtro", command=self.aplicar_filtro_desde_interfaz)
        btn_aplicar_filtro.pack(pady=5)

        # Botón recortar
        ctk.CTkLabel(frame_botones, text="").pack(expand=True, fill="both")
        btn_recortar = ctk.CTkButton(frame_botones, text="✂️ Recortar", command=self.activar_recorte)
        btn_recortar.pack(pady=5, side="bottom")

        # Frame derecho para el canvas
        frame_canvas = ctk.CTkFrame(main_frame, width=700, height=600)
        frame_canvas.pack(side="left", padx=10, pady=10, fill="both", expand=True)
        frame_canvas.pack_propagate(False)

        # Frame para botones superiores
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

        self.canvas.bind("<ButtonPress-1>", self.inicio_recorte)
        self.canvas.bind("<B1-Motion>", self.dibujar_rectangulo)
        self.canvas.bind("<ButtonRelease-1>", self.aplicar_recorte)

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
            self.mostrar_imagen()
        except Exception as error:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{error}")

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

    def actualizar_botones_historial(self):
        if hasattr(self, "btn_deshacer"):
            self.btn_deshacer.configure(state="normal" if not self.editor.historial.esta_vacio() else "disabled")
        if hasattr(self, "btn_rehacer"):
            estado = "normal" if hasattr(self.editor.historial, "futuros") and self.editor.historial.futuros else "disabled"
            self.btn_rehacer.configure(state=estado)

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
        self.imagen_editada_backup = self.editor.imagen_editada.copy()
        self.mostrar_imagen()

    def aplicar_filtro_desde_interfaz(self):
        tipo = self.filtro_seleccionado.get()
        self.editor.aplicar_filtro(tipo)
        self.imagen_editada_backup = self.editor.imagen_editada.copy()
        self.mostrar_imagen()

    def activar_recorte(self):
        messagebox.showinfo("Modo Recorte", "Selecciona un área con el mouse para recortar.")

    def rehacer_cambio(self):
        nueva = self.editor.historial.rehacer()
        if nueva:
            self.editor.imagen_editada = nueva
            self.mostrar_imagen()
        else:
            messagebox.showinfo("Rehacer", "No hay cambios para rehacer.")

    def deshacer_cambio(self):
        self.editor.deshacer_cambio()
        self.mostrar_imagen()

    def restaurar_original(self):
        self.imagen_editada_backup = self.editor.imagen_editada.copy()
        self.editor.restaurar_original()
        self.mostrar_imagen()

