from PIL import Image, ImageDraw

class Dibujador:

    def __init__(self, color_lapiz: str = "black", grosor_lapiz: int = 3, modo_activo: bool = False):

        self.color_lapiz = color_lapiz

        self.grosor_lapiz = grosor_lapiz

        self.modo_activo = modo_activo

    @staticmethod
    def dibujar( imagen: Image, coordenadas: list[tuple[int, int]], color: str, grosor: int) -> Image:

        if imagen is None:
            print(" No se ha proporcionado una imagen válida")
            return None

        if len(coordenadas) < 2:
            print(" Se requieren al menos dos puntos para dibujar")
            return imagen


        imagen_dibujada = imagen.copy()


        lienzo = ImageDraw.Draw(imagen_dibujada)


        lienzo.line(coordenadas, fill=color, width=grosor)

        print(f" Se ha dibujado una línea con {len(coordenadas)} puntos, color {color}, grosor {grosor}")
        return imagen_dibujada