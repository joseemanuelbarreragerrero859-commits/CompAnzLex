import tkinter as tk
from tkinter import ttk, messagebox

# Contenedor global de AFNs
afns_en_memoria = {}
contador_afn = 1

class InterfazCompilador:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico - Thompson")
        self.root.geometry("600x500")

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.crear_menu()
        self.mostrar_vista_crear_basico()

    def crear_menu(self):
        menubar = tk.Menu(self.root)
        
        menu_thompson = tk.Menu(menubar, tearoff=0)
        menu_thompson.add_command(label="Crear AFN Básico", command=self.mostrar_vista_crear_basico)
        menu_thompson.add_command(label="Unir AFNs", command=self.mostrar_vista_unir)
        menu_thompson.add_command(label="Concatenar", command=self.mostrar_vista_concatenar)
        menu_thompson.add_command(label="Cerradura Positiva", command=self.mostrar_vista_cerradura_pos)
        menu_thompson.add_command(label="Cerradura de Kleen", command=self.mostrar_vista_cerradura_kleen)
        menu_thompson.add_command(label="Opcional", command=self.mostrar_vista_opcional)
        menu_thompson.add_separator()
        menu_thompson.add_command(label="Unión para Analizador Léxico", command=self.mostrar_vista_union_lexico)
        menu_thompson.add_command(label="Convertir AFN a AFD", command=self.mostrar_vista_convertir_afd)
        
        menubar.add_cascade(label="AFN's", menu=menu_thompson)
        self.root.config(menu=menubar)

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- VISTAS EXISTENTES MODIFICADAS PARA CONECTAR BACKEND (SIMULADO) ---
    def mostrar_vista_crear_basico(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="CREAR BÁSICO", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        
        tk.Label(self.main_frame, text="Simb 1").grid(row=1, column=0, pady=10, sticky="e")
        entrada_simb1 = tk.Entry(self.main_frame, width=15)
        entrada_simb1.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="Simb 2").grid(row=2, column=0, pady=10, sticky="e")
        entrada_simb2 = tk.Entry(self.main_frame, width=15)
        entrada_simb2.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="ID AFN").grid(row=3, column=0, pady=10, sticky="e")
        entrada_id = tk.Entry(self.main_frame, width=15)
        entrada_id.grid(row=3, column=1, padx=10, pady=10)

        def accion_crear():
            global contador_afn
            s1 = entrada_simb1.get()
            s2 = entrada_simb2.get() if entrada_simb2.get() != "" else None
            id_afn = entrada_id.get()
            
            if not s1:
                messagebox.showerror("Error", "El Simb 1 es obligatorio")
                return
            if not id_afn:
                id_afn = f"AFN_{contador_afn}"
                contador_afn += 1
                
            afns_en_memoria[id_afn] = {"tipo": "basico", "simb1": s1, "simb2": s2} 
            messagebox.showinfo("Éxito", f"AFN '{id_afn}' creado correctamente.")
            entrada_simb1.delete(0, tk.END)
            entrada_simb2.delete(0, tk.END)
            entrada_id.delete(0, tk.END)

        tk.Button(self.main_frame, text="CREAR", command=accion_crear, width=10).grid(row=4, column=0, columnspan=2, pady=20)

    # --- NUEVAS VISTAS THOMPSON SIMPLES ---
    def mostrar_vista_unir(self):
        self._vista_operacion_doble("UNIR AFN")

    def mostrar_vista_concatenar(self):
        self._vista_operacion_doble("CONCATENAR AFNs")

    def _vista_operacion_doble(self, titulo):
        self.limpiar_frame()
        tk.Label(self.main_frame, text=titulo, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        opciones_afn = list(afns_en_memoria.keys())

        tk.Label(self.main_frame, text="AFN 1").grid(row=1, column=0, pady=10, sticky="e")
        combo_afn1 = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=12)
        combo_afn1.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="AFN 2").grid(row=2, column=0, pady=10, sticky="e")
        combo_afn2 = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=12)
        combo_afn2.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="ID Nuevo AFN").grid(row=3, column=0, pady=10, sticky="e")
        entrada_id = tk.Entry(self.main_frame, width=15)
        entrada_id.grid(row=3, column=1, padx=10, pady=10)

        tk.Button(self.main_frame, text="APLICAR", width=10).grid(row=4, column=0, columnspan=2, pady=20)

    def mostrar_vista_cerradura_pos(self):
        self._vista_operacion_simple("CERRADURA POSITIVA")

    def mostrar_vista_cerradura_kleen(self):
        self._vista_operacion_simple("CERRADURA DE KLEEN")

    def mostrar_vista_opcional(self):
        self._vista_operacion_simple("OPERACIÓN OPCIONAL")

    def _vista_operacion_simple(self, titulo):
        self.limpiar_frame()
        tk.Label(self.main_frame, text=titulo, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        opciones_afn = list(afns_en_memoria.keys())

        tk.Label(self.main_frame, text="Seleccionar AFN").grid(row=1, column=0, pady=10, sticky="e")
        combo_afn = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=12)
        combo_afn.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="ID Nuevo AFN").grid(row=2, column=0, pady=10, sticky="e")
        entrada_id = tk.Entry(self.main_frame, width=15)
        entrada_id.grid(row=2, column=1, padx=10, pady=10)

        tk.Button(self.main_frame, text="APLICAR", width=15).grid(row=3, column=0, columnspan=2, pady=20)

    # --- VISTAS AVANZADAS (Según los videos de referencia) ---
    def mostrar_vista_union_lexico(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="UNIÓN PARA ANALIZADOR LÉXICO", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        tk.Label(self.main_frame, text="Selecciona los AFNs a unir y asigna sus Tokens").grid(row=1, column=0, columnspan=3, sticky="w")
        
        # Aquí crearíamos una lista dinámica o un Treeview para seleccionar múltiples AFNs y poner un Entry para el Token
        frame_lista = tk.Frame(self.main_frame)
        frame_lista.grid(row=2, column=0, columnspan=3, pady=10, sticky="w")
        
        # Dummy labels simulando la vista del video
        tk.Label(frame_lista, text="ID AFN").grid(row=0, column=0, padx=10)
        tk.Label(frame_lista, text="Token").grid(row=0, column=1, padx=10)
        
        opciones_afn = list(afns_en_memoria.keys())
        for idx, afn_id in enumerate(opciones_afn):
            tk.Checkbutton(frame_lista, text=afn_id).grid(row=idx+1, column=0, sticky="w")
            tk.Entry(frame_lista, width=10).grid(row=idx+1, column=1)

        tk.Label(self.main_frame, text="ID Nuevo AFN Léxico:").grid(row=3, column=0, pady=10, sticky="e")
        tk.Entry(self.main_frame, width=15).grid(row=3, column=1, sticky="w")
        
        tk.Button(self.main_frame, text="UNIR AFNs", width=15).grid(row=4, column=0, columnspan=2, pady=10)

    def mostrar_vista_convertir_afd(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="CONVERTIR AFN A AFD", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        
        opciones_afn = list(afns_en_memoria.keys())
        tk.Label(self.main_frame, text="Seleccionar AFN").grid(row=1, column=0, pady=10, sticky="e")
        combo_afn = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=15)
        combo_afn.grid(row=1, column=1, padx=10, pady=10)
        
        tk.Button(self.main_frame, text="Convertir y Guardar").grid(row=1, column=2, padx=10)

        # Configuración del DataGridView equivalente (Treeview en tkinter) para ver la matriz
        frame_tabla = tk.Frame(self.main_frame)
        frame_tabla.grid(row=2, column=0, columnspan=3, pady=10)
        
        columnas = ("Estado", "a", "b", "c", "Token")
        tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, width=80, anchor="center")
            
        tabla.pack(side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCompilador(root)
    root.mainloop()