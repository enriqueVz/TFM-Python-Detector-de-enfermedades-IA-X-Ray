from supabase import create_client, Client
from dotenv import load_dotenv
import os

class SupabaseDB:
    def __init__(self):
        load_dotenv()  # Carga variables desde .env
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        if not url or not key:
            raise ValueError("Faltan SUPABASE_URL o SUPABASE_KEY en el archivo .env")

        self.supabase: Client = create_client(url, key)

    def verificar_usuario(self, correo: str, contrasena: str) -> bool:
        """
        Verifica si el usuario existe con la contraseña dada.
        """
        respuesta = self.supabase.table("usuarios") \
            .select("*") \
            .eq("correo", correo) \
            .eq("contrasena", contrasena) \
            .execute()

        return len(respuesta.data) > 0
