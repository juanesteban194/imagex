from PIL import Image, ImageEnhance, ImageOps

class Filtro:

    def __init__(self, tipo_filtro: str):
        # Tipo de filtro a aplicar
        self.tipo_filtro = tipo_filtro

    def aplicar_filtro(self, imagen: Image ) -> Image:
        if imagen is None:
            print(" No hay imagen para aplicar filtro.")
            return None

        imagen_resultado = imagen

        if self.tipo_filtro == "grises":
            imagen_resultado = imagen.convert("L")

        elif self.tipo_filtro == "invertir":
            imagen_resultado = ImageOps.invert(imagen.convert("RGB"))

        elif self.tipo_filtro  == "brillo":
            ajustador = ImageEnhance.Brightness(imagen)
            imagen_resultado = ajustador.enhance(1.5)

        elif self.tipo_filtro  == "contraste":
            ajustador = ImageEnhance.Contrast(imagen)
            imagen_resultado = ajustador.enhance(1.5)

        else:
            print(f" Tipo de filtro no válido: {self.tipo_filtro }")
            return imagen

        print(f"Filtro {self.tipo_filtro } aplicado correctamente.")

        return imagen_resultado

