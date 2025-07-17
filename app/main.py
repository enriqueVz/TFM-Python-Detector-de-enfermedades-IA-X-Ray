import tkinter as tk
from app.supabaseconn import SupabaseDB
import threading
from PIL import Image, ImageTk
import webbrowser
import os
import random
from tkinter import messagebox
import pandas as pd
import re

class PantallaCarga:
    def __init__(self, root, on_conexion_verificada):
        self.root = root
        self.on_conexion_verificada = on_conexion_verificada

        self.frame = tk.Frame(root)
        self.frame.pack(fill="both", expand=True)

        self.label_cargando = tk.Label(self.frame, text="Conectando a la base de datos...", font=("Arial", 16))
        self.label_cargando.pack(pady=20)

        self.spinner_label = tk.Label(self.frame, text="⠋", font=("Arial", 40))
        self.spinner_label.pack(pady=10)

        self.spinner_index = 0
        self.spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]

        self.root.after(100, self.animar_spinner)
        threading.Thread(target=self.verificar_conexion, daemon=True).start()

    def animar_spinner(self):
        self.spinner_label.config(text=self.spinner_frames[self.spinner_index])
        self.spinner_index = (self.spinner_index + 1) % len(self.spinner_frames)
        self.root.after(100, self.animar_spinner)

    def verificar_conexion(self):
        try:
            db = SupabaseDB()
            conectado = True
        except Exception as e:
            print("Error de conexión con Supabase:", e)
            conectado = False
            db = None

        self.root.after(500, lambda: self.finalizar_carga(conectado, db))

    def finalizar_carga(self, conectado, db):
        self.frame.pack_forget()
        self.on_conexion_verificada(conectado, db)


class PantallaPrincipal:
    def __init__(self, root, mostrar_login, solicitar_cuenta):
        self.root = root
        self.mostrar_login = mostrar_login
        self.solicitar_cuenta = solicitar_cuenta

        self.frame = tk.Frame(root)

        self.label_bienvenida = tk.Label(self.frame, text="Bienvenido", font=("Arial", 16))
        self.label_bienvenida.pack(pady=20)

        self.btn_login = tk.Button(self.frame, text="Iniciar sesión", command=self.mostrar_login)
        self.btn_login.pack(pady=10)

        self.btn_solicitar = tk.Button(self.frame, text="Solicitar una cuenta", command=self.solicitar_cuenta)
        self.btn_solicitar.pack(pady=10)

        # Frame redes sociales
        self.frame_redes = tk.Frame(root)

        ruta_assets = os.path.join("assets", "icons")
        img_linkedin = Image.open(os.path.join(ruta_assets, "linkedin.png")).resize((80, 80), Image.Resampling.LANCZOS)
        img_github = Image.open(os.path.join(ruta_assets, "github.png")).resize((80, 80), Image.Resampling.LANCZOS)
        img_kaggle = Image.open(os.path.join(ruta_assets, "kaggle.png")).resize((100, 80), Image.Resampling.LANCZOS)

        self.icon_linkedin = ImageTk.PhotoImage(img_linkedin)
        self.icon_github = ImageTk.PhotoImage(img_github)
        self.icon_kaggle = ImageTk.PhotoImage(img_kaggle)

        # Funciones abrir enlaces
        def abrir_linkedin(event=None):
            webbrowser.open_new("https://www.linkedin.com/in/enrique-v%C3%A1zquez-iriarte-a2a193302/")

        def abrir_github(event=None):
            webbrowser.open_new("https://github.com/enriqueVz")

        def abrir_kaggle(event=None):
            webbrowser.open_new("https://www.kaggle.com/datasets/nih-chest-xrays/data")

        btn_linkedin = tk.Button(self.frame_redes, image=self.icon_linkedin, cursor="hand2")
        btn_linkedin.grid(row=0, column=0, padx=30)
        btn_linkedin.bind("<Button-1>", abrir_linkedin)

        btn_github = tk.Button(self.frame_redes, image=self.icon_github, cursor="hand2")
        btn_github.grid(row=0, column=1, padx=30)
        btn_github.bind("<Button-1>", abrir_github)

        btn_kaggle = tk.Button(self.frame_redes, image=self.icon_kaggle, cursor="hand2")
        btn_kaggle.grid(row=0, column=2, padx=30)
        btn_kaggle.bind("<Button-1>", abrir_kaggle)

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
        self.frame_redes.pack(side="bottom", pady=40)

    def ocultar(self):
        self.frame.pack_forget()
        self.frame_redes.pack_forget()


class PantallaLogin:
    def __init__(self, root, intentar_login, volver_menu):
        self.root = root
        self.intentar_login = intentar_login
        self.volver_menu = volver_menu

        self.frame = tk.Frame(root)

        tk.Label(self.frame, text="Correo electrónico:").pack(pady=5)
        self.entry_email = tk.Entry(self.frame, width=30)
        self.entry_email.pack()

        tk.Label(self.frame, text="Contraseña:").pack(pady=5)
        self.entry_password = tk.Entry(self.frame, width=30, show="*")
        self.entry_password.pack()

        self.btn_entrar = tk.Button(self.frame, text="Entrar", command=self.intentar_login)
        self.btn_entrar.pack(pady=20)

        self.btn_volver = tk.Button(self.frame, text="Volver", command=self.volver_menu)
        self.btn_volver.pack(pady=20)

        self.label_mensaje = tk.Label(self.frame, text="", fg="red")
        self.label_mensaje.pack()

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.label_mensaje.config(text="")

    def ocultar(self):
        self.frame.pack_forget()


class PantallaPostLogin:
    def __init__(self, root, mostrar_radiografias, cerrar_sesion_callback, mostrar_historial_callback=None):
        self.root = root
        self.mostrar_radiografias = mostrar_radiografias
        self.cerrar_sesion_callback = cerrar_sesion_callback  # Guardamos el callback
        self.mostrar_historial_callback = mostrar_historial_callback


        self.frame = tk.Frame(root)

        self.label_bienvenida = tk.Label(self.frame, text="Inicio de sesión correcto", font=("Arial", 20), fg="green")
        self.label_bienvenida.pack(pady=40)

        self.btn_analizar = tk.Button(self.frame, text="Analizar radiografía", width=25, height=2)
        self.btn_analizar.pack(pady=10)

        self.btn_historial = tk.Button(self.frame, text="Historial de sus pacientes", width=25, height=2, command=self.mostrar_historial_callback)
        self.btn_historial.pack(pady=10)

        self.btn_stock = tk.Button(self.frame, text="Stock de radiografías", width=25, height=2, command=self.mostrar_radiografias)
        self.btn_stock.pack(pady=10)

        self.btn_modelos = tk.Button(self.frame, text="Modelos disponibles", width=25, height=2)
        self.btn_modelos.pack(pady=10)

        self.btn_cerrar_sesion = tk.Button(self.frame, text="Cerrar sesión", width=25, height=2, command=self.cerrar_sesion_callback)
        self.btn_cerrar_sesion.pack(pady=10)

    def mostrar(self):
        self.frame.pack(fill="both", expand=True)

    def ocultar(self):
        self.frame.pack_forget()

class PantallaRadiografias(tk.Frame):
    def __init__(self, root, volver, controlador, carpeta=None):
        super().__init__(root)
        self.root = root
        self.volver = volver
        self.controlador = controlador
        self.tamano_original = self.root.geometry()
        self.pack(fill="both", expand=True)
        
        self.ruta_imgs = carpeta if carpeta else os.path.join("assets", "xrays")

        self.imagen_paths = [os.path.join(self.ruta_imgs, f) for f in os.listdir(self.ruta_imgs)
                             if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
        
        self.imgs_mostradas = []

        # --- Barra superior ---
        frame_botones = tk.Frame(self)
        frame_botones.pack(fill="x", pady=10, padx=10)

        btn_volver = tk.Button(frame_botones, text="Volver", command=self.volver_y_restaurar_tamano)
        btn_volver.pack(side="left")

        # Contenedor del botón aleatorio y el FAQ, alineados a la derecha
        frame_derecha = tk.Frame(frame_botones)
        frame_derecha.pack(side="right")

        btn_random = tk.Button(frame_derecha, text="Mostrar radiografías aleatorias", command=self.mostrar_imagenes_aleatorias)
        btn_random.pack(side="left", padx=(0, 10))

        btn_masa = tk.Button(frame_derecha, text="Mostrar solo masa", command=self.controlador.mostrar_radiografias_masa)
        btn_masa.pack(side="left", padx=(0, 10))

        btn_pneumonia = tk.Button(frame_derecha, text="Mostrar solo pneumonia", command=self.controlador.mostrar_radiografias_pneumonia)
        btn_pneumonia.pack(side="left", padx=(0, 10))

        frame_faq = tk.Frame(self)
        frame_faq.pack(pady=(0, 5))

        ruta_faq = os.path.join("assets", "icons", "faq.png")
        img_faq = Image.open(ruta_faq).resize((30, 30), Image.Resampling.LANCZOS)
        self.icon_faq = ImageTk.PhotoImage(img_faq)

        btn_faq = tk.Button(frame_faq, image=self.icon_faq, command=lambda: controlador.mostrar_faq("radiografias"), cursor="hand2", bd=0)
        btn_faq.pack()

        # --- Área scrollable ---
        self.frame_imgs = tk.Frame(self)
        self.frame_imgs.pack(fill="both", expand=True)

        self.canvas = tk.Canvas(self.frame_imgs)
        self.scrollbar = tk.Scrollbar(self.frame_imgs, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.mostrar_imagenes_aleatorias()
    
    def volver_y_restaurar_tamano(self):
        self.root.geometry(self.tamano_original)
        self.volver()

    def mostrar_imagenes_aleatorias(self):
        # Limpiar imágenes anteriores
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.imgs_mostradas.clear()

        imgs_seleccionadas = random.sample(self.imagen_paths, min(100, len(self.imagen_paths)))

        for i in range(0, len(imgs_seleccionadas), 2):
            # Crear una fila centrada
            fila = tk.Frame(self.scrollable_frame)
            fila.pack(pady=10)

            # Fila con 2 imágenes, centradas
            fila.columnconfigure(0, weight=1)
            fila.columnconfigure(1, weight=1)

            for j in range(2):
                if i + j >= len(imgs_seleccionadas):
                    break

                path = imgs_seleccionadas[i + j]
                img = Image.open(path)
                img.thumbnail((400, 300))
                img_tk = ImageTk.PhotoImage(img)

                contenedor = tk.Frame(fila, padx=10)
                contenedor.pack(side="left", expand=True)

                lbl_img = tk.Label(contenedor, image=img_tk, borderwidth=2, relief="groove")
                lbl_img.pack()

                self.imgs_mostradas.append(img_tk)

class PantallaHistorialPacientes(tk.Frame):
    def __init__(self, root, volver_callback, db, user_id):
        super().__init__(root)
        self.root = root
        self.volver_callback = volver_callback
        self.db = db
        self.user_id = user_id

        self.label_mensaje = tk.Label(self, text="", fg="red", font=("Arial", 12))
        self.label_mensaje.pack()

        self.pack(fill="both", expand=True)
        self.mostrar_busqueda()

    def mostrar_busqueda(self):
        self.limpiar_contenido()

        label = tk.Label(self, text="Consultar historial de paciente", font=("Arial", 16))
        label.pack(pady=20)

        frame_busqueda = tk.Frame(self)
        frame_busqueda.pack()

        tk.Label(frame_busqueda, text="DNI del paciente:").pack(side="left")
        self.entry_dni = tk.Entry(frame_busqueda)
        self.entry_dni.pack(side="left", padx=10)

        btn_buscar = tk.Button(frame_busqueda, text="Buscar", command=self.buscar_historial)
        btn_buscar.pack(side="left")

        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        btn_volver = tk.Button(frame_botones, text="Volver", command=self.volver)
        btn_volver.pack(side="left", padx=10)

        btn_añadir = tk.Button(frame_botones, text="Añadir paciente", command=self.abrir_formulario_paciente)
        btn_añadir.pack(side="left", padx=10)

        self.resultado_texto = tk.Text(self, width=80, height=20)
        self.resultado_texto.pack(pady=20)

    def buscar_historial(self):
        dni = self.entry_dni.get().strip()
        self.label_mensaje.config(text="")
        self.resultado_texto.delete(1.0, tk.END)

        if not dni:
            self.label_mensaje.config(text="Por favor, introduce un DNI.")
            return

        if not re.match(r'^\d{8}[A-Z]$', dni):
            self.label_mensaje.config(text="Formato de DNI inválido. Debe ser 8 números seguidos de una letra mayúscula.")
            return

        try:
            resultados = self.db.get_historial_por_dni(dni, self.user_id)

            if not resultados:
                self.label_mensaje.config(text="No hay un historial para este número de documento.")
                return

            df = pd.DataFrame(resultados)
            self.resultado_texto.insert(tk.END, df.to_string(index=False))

        except Exception:
            self.label_mensaje.config(text="No se pudo recuperar el historial, revise la veracidad de sus datos.")

    def abrir_formulario_paciente(self):
        self.limpiar_contenido()
        self.label_mensaje.config(text="")

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="DNI del paciente:").grid(row=0, column=0, padx=10, pady=5)
        entry_dni = tk.Entry(form_frame)
        entry_dni.grid(row=0, column=1)

        tk.Label(form_frame, text="Nº Radiografía:").grid(row=1, column=0, padx=10, pady=5)
        entry_radiografia = tk.Entry(form_frame)
        entry_radiografia.insert(0, "0")
        entry_radiografia.grid(row=1, column=1)

        tk.Label(form_frame, text="Patologías (separadas por comas):").grid(row=2, column=0, padx=10, pady=5)
        entry_patologias = tk.Entry(form_frame)
        entry_patologias.grid(row=2, column=1)

        def registrar():
            dni = entry_dni.get().strip()
            num_rad = entry_radiografia.get().strip()
            patologias = entry_patologias.get().strip().split(",")

            if not dni or not num_rad:
                self.label_mensaje.config(text="Todos los campos son obligatorios.")
                return

            if not re.match(r'^\d{8}[A-Z]$', dni):
                self.label_mensaje.config(text="DNI inválido: deben ser 8 números seguidos de una letra mayúscula.")
                return

            try:
                self.db.insertar_paciente(
                    user_id=self.user_id,
                    paciente_id=dni,
                    numero_radiografia=num_rad,
                    patologias=[p.strip() for p in patologias if p.strip()]
                )
                self.label_mensaje.config(text="Paciente añadido con éxito.", fg="green")
                self.mostrar_busqueda()
            except Exception:
                self.label_mensaje.config(text="Error al guardar el paciente.", fg="red")

        btn_guardar = tk.Button(form_frame, text="Guardar", command=registrar)
        btn_guardar.grid(row=3, column=0, columnspan=2, pady=10)

    def limpiar_contenido(self):
        for widget in self.winfo_children():
            if widget not in [self.label_mensaje]:
                widget.destroy()

    def volver(self):
        self.pack_forget()
        self.volver_callback()
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("CribaDOC")
        self.centrar_ventana(1000, 740)

        self.db = None
        self.conectado = False

        # Inicializar pantallas
        self.pantalla_carga = PantallaCarga(root, self.on_conexion_verificada)
        self.pantalla_principal = PantallaPrincipal(root, self.mostrar_login, self.solicitar_cuenta)
        self.pantalla_login = PantallaLogin(root, self.intentar_login, self.volver_menu)
        self.pantalla_post_login = None
        self.pantalla_radiografias = None

    def on_conexion_verificada(self, conectado, db):
        self.conectado = conectado
        self.db = db
        if conectado:
            self.pantalla_principal.mostrar()
        else:
            error_label = tk.Label(self.root, text="No se pudo conectar con la base de datos.", font=("Arial", 16), fg="red")
            error_label.pack(pady=20)

    def mostrar_login(self):
        if not self.conectado:
            return
        self.pantalla_principal.ocultar()
        self.pantalla_login.mostrar()

    def volver_menu(self):
        self.pantalla_login.ocultar()
        self.pantalla_principal.mostrar()

    def intentar_login(self):
        email = self.pantalla_login.entry_email.get()
        password = self.pantalla_login.entry_password.get()

        if not email or not password:
            self.pantalla_login.label_mensaje.config(text="Por favor, ingresa email y contraseña.", fg="red")
            return

        try:
            es_valido = self.db.verificar_usuario(email, password)

            if es_valido:
                self.pantalla_login.ocultar()
                # Crear pantalla post login si no existe
                self.pantalla_post_login = PantallaPostLogin(
                self.root,
                self.mostrar_radiografias,
                self.cerrar_sesion,
                self.mostrar_historial  # Este es el nuevo callback para el botón "Historial"
                )
                self.pantalla_post_login.mostrar()
            else:
                self.pantalla_login.label_mensaje.config(text="Credenciales incorrectas.", fg="red")

        except Exception as e:
            self.pantalla_login.label_mensaje.config(text=f"Algo salió mal: {e}", fg="red")

    def centrar_ventana(self, ancho, alto):
        self.root.update_idletasks()
        ancho_pantalla = self.root.winfo_screenwidth()
        alto_pantalla = self.root.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho // 2)
        y = (alto_pantalla // 2) - (alto // 2)
        self.root.geometry(f"{ancho}x{alto}+{x}+{y}")
        
    def mostrar_radiografias(self):
        if self.pantalla_post_login:
            self.pantalla_post_login.ocultar()
        if self.pantalla_radiografias is None:
            self.pantalla_radiografias = PantallaRadiografias(self.root, self.volver_post_login, self)
        self.centrar_ventana(680, 740)
        self.pantalla_radiografias.pack(fill="both", expand=True)

    def mostrar_radiografias_masa(self):
        if self.pantalla_post_login:
            self.pantalla_post_login.ocultar()
        if self.pantalla_radiografias:
            self.pantalla_radiografias.destroy()
        self.pantalla_radiografias = PantallaRadiografias(self.root, self.volver_post_login, self, carpeta="assets/masa")
        self.centrar_ventana(680, 740)
        self.pantalla_radiografias.pack(fill="both", expand=True)

    def mostrar_radiografias_pneumonia(self):
        if self.pantalla_post_login:
            self.pantalla_post_login.ocultar()
        if self.pantalla_radiografias:
            self.pantalla_radiografias.destroy()
        self.pantalla_radiografias = PantallaRadiografias(self.root, self.volver_post_login, self, carpeta="assets/pneumonia")
        self.centrar_ventana(680, 740)
        self.pantalla_radiografias.pack(fill="both", expand=True)

    def volver_post_login(self):
        if self.pantalla_radiografias:
            self.pantalla_radiografias.pack_forget()
            
        if hasattr(self, "pantalla_historial") and self.pantalla_historial:
            self.pantalla_historial.pack_forget()

        if self.pantalla_post_login:
            self.centrar_ventana(1000, 740)
            self.pantalla_post_login.mostrar()


    def cerrar_sesion(self):
        # Ocultar cualquier pantalla activa
        if self.pantalla_post_login:
            self.pantalla_post_login.ocultar()
        if self.pantalla_radiografias:
            self.pantalla_radiografias.pack_forget()

        self.centrar_ventana(1000, 740)
        self.pantalla_principal.mostrar()

    
    def mostrar_historial(self):
        if self.pantalla_post_login:
            self.pantalla_post_login.ocultar()
        if hasattr(self, "pantalla_historial") and self.pantalla_historial:
            self.pantalla_historial.pack_forget()
        self.pantalla_historial = PantallaHistorialPacientes(self.root, self.volver_post_login, self.db, self.db.usuario_actual)
        self.centrar_ventana(1000, 740)
        self.pantalla_historial.pack(fill="both", expand=True)

    def solicitar_cuenta(self):
        messagebox.showinfo("Solicitar cuenta", "Para solicitar una cuenta, contacta con el administrador del sistema.")

    def mostrar_faq(self, contexto):
        textos = {
            
            "radiografias": "Son sólo una pequeña parte de las radiografías usadas en el entrenamiento (5.000 de las 120.000 del dataset)."
        }

        texto_a_mostrar = textos.get(contexto, "Información no disponible.")

        messagebox.showinfo("Ayuda - FAQ", texto_a_mostrar)
    



if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()