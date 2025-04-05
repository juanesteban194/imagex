from PIL.Image import Image



class HistorialCambios:

    def __init__(self, limite = 10):

        self.historial: list[Image] = []
        self.limite: int = limite

    def guardar_estado(self, imagen: Image):

        if len(self.historial) >= self.limite:
            self.historial.pop(0)
        self.historial.append(imagen.copy())


    def deshacer(self) -> Image | None:

        if len(self.historial) > 0 :
            return self.historial.pop()
        else:
            return None


    def estado_actual(self):

        if len(self.historial) > 0:
            return self.historial[-1]
        else:
            return None

    def esta_vacio(self) -> bool:
        return len(self.historial) == 0








