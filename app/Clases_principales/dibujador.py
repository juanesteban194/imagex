from PIL import Image, ImageDraw

class Dibujador:
    def __init__(self, color_lapiz: str = "black", grosor_lapiz: int = 3, modo_activo: bool = False):
        self.color_lapiz = color_lapiz
        self.grosor_lapiz = grosor_lapiz
        self.modo_activo = modo_activo

    def cambiar_color(self, nuevo_color: str):
        """Cambia el color del lápiz."""
        self.color_lapiz = nuevo_color
        print(f"Color del lápiz cambiado a: {nuevo_color}")

    def cambiar_grosor(self, nuevo_grosor: int):
        """Cambia el grosor del lápiz."""
        if nuevo_grosor > 0:
            self.grosor_lapiz = nuevo_grosor
            print(f"Grosor del lápiz cambiado a: {nuevo_grosor}")
        else:
            print("El grosor debe ser mayor a 0")

    def activar_modo_dibujo(self):
        self.modo_activo = True
        print("Modo dibujo activado")

    def desactivar_modo_dibujo(self):
        self.modo_activo = False
        print("Modo dibujo desactivado")

    def dibujar(self, imagen: Image, coordenadas: list[tuple[int, int]]) -> Image:
        if imagen is None:
            print("No se ha proporcionado una imagen válida")
            return None

        if len(coordenadas) < 2:
            print("Se requieren al menos dos puntos para dibujar")
            return imagen

        imagen_dibujada = imagen.copy()
        lienzo = ImageDraw.Draw(imagen_dibujada)
        lienzo.line(coordenadas, fill=self.color_lapiz, width=self.grosor_lapiz)

        print(f"Se ha dibujado una línea con {len(coordenadas)} puntos, color {self.color_lapiz}, grosor {self.grosor_lapiz}")
        return imagen_dibujada
