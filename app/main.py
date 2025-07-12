import tkinter as tk
from tkinter import messagebox
from app.supabaseconn import SupabaseDB

class VentanaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("Inicio - App Radiografías")
        self.root.geometry("1000x800")

        self.db = None
        self.conectado = False

        # Frame principal (para bienvenida y botones)
        self.frame_principal = tk.Frame(root)
        self.frame_principal.pack(fill="both", expand=True)

        self.label_bienvenida = tk.Label(self.frame_principal, text="Bienvenido", font=("Arial", 16))
        self.label_bienvenida.pack(pady=20)

        self.btn_login = tk.Button(self.frame_principal, text="Iniciar sesión", command=self.mostrar_login)
        self.btn_login.pack(pady=10)

        self.btn_solicitar = tk.Button(self.frame_principal, text="Solicitar una cuenta", command=self.solicitar_cuenta)
        self.btn_solicitar.pack(pady=10)

        # Frame login (inicialmente oculto)
        self.frame_login = tk.Frame(root)

        tk.Label(self.frame_login, text="Correo electrónico:").pack(pady=5)
        self.entry_email = tk.Entry(self.frame_login, width=30)
        self.entry_email.pack()

        tk.Label(self.frame_login, text="Contraseña:").pack(pady=5)
        self.entry_password = tk.Entry(self.frame_login, width=30, show="*")
        self.entry_password.pack()

        self.btn_entrar = tk.Button(self.frame_login, text="Entrar", command=self.intentar_login)
        self.btn_entrar.pack(pady=20)

        self.label_mensaje = tk.Label(self.frame_login, text="", fg="red")
        self.label_mensaje.pack()

        self.root.after(100, self.verificar_conexion)

    def verificar_conexion(self):
        try:
            self.db = SupabaseDB()
            self.conectado = True
        except Exception as e:
            print("Error de conexión con Supabase:", e)
            self.conectado = False
            messagebox.showerror("Error", "No se pudo conectar con la base de datos.")

    def mostrar_login(self):
        if not self.conectado:
            messagebox.showwarning("Sin conexión", "No puedes iniciar sesión sin conexión a la base de datos.")
            return

        # Ocultar frame principal y mostrar login
        self.frame_principal.pack_forget()
        self.frame_login.pack(fill="both", expand=True)

        # Limpiar campos y mensaje
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.label_mensaje.config(text="")

    def intentar_login(self):
        email = self.entry_email.get()
        password = self.entry_password.get()

        if not email or not password:
            self.label_mensaje.config(text="Por favor, ingresa email y contraseña.", fg="red")
            return

        try:
            es_valido = self.db.verificar_usuario(email, password)

            if es_valido:
                print("logueado")
                # Limpiar toda la ventana
                for widget in self.root.winfo_children():
                    widget.destroy()

                # Mostrar solo mensaje de éxito
                mensaje = tk.Label(self.root, text="Inicio de sesión correcto.", font=("Arial", 20), fg="green")
                mensaje.pack(expand=True)

            else:
                self.label_mensaje.config(text="Credenciales incorrectas.", fg="red")

        except Exception as e:
            self.label_mensaje.config(text=f"Algo salió mal: {e}", fg="red")


    def solicitar_cuenta(self):
        messagebox.showinfo("Solicitar cuenta", "Para solicitar una cuenta, contacta con el administrador del sistema.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInicio(root)
    root.mainloop()
