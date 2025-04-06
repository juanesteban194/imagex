from PIL import Image, ImageEnhance, ImageOps

class Filtro:
    @staticmethod
    def aplicar_filtro(imagen: Image, tipo: str) -> Image:
        """
        Aplica un filtro a la imagen según el tipo indicado.
        Tipos válidos: 'grises', 'invertir', 'brillo', 'contraste'
        """
        if imagen is None:
            print(" No hay imagen para aplicar filtros.")
            return None

        imagen_resultado = imagen

        if tipo == "grises":
            imagen_resultado = imagen.convert("L")

        elif tipo == "invertir":
            imagen_resultado = ImageOps.invert(imagen.convert("RGB"))

        elif tipo == "brillo":
            ajustador = ImageEnhance.Brightness(imagen)
            imagen_resultado = ajustador.enhance(1.5)

        elif tipo == "contraste":
            ajustador = ImageEnhance.Contrast(imagen)
            imagen_resultado = ajustador.enhance(1.5)

        else:
            print(f"️ Tipo de filtro no válido: '{tipo}'")
            return imagen

        print(f" Filtro '{tipo}' aplicado correctamente.")
        return imagen_resultado