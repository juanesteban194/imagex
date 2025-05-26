from PIL.Image import Image

class HistorialCambios:
    def __init__(self, limite: int = 10):
        self.historial: list[Image] = []
        self.futuros: list[Image] = []
        self.limite: int = limite

    def guardar_estado(self, imagen: Image):
        if imagen is None:
            return
        if len(self.historial) >= self.limite:
            self.historial.pop(0)
        self.historial.append(imagen.copy())
        self.futuros.clear()

    def deshacer(self) -> Image | None:
        if len(self.historial) > 1:
            actual = self.historial.pop()
            self.futuros.append(actual)
            return self.historial[-1].copy()
        return None

    def rehacer(self) -> Image | None:
        if self.futuros:
            imagen = self.futuros.pop()
            self.historial.append(imagen)
            return imagen.copy()
        return None

    def estado_actual(self) -> Image | None:
        if self.historial:
            return self.historial[-1].copy()
        return None

    def esta_vacio(self) -> bool:
        return len(self.historial) <= 1
