from PIL import Image

class Recorte:
    def __init__(self, ruta_imagen):
        self.imagen = Image.open(ruta_imagen)

    def aplicar_recorte(self, x1, y1, x2, y2):
        imagen_recortada = self.imagen.crop((x1, y1, x2, y2))
        imagen_recortada.show()
        imagen_recortada.save("imagen_recortada.jpg")

recorte = Recorte("imagen_original.jpg")
recorte.aplicar_recorte(50, 50, 300, 300)  # (x1, y1, x2, y2)

