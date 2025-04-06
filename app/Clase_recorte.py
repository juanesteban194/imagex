from PIL import Image

class Recorte:
    @staticmethod
    def recortar(imagen: Image, coordenadas: tuple[int, int, int, int]) -> Image:

        if imagen is None:
            print("⚠ No hay imagen para recortar.")
            return None

        x1 = coordenadas[0]
        y1 = coordenadas[1]
        x2 = coordenadas[2]
        y2 = coordenadas[3]

        if x1 >= x2 or y1 >= y2:
            print("❌ Las coordenadas de recorte no son válidas.")
            return imagen

        imagen_recortada = imagen.crop((x1, y1, x2, y2))

        print(f"✂ Imagen recortada desde ({x1}, {y1}) hasta ({x2}, {y2})")
        return imagen_recortada