import os
from PIL.Image import Image

from app.services.historial_cambios import HistorialCambios


class EditorImagen:

    def __init__(self):
        self.imagen_original: Image | None = None
        self.imagen_editada: Image | None = None
        self.historial: HistorialCambios = HistorialCambios()

    def cargar_imagen(self, ruta: str):

        if os.path.exists(ruta):
            imagen = Image.open(ruta)
            self.imagen_original: Image | None = imagen
            self.imagen_editada: Image | None = imagen.copy()
            self.historial: HistorialCambios = HistorialCambios()
            self.historial.guardar_estado(self.imagen_editada)
            print( f" la imagen fue cargada correctamente " )
            return True
        else:
            print(f" La imagen no fue cargada, no fue encontrada en la ruta: {ruta}. ")
            return False

    def mostrar_imagen(self):

        if self.imagen_editada is not None:
            print(" Mostrando imagen actual...")
            return self.imagen_editada.show()


        else:
            print(f" No has cargado una imagen ")


    def cargar_foto(self, ruta: str):
        pass





