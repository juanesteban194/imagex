from PIL import Image
import os

class EditorImagen:
    def __init__(self):
        self.imagen_original = None
        self.imagen_editada = None
        self.historial = []

    def validar_formato(self, ruta: str) -> bool:
        extensiones_validas = ['.jpg', '.jpeg', '.png', '.bmp']
        _, extension = os.path.splitext(ruta.lower())
        return extension in extensiones_validas

    def cargar_imagen(self, ruta: str) -> bool:
        if not self.validar_formato(ruta):
            print("Formato no válido.")
            return False
        try:
            imagen = Image.open(ruta)
            self.imagen_original = imagen
            self.imagen_editada = imagen.copy()
            self.historial.clear()  # Reinicia historial
            print("Imagen cargada correctamente.")
            return True
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            return False

    def imagen_disponible(self) -> bool:
        return self.imagen_editada is not None
