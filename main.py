from dotenv import load_dotenv
import os
from app.api.api_manager import ApiManager
from app.interfaz_grafica.interfaz import InterfazEditor

load_dotenv()
api_key = os.getenv("API_KEY")

api_manager = ApiManager(api_key=api_key)

if __name__ == "__main__":
    InterfazEditor(api_manager=api_manager)

