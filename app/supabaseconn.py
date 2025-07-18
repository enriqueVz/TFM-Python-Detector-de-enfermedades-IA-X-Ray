from supabase import create_client, Client
from dotenv import load_dotenv
import uuid  # Para nombres únicos de archivos

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
            "user_id": self.usuario_logueado, 
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



    def subir_radiografia(self, archivo_path: str) -> str:
        bucket_name = "xrays"
        archivo_nombre = f"{uuid.uuid4().hex}_{os.path.basename(archivo_path)}"

        with open(archivo_path, "rb") as archivo:
            response = self.supabase.storage.from_(bucket_name).upload(archivo_nombre, archivo.read())

        if response.get("error"):
            print("Error al subir imagen:", response["error"])
            return None

        # Generar URL pública
        url = self.supabase.storage.from_(bucket_name).get_public_url(archivo_nombre)
        return url
    
    def guardar_radiografia_completa(self, archivo_path, user_id, paciente_id, numero_radiografia, patologias):
        url = self.subir_radiografia(archivo_path)
        if not url:
            print("Error: No se pudo subir la imagen al bucket.")
            return False

        self.insertar_radiografia(
            user_id=user_id,
            paciente_id=paciente_id,
            numero_radiografia=numero_radiografia,
            patologias=patologias,
            ruta_imagen=url
        )
        return True
