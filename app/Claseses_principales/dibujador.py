from PIL import Image, ImageDraw

class Dibujador:
    def _init_(self, color_lapiz: str = "black", grosor_lapiz: int = 3, modo_activo: bool = True):

        self.color_lapiz = color_lapiz

        self.grosor_lapiz = grosor_lapiz

        self.modo_activo = modo_activo

    def dibujar(
        self,
        imagen: Image,
        coordenadas: list[tuple[int, int]],
        color: str,
        grosor: int
    ) -> Image:
        """
        Dibuja una línea conectando todos los puntos en la lista de coordenadas,
        usando el color y grosor indicados, sobre una copia de la imagen.
        """
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