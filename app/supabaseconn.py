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
        self.usuario_logueado = None  # Guardaremos aquí el usuario

    def verificar_usuario(self, correo: str, contrasena: str) -> bool:
        respuesta = self.supabase.table("usuarios") \
            .select("*") \
            .eq("correo", correo) \
            .eq("contrasena", contrasena) \
            .execute()

        if len(respuesta.data) > 0:
            self.usuario_actual = correo  # Guardamos el correo para futuras consultas
            return True
        return False


    def obtener_usuario_id(self):
        """
        Devuelve el correo del usuario logueado.
        """
        if self.usuario_logueado:
            return self.usuario_logueado.get("correo")  # ahora el ID es el correo
        return None
    
    def insertar_paciente(self, user_id, paciente_id, numero_radiografia, patologias):
        self.supabase.table("pacientes_usuario").insert({
            "user_id": user_id,
            "paciente_id": paciente_id,
            "numero_radiografia": numero_radiografia,
            "patologias": patologias
        }).execute()
