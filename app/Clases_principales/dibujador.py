from PIL import Image, ImageDraw
import math

class Dibujador:
    def __init__(self, color_lapiz: str = "black", grosor_lapiz: int = 3, modo_activo: bool = False):
        self.color_lapiz = color_lapiz
        self.grosor_lapiz = grosor_lapiz
        self.modo_activo = modo_activo

    def cambiar_color(self, nuevo_color: str):
        self.color_lapiz = nuevo_color
        print(f"Color del lápiz cambiado a: {nuevo_color}")

    def cambiar_grosor(self, nuevo_grosor: int):
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

    def suavizar_puntos(self, puntos: list[tuple[int, int]]) -> list[tuple[int, int]]:
        if len(puntos) < 3:
            return puntos

        suavizados = [puntos[0]]
        for i in range(1, len(puntos) - 1):
            x0, y0 = puntos[i - 1]
            x1, y1 = puntos[i]
            x2, y2 = puntos[i + 1]
            mx = (x0 + x1 + x2) // 3
            my = (y0 + y1 + y2) // 3
            suavizados.append((mx, my))
        suavizados.append(puntos[-1])
        return suavizados

    def dibujar(self, imagen: Image, coordenadas: list[tuple[int, int]], color: str = None, grosor: int = None, centrado: bool = False) -> Image:
        if imagen is None:
            print("No se ha proporcionado una imagen válida")
            return None

        if not coordenadas:
            print("No se han proporcionado coordenadas")
            return imagen

        color = color or self.color_lapiz
        grosor = grosor or self.grosor_lapiz

        imagen_dibujada = imagen.copy()
        lienzo = ImageDraw.Draw(imagen_dibujada)

        if len(coordenadas) == 1:
            x, y = coordenadas[0]
            r = grosor // 2
            lienzo.ellipse([x - r, y - r, x + r, y + r], fill=color)
        elif len(coordenadas) >= 2:
            coords_suavizados = self.suavizar_puntos(coordenadas)
            lienzo.line(coords_suavizados, fill=color, width=grosor)

        print(f"Se ha dibujado {'un punto' if len(coordenadas)==1 else 'una línea suavizada'} con color {color}, grosor {grosor}, centrado {centrado}")
        return imagen_dibujada