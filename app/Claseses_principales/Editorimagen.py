import os
from PIL.Image import Image
from app.services.historial_cambios import HistorialCambios
from PIL import ImageEnhance




class EditorImagen:

    def __init__(self):
        self.imagen_original: Image | None = None
        self.imagen_editada: Image | None = None
        self.historial: HistorialCambios = HistorialCambios()

    @staticmethod
    def validar_formato(ruta: str) -> bool:
        return ruta.lower().endswith((".jpg", ".jpeg"))

    def cargar_imagen(self, ruta: str) -> bool:

        if not self.validar_formato(ruta):
            print(" Solo se pueden cargar imágenes con extensión .jpg o .jpeg ")
            return False


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
            self.imagen_editada.show()


        else:
            print(f" No has cargado una imagen ")


    def guardar_imagen(self, ruta: str):

        if self.imagen_editada is not None:

            if  self.validar_formato(ruta):
                self.imagen_editada.save(ruta)
                print(f" imagen guardada en: {ruta}")
                return True
            else:
                print(f" Formato no válido. Solo puedes guardar archivos de tipo .jpg o . jpeg")

        else:
            print( " No hay imagen cargada para guardar ")


    def restaurar_original(self):

        if self.imagen_original is not None:
            self.imagen_editada = self.imagen_original.copy()
            self.historial.guardar_estado(self.imagen_editada)
            print(" Imagen restaurada al estado original ")

        else:
            print(" No hay imagen cargada para restaurar, carga una imagen ")

    def deshacer_cambio(self):

        if not self.historial.esta_vacio():
            imagen_anterior = self.historial.deshacer()

            if imagen_anterior is not None:
                self.imagen_editada = imagen_anterior
                print(" Se deshizo el último cambio ")

            else:
                print(" No se pudo recuperar el estado anterior ")

        else:
            print(" No hay cambios para deshacer.")


    def imagen_disponible(self) -> bool:

        if self.imagen_editada is not None:
            return True
        else:
            return False

    def ajustar_parametro(self, tipo: str, valor: int):

        if self.imagen_editada is not None:

            if tipo == "Rotar":
                imagen_ajustada = self.imagen_editada.rotate(valor)

            elif tipo == "grises":
                imagen_ajustada = self.imagen_editada.convert("L")

            elif tipo == "brillo":
                ajustador_brillo = ImageEnhance.Brightness(self.imagen_editada)
                imagen_ajustada = ajustador_brillo.enhance(valor / 100)

            elif tipo == "contraste":
                ajustador_contraste = ImageEnhance.Contrast(self.imagen_editada)
                imagen_ajustada = ajustador_contraste.enhance(valor / 100)

            else:
                print(f" Tipo de ajuste no válido: {tipo}")
                return

            self.imagen_editada = imagen_ajustada
            self.historial.guardar_estado(self.imagen_editada)
            print(f" Ajuste '{tipo}' aplicado correctamente.")
        else:
            print(" No hay imagen cargada para aplicar ajustes ")

    def actualizar_historial(self):

        if self.imagen_editada is not None:
            self.historial.guardar_estado(self.imagen_editada)
            print(" Imagen actual guardada en el historial.")
        else:
            print(" No hay imagen editada para guardar en el historial.")












