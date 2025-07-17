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
            # Guarda solo el correo, no todo el objeto
            self.usuario_logueado = correo
            return True
        return False

    def obtener_usuario_id(self):
        return self.usuario_logueado

    
    def insertar_paciente(self, user_id, paciente_id, numero_radiografia, patologias):
        self.supabase.table("pacientes_usuario").insert({
            "user_id": user_id,
            "paciente_id": paciente_id,
            "numero_radiografia": numero_radiografia,
            "patologias": patologias,
            "ruta_imagen": ""

        }).execute()

    def get_historial_por_dni(self, dni, user_id):
        response = self.supabase.table("pacientes_usuario") \
            .select("*") \
            .eq("paciente_id", dni) \
            .eq("user_id", user_id) \
            .execute()

        return response.data

def paciente_existe(self, paciente_id):
    response = self.supabase.table("pacientes_usuario") \
        .select("paciente_id") \
        .eq("paciente_id", paciente_id) \
        .execute()
    return len(response.data) > 0

def crear_paciente_simple(self, paciente_id):
    # Insertar paciente con solo paciente_id, sin patologías ni timestamp
    self.supabase.table("pacientes_usuario").insert({
        "paciente_id": paciente_id,
        "numero_radiografia": 0,
        "patologias": [],
        "ruta_imagen": ""

    }).execute()

def insertar_radiografia(self, user_id, paciente_id, numero_radiografia, patologias, ruta_imagen):
    # Aquí debes guardar ruta_imagen (idealmente URL de Supabase Storage)
    self.supabase.table("pacientes_usuario").insert({
        "user_id": user_id,
        "paciente_id": paciente_id,
        "numero_radiografia": numero_radiografia,
        "patologias": patologias,
        "ruta_imagen": ruta_imagen
    }).execute()
