import tkinter as tk
from tkinter import messagebox
from app.supabaseconn import SupabaseDB

# Intentar conexión con Supabase
try:
    db = SupabaseDB()
    conectado = True
except Exception as e:
    print("Error de conexión con Supabase:", e)
    conectado = False


class VentanaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio - App Radiografías")
        self.root.geometry("1000x800")

        label = tk.Label(root, text="Bienvenido", font=("Arial", 16))
        label.pack(pady=20)

        btn_login = tk.Button(root, text="Iniciar sesión", command=self.login)
        btn_login.pack(pady=10)

        btn_solicitar = tk.Button(root, text="Solicitar una cuenta", command=self.solicitar_cuenta)
        btn_solicitar.pack(pady=10)

        if not conectado:
            messagebox.showerror("Error", "No se pudo conectar con la base de datos.")

    def login(self):
        # Aquí luego irá la ventana real de login
        messagebox.showinfo("Login", "Aquí irá la pantalla de login.")

    def solicitar_cuenta(self):
        messagebox.showinfo("Solicitar cuenta", "Para solicitar una cuenta, contacta con el administrador del sistema.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInicio(root)
    root.mainloop()
