from PIL import ImageFilter     #este modulo imageFilter lo usamos para procesar imagenes en phyton y PIL es la biblioteca para trabajar con imagenes


class Filtro:

    def aplicar_filtro(self, imagen, tipo):   #este metodo recibe dos parametros imagen y tipo
                                              #imagen e este caso sera la que le aplicara el filtro y tipo sera el filtro que seleccione el usuario

        filtros_disponibles = {                            #en este paso estamos definiendo un diccionario con los filtros diponible en la biblioteca que estamos usado
            "BLUR": ImageFilter.BLUR,                      #estamos dandole un nobre a cada filtro para que el  usuario pueda seleccionar cual desea usar
            "CONTOUR": ImageFilter.CONTOUR,
            "DETAIL": ImageFilter.DETAIL,
            "EDGE_ENHANCE": ImageFilter.EDGE_ENHANCE,
            "EMBOSS": ImageFilter.EMBOSS,
            "SHARPEN": ImageFilter.SHARPEN
        }

        if tipo in filtros_disponibles:            #aqui simplemente verificamos que el filtro que la persona selecciono este disponible
            print(f"Aplicando filtro: {tipo}")     #muestra un pequeño mensaje diciendo que el filtro se esta aplicando
            return imagen.filter(filtros_disponibles[tipo])  # .filter es un metodo de PIL(la biblioteca)  para aplicar el filtro a la imagen
        else:
            print("Filtro no válido. Seleccione uno de la lista.")   #si igresan un filtro que no esta disponible muestra el mensaje y retorna la iamgen sin cambios
            return imagen

#nota: esta saltando el error de que no se le esta dando un uso a self porque falta la otra parte del codigo por ende se va quitar cuando ya este