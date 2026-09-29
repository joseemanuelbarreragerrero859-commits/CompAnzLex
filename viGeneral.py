import tkinter as tk
from tkinter import messagebox

# 1. Contenedor global sugerido para almacenar los AFNs antes de guardarlos en archivo
afns_en_memoria = {}
contador_afn = 1  # Para generar IDs automáticos si se prefiere

class InterfazCompilador:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico - Thompson")
        self.root.geometry("500x350")

        # Frame contenedor dinámico donde se cargarán las diferentes vistas
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.crear_menu()
        self.mostrar_vista_crear_basico() # Vista por defecto al iniciar

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        
        # Menú desplegable THOMPSON
        menu_thompson = tk.Menu(menubar, tearoff=0)
        menu_thompson.add_command(label="Crear AFN Básico", command=self.mostrar_vista_crear_basico)
        menu_thompson.add_command(label="Unir AFNs", command=lambda: print("Cargar vista Unir"))
        menu_thompson.add_command(label="Concatenar", command=lambda: print("Cargar vista Concatenar"))
        menu_thompson.add_command(label="Cerradura Positiva", command=lambda: print("Cargar vista Cerradura Positiva"))
        menu_thompson.add_command(label="Cerradura de Kleen", command=lambda: print("Cargar vista Cerradura de Kleen"))
        menu_thompson.add_command(label="Opcional", command=lambda: print("Cargar vista Opcional"))
        menu_thompson.add_separator()
        menu_thompson.add_command(label="Ver AFN", command=lambda: print("Cargar vista Ver AFN"))
        
        menubar.add_cascade(label="THOMPSON", menu=menu_thompson)
        self.root.config(menu=menubar)

    def limpiar_frame(self):
        # Destruye los widgets actuales del frame para montar la nueva vista
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_vista_crear_basico(self):
        self.limpiar_frame()
        
        # Título
        tk.Label(self.main_frame, text="CREAR BÁSICO", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")

        # Fila Simb 1
        tk.Label(self.main_frame, text="Simb 1").grid(row=1, column=0, pady=10, sticky="e")
        entrada_simb1 = tk.Entry(self.main_frame, width=15)
        entrada_simb1.grid(row=1, column=1, padx=10, pady=10)
        tk.Label(self.main_frame, text="(1 CHAR)").grid(row=1, column=2, sticky="w")

        # Fila Simb 2
        tk.Label(self.main_frame, text="Simb 2").grid(row=2, column=0, pady=10, sticky="e")
        entrada_simb2 = tk.Entry(self.main_frame, width=15)
        entrada_simb2.grid(row=2, column=1, padx=10, pady=10)
        tk.Label(self.main_frame, text="(1 CHAR)").grid(row=2, column=2, sticky="w")

        # Función que se ejecuta al presionar "CREAR"
        def accion_crear():
            global contador_afn
            s1 = entrada_simb1.get()
            s2 = entrada_simb2.get() if entrada_simb2.get() != "" else None
            
            if not s1:
                messagebox.showerror("Error", "El Simb 1 es obligatorio")
                return
                
            # AQUÍ SE CONECTA CON TU BACKEND:
            # nuevo_afn = AFN().CrearBasico(s1, s2)
            
            # Simulamos el objeto guardado en el contenedor global
            id_afn = f"AFN_{contador_afn}"
            afns_en_memoria[id_afn] = {"simb1": s1, "simb2": s2} # En producción: afns_en_memoria[id_afn] = nuevo_afn
            contador_afn += 1
            
            messagebox.showinfo("Éxito", f"Se creó el autómata {id_afn} correctamente.\n\nContenedor actual: {list(afns_en_memoria.keys())}")
            
            # Limpiar campos
            entrada_simb1.delete(0, tk.END)
            entrada_simb2.delete(0, tk.END)

        # Botón CREAR
        tk.Button(self.main_frame, text="CREAR", command=accion_crear, width=10, relief="solid", borderwidth=1).grid(row=3, column=0, columnspan=2, pady=30)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCompilador(root)
    root.mainloop()