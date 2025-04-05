from PIL import Image
from app.services.historial_cambios import HistorialCambios

# Cargar imagen de prueba desde carpeta
imagen_original = Image.open("../Fotos_Prueba/foto.jpg")

# Crear historial con límite de 3 versiones
historial = HistorialCambios(limite=3)

# Guardar estado inicial
historial.guardar_estado(imagen_original)

# Simular cambios: rotar y voltear
imagen_rotada = imagen_original.rotate(90)
historial.guardar_estado(imagen_rotada)

imagen_volteada = imagen_rotada.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
historial.guardar_estado(imagen_volteada)

# Mostrar estado actual
estado = historial.estado_actual()
print("Mostrando imagen actual (con cambios)")
estado.show()

# Deshacer último cambio
deshecha = historial.deshacer()
print("Mostrando imagen anterior (deshacer)")
deshecha.show()

# Estado luego de deshacer
estado_actual = historial.estado_actual()
print("¿Historial vacío?:", historial.esta_vacio())
print("Mostrando imagen actual después de deshacer")
estado_actual.show()
