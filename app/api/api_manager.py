import requests
from PIL import Image
from io import BytesIO

class ApiManager:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("API_KEY no encontrada. Verifica tu archivo .env")

        self.api_key = api_key
        self.url_colorizer = "https://api.deepai.org/api/colorizer"
        self.url_mejorar_calidad = "https://api.deepai.org/api/waifu2x"
        self.url_toonify = "https://api.deepai.org/api/toonify"
        self.url_fast_style_transfer = "https://api.deepai.org/api/fast-style-transfer"

    def _convertir_a_buffer(self, image: Image.Image) -> BytesIO:
        buffer = BytesIO()
        image.convert("RGB").save(buffer, format="JPEG")
        buffer.seek(0)
        return buffer


    def restaurar_color(self, imagen: Image.Image) -> Image.Image:
        buffer = self._convertir_a_buffer(imagen)
        response = requests.post(
            self.url_colorizer,
            files={"image": buffer},
            headers={"api-key": self.api_key}
        )
        response.raise_for_status()
        url = response.json()["output_url"]
        return Image.open(requests.get(url, stream=True).raw)

    def mejorar_calidad(self, imagen: Image.Image) -> Image.Image:
        buffer = self._convertir_a_buffer(imagen)
        response = requests.post(
            self.url_mejorar_calidad,
            files={"image": buffer},
            headers={"api-key": self.api_key}
        )
        response.raise_for_status()
        url = response.json()["output_url"]
        return Image.open(requests.get(url, stream=True).raw)
