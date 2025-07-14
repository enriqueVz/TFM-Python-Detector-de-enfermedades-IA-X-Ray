import tkinter as tk
from app.supabaseconn import SupabaseDB
import threading
from PIL import Image, ImageTk
import webbrowser
import os

class VentanaInicio:
    def __init__(self, root):
        self.root = root
        self.root.title("CribaDOC")
        self.root.geometry("1000x800")

        self.db = None
        self.conectado = False

        # Frame de carga inicial
        self.frame_cargando = tk.Frame(root)
        self.frame_cargando.pack(fill="both", expand=True)

        self.label_cargando = tk.Label(self.frame_cargando, text="Conectando a la base de datos...", font=("Arial", 16))
        self.label_cargando.pack(pady=20)

        self.spinner_label = tk.Label(self.frame_cargando, text="⠋", font=("Arial", 40))
        self.spinner_label.pack(pady=10)

        self.spinner_index = 0
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

        self.root.after(100, self.animar_spinner)
        threading.Thread(target=self.verificar_conexion, daemon=True).start()

        # Frame principal (menu de bienvenida)
        self.frame_principal = tk.Frame(root)

        self.label_bienvenida = tk.Label(self.frame_principal, text="Bienvenido", font=("Arial", 16))
        self.label_bienvenida.pack(pady=20)

        self.btn_login = tk.Button(self.frame_principal, text="Iniciar sesión", command=self.mostrar_login)
        self.btn_login.pack(pady=10)

        self.btn_solicitar = tk.Button(self.frame_principal, text="Solicitar una cuenta", command=self.solicitar_cuenta)
        self.btn_solicitar.pack(pady=10)

        #Redes 

        self.frame_redes = tk.Frame(self.root)

        # Cargar iconos
        ruta_assets = os.path.join("assets", "images")
        img_linkedin = Image.open(os.path.join(ruta_assets, "linkedin.png")).resize((80, 80), Image.Resampling.LANCZOS)
        img_github = Image.open(os.path.join(ruta_assets, "github.png")).resize((80, 80), Image.Resampling.LANCZOS)
        img_kaggle = Image.open(os.path.join(ruta_assets, "kaggle.png")).resize((100, 80), Image.Resampling.LANCZOS)

        self.icon_linkedin = ImageTk.PhotoImage(img_linkedin)
        self.icon_github = ImageTk.PhotoImage(img_github)
        self.icon_kaggle = ImageTk.PhotoImage(img_kaggle)

        # Funciones para abrir enlaces
        def abrir_linkedin(event=None):
            webbrowser.open_new("https://www.linkedin.com/in/enrique-v%C3%A1zquez-iriarte-a2a193302/")

        def abrir_github(event=None):
            webbrowser.open_new("https://github.com/enriqueVz")

        def abrir_kaggle(event=None):
            webbrowser.open_new("https://www.kaggle.com/datasets/nih-chest-xrays/data")

        # Crear botones con imagen y enlace
        btn_linkedin = tk.Button(self.frame_redes, image=self.icon_linkedin, cursor="hand2")
        btn_linkedin.grid(row=0, column=0, padx=30)
        btn_linkedin.bind("<Button-1>", abrir_linkedin)

        btn_github = tk.Button(self.frame_redes, image=self.icon_github, cursor="hand2")
        btn_github.grid(row=0, column=1, padx=30)
        btn_github.bind("<Button-1>", abrir_github)

        btn_kaggle = tk.Button(self.frame_redes, image=self.icon_kaggle, cursor="hand2")
        btn_kaggle.grid(row=0, column=2, padx=30)
        btn_kaggle.bind("<Button-1>", abrir_kaggle)

        # Frame login
        self.frame_login = tk.Frame(root)

        tk.Label(self.frame_login, text="Correo electrónico:").pack(pady=5)
        self.entry_email = tk.Entry(self.frame_login, width=30)
        self.entry_email.pack()

        tk.Label(self.frame_login, text="Contraseña:").pack(pady=5)
        self.entry_password = tk.Entry(self.frame_login, width=30, show="*")
        self.entry_password.pack()

        self.btn_entrar = tk.Button(self.frame_login, text="Entrar", command=self.intentar_login)
        self.btn_entrar.pack(pady=20)

        self.btn_volver = tk.Button(self.frame_login, text="Volver", command=self.volver_menu)
        self.btn_volver.pack(pady=20)

        self.label_mensaje = tk.Label(self.frame_login, text="", fg="red")
        self.label_mensaje.pack()

    def volver_menu(self):
        self.frame_login.pack_forget()
        self.frame_principal.pack(fill="both", expand=True)

    def animar_spinner(self):
        self.spinner_label.config(text=self.spinner_frames[self.spinner_index])
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
        self.root.after(100, self.animar_spinner)

    def verificar_conexion(self):
        try:
            self.db = SupabaseDB()
            self.conectado = True
        except Exception as e:
            print("Error de conexión con Supabase:", e)
            self.conectado = False

        self.root.after(500, self.finalizar_carga)

    def finalizar_carga(self):
        self.frame_cargando.pack_forget()
        if self.conectado:
            self.frame_principal.pack(fill="both", expand=True)
            self.frame_redes.pack(side="bottom", pady=40)  # <-- Mostrar aquí
        else:
            error_label = tk.Label(self.root, text="No se pudo conectar con la base de datos.", font=("Arial", 16), fg="red")
            error_label.pack(pady=20)

    def mostrar_login(self):
        if not self.conectado:
            return

        self.frame_principal.pack_forget()
        self.frame_login.pack(fill="both", expand=True)

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
                # Limpiar toda la ventana
                for widget in self.root.winfo_children():
                    widget.destroy()

                # Mostrar pantalla principal tras login
                frame_post_login = tk.Frame(self.root)
                frame_post_login.pack(fill="both", expand=True)

                label_bienvenida = tk.Label(frame_post_login, text="Inicio de sesión correcto", font=("Arial", 20), fg="green")
                label_bienvenida.pack(pady=40)

                btn_analizar = tk.Button(frame_post_login, text="Analizar radiografía", width=25, height=2)
                btn_analizar.pack(pady=10)

                btn_stock = tk.Button(frame_post_login, text="Stock de radiografías", width=25, height=2)
                btn_stock.pack(pady=10)

                btn_modelos = tk.Button(frame_post_login, text="Modelos disponibles", width=25, height=2)
                btn_modelos.pack(pady=10)

            else:
                self.label_mensaje.config(text="Credenciales incorrectas.", fg="red")

        except Exception as e:
            self.label_mensaje.config(text=f"Algo salió mal: {e}", fg="red")

    def solicitar_cuenta(self):
        tk.messagebox.showinfo("Solicitar cuenta", "Para solicitar una cuenta, contacta con el administrador del sistema.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VentanaInicio(root)
    root.mainloop()
