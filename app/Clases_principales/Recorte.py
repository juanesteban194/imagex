from PIL import Image

class Recorte:

    @staticmethod
    def recortar(imagen: Image, coordenadas: tuple[int, int, int, int]) -> Image:
        """
        Recorta la imagen según las coordenadas dadas (x1, y1, x2, y2),
        asegurando que los valores estén ordenados correctamente.
        """

        if imagen is None:
            print(" No hay imagen para recortar")
            return None

        x1, y1, x2, y2 = map(int, coordenadas)


        x_izq = min(x1, x2)
        x_der = max(x1, x2)
        y_sup = min(y1, y2)
        y_inf = max(y1, y2)

        # Validación de límites
        if x_izq == x_der or y_sup == y_inf:
            print(" Las coordenadas de recorte no son válidas")
            return imagen

        # Aplicar recorte
        imagen_recortada = imagen.crop((x_izq, y_sup, x_der, y_inf))
        print(f" Imagen recortada desde ({x_izq}, {y_sup}) hasta ({x_der}, {y_inf})")

        return imagen_recortada