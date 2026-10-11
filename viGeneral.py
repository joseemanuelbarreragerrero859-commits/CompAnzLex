import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog

# IMPORTACIÓN DE TU BACKEND LÓGICO
# Asegúrate de que AnzLex_Completo.py está en el mismo directorio
from AnzLex_Completo import AFN 

# Contenedor global que ahora guardará las INSTANCIAS REALES de los AFNs
afns_en_memoria = {}
contador_afn = 1

class InterfazCompilador:
    def __init__(self, root):
        self.root = root
        self.root.title("Analizador Léxico - Testbench Thompson")
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
        menu_thompson.add_command(label="Unión para analizador léxico", command=self.mostrar_vista_union_lexico)
        menu_thompson.add_command(label="Convertir AFN a AFD", command=self.mostrar_vista_convertir_afd)
        
        menubar.add_cascade(label="AFN's", menu=menu_thompson)
        self.root.config(menu=menubar)

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # ==========================================
    # VISTAS CON CONEXIÓN AL BACKEND
    # ==========================================

    def mostrar_vista_crear_basico(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="CREAR BÁSICO", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        
        tk.Label(self.main_frame, text="Simb 1 (ej. 'a')").grid(row=1, column=0, pady=10, sticky="e")
        entrada_simb1 = tk.Entry(self.main_frame, width=15)
        entrada_simb1.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="Simb 2 (opcional)").grid(row=2, column=0, pady=10, sticky="e")
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
                
            try:
                # --- LLAMADA AL BACKEND ---
                nuevo_afn = AFN().CrearBasico(s1, s2)
                afns_en_memoria[id_afn] = nuevo_afn
                
                detalles = f"AFN '{id_afn}' creado exitosamente.\nEstados: {len(nuevo_afn.EdosAFN)}\nAlfabeto: {sorted(list(nuevo_afn.Alfabeto))}"
                messagebox.showinfo("Éxito", detalles)
                
                entrada_simb1.delete(0, tk.END)
                entrada_simb2.delete(0, tk.END)
                entrada_id.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error del Backend", str(e))

        tk.Button(self.main_frame, text="CREAR", command=accion_crear, width=10).grid(row=4, column=0, columnspan=2, pady=20)


    def mostrar_vista_unir(self):
        self._vista_operacion_doble("UNIR AFN", "unir")

    def mostrar_vista_concatenar(self):
        self._vista_operacion_doble("CONCATENAR AFNs", "concatenar")

    def _vista_operacion_doble(self, titulo, operacion):
        self.limpiar_frame()
        tk.Label(self.main_frame, text=titulo, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        opciones_afn = list(afns_en_memoria.keys())

        tk.Label(self.main_frame, text="AFN 1").grid(row=1, column=0, pady=10, sticky="e")
        combo_afn1 = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=12)
        combo_afn1.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(self.main_frame, text="AFN 2").grid(row=2, column=0, pady=10, sticky="e")
        combo_afn2 = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=12)
        combo_afn2.grid(row=2, column=1, padx=10, pady=10)

        def accion_aplicar():
            id1 = combo_afn1.get()
            id2 = combo_afn2.get()
            
            if not id1 or not id2:
                messagebox.showerror("Error", "Seleccione ambos AFNs")
                return
            
            afn1 = afns_en_memoria[id1]
            afn2 = afns_en_memoria[id2]
            
            try:
                # --- LLAMADAS AL BACKEND ---
                if operacion == "unir":
                    afn_resultante = afn1.UnirAFN(afn2)
                elif operacion == "concatenar":
                    afn_resultante = afn1.Concatenar(afn2)
                
                # Para simplificar la memoria, sobrescribimos el AFN 1 con el resultado
                afns_en_memoria[id1] = afn_resultante
                
                messagebox.showinfo("Éxito", f"Operación exitosa.\nEstados totales: {len(afn_resultante.EdosAFN)}\nAlfabeto: {sorted(list(afn_resultante.Alfabeto))}")
            except Exception as e:
                messagebox.showerror("Error del Backend", str(e))

        tk.Button(self.main_frame, text="APLICAR", command=accion_aplicar, width=10).grid(row=4, column=0, columnspan=2, pady=20)


    def mostrar_vista_cerradura_pos(self):
        self._vista_operacion_simple("CERRADURA POSITIVA", "pos")

    def mostrar_vista_cerradura_kleen(self):
        self._vista_operacion_simple("CERRADURA DE KLEEN", "kleen")

    def mostrar_vista_opcional(self):
        self._vista_operacion_simple("OPERACIÓN OPCIONAL", "opc")

    def _vista_operacion_simple(self, titulo, operacion):
        self.limpiar_frame()
        tk.Label(self.main_frame, text=titulo, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 20), sticky="w")
        opciones_afn = list(afns_en_memoria.keys())

        tk.Label(self.main_frame, text="Seleccionar AFN").grid(row=1, column=0, pady=10, sticky="e")
        combo_afn = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=12)
        combo_afn.grid(row=1, column=1, padx=10, pady=10)

        def accion_aplicar():
            id_sel = combo_afn.get()
            if not id_sel:
                messagebox.showerror("Error", "Seleccione un AFN")
                return
            
            afn = afns_en_memoria[id_sel]
            
            try:
                # --- LLAMADAS AL BACKEND ---
                if operacion == "pos":
                    afn_resultante = afn.cerraduraPos()
                elif operacion == "kleen":
                    afn_resultante = afn.cerraduraKleen()
                elif operacion == "opc":
                    afn_resultante = afn.Opcional()
                
                afns_en_memoria[id_sel] = afn_resultante
                messagebox.showinfo("Éxito", f"Operación aplicada al AFN.\nNuevos estados: {len(afn_resultante.EdosAFN)}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(self.main_frame, text="APLICAR", command=accion_aplicar, width=15).grid(row=3, column=0, columnspan=2, pady=20)

    def mostrar_vista_convertir_afd(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="CONVERTIR AFN A AFD", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=4, pady=(0, 10), sticky="w")
        
        opciones_afn = list(afns_en_memoria.keys())
        
        # Campo 1: Seleccionar el AFN origen
        tk.Label(self.main_frame, text="AFN a convertir a AFD:").grid(row=1, column=0, pady=10, sticky="e")
        combo_afn = ttk.Combobox(self.main_frame, values=opciones_afn, state="readonly", width=15)
        combo_afn.grid(row=1, column=1, padx=10, pady=10)
        
        # Campo 2: Id del AFD resultante (Nuevo campo agregado según referencia)
        tk.Label(self.main_frame, text="Id del AFD:").grid(row=1, column=2, pady=10, sticky="e")
        entrada_id_afd = tk.Entry(self.main_frame, width=10)
        entrada_id_afd.grid(row=1, column=3, padx=10, pady=10)
        
        # Frame para la tabla de transiciones
        frame_tabla = tk.Frame(self.main_frame)
        frame_tabla.grid(row=3, column=0, columnspan=4, pady=10)

        def accion_convertir_y_guardar():
            # Limpiar tabla previa si existe
            for widget in frame_tabla.winfo_children():
                widget.destroy()
                
            id_sel = combo_afn.get()
            id_afd = entrada_id_afd.get()
            
            if not id_sel:
                messagebox.showerror("Error", "Selecciona un AFN a convertir.")
                return
            if not id_afd:
                messagebox.showerror("Error", "Ingresa un Id para el nuevo AFD.")
                return
                
            afn_obj = afns_en_memoria[id_sel]
            
            try:
                # --- 1. LÓGICA DE CONVERSIÓN ---
                afd_generado = afn_obj.Convertir_a_AFD()
                
                # --- 2. DIBUJAR LA TABLA ---
                alfabeto_lista = sorted(list(afd_generado.Alfabeto))
                columnas = ["Estado"] + alfabeto_lista + ["Token"]
                
                tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings", height=8)
                
                for col in columnas:
                    tabla.heading(col, text=col)
                    ancho = 60 if col != "Estado" else 80
                    tabla.column(col, width=ancho, anchor="center")
                    
                for edo in afd_generado.EdosAFD:
                    fila = [f"q{edo.IdAFD}"]
                    for sim in alfabeto_lista:
                        idx = ord(sim)
                        dest = edo.TransEdo[idx]
                        fila.append(f"q{dest}" if dest != -1 else "-")
                    
                    token = edo.TransEdo[256]
                    fila.append(str(token) if token != -1 else "-")
                    tabla.insert("", "end", values=fila)
                    
                tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar = ttk.Scrollbar(frame_tabla, orient=tk.VERTICAL, command=tabla.yview)
                tabla.configure(yscrollcommand=scrollbar.set)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # --- 3. ABRIR EL EXPLORADOR DE ARCHIVOS ---
                ruta_archivo = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
                    title="Guardar como archivo de texto"
                )
                
                if ruta_archivo:
                    # Aquí enviaremos la orden de escritura al backend en el próximo paso
                    # afd_generado.guardar_en_archivo(ruta_archivo, id_afd)
                    
                    messagebox.showinfo("Simulación de Guardado", f"El explorador funcionó.\nRuta seleccionada:\n{ruta_archivo}\n\nNota: Falta integrar el método de escritura en el backend.")
                else:
                    messagebox.showwarning("Cancelado", "La conversión se realizó en memoria, pero no se guardó el archivo.")
                    
            except Exception as e:
                messagebox.showerror("Error", str(e))

        # Botón actualizado
        tk.Button(self.main_frame, text="Convertir y guardar", command=accion_convertir_y_guardar, width=20).grid(row=2, column=0, columnspan=4, pady=10)    
    def mostrar_vista_union_lexico(self):
        self.limpiar_frame()
        
        tk.Label(self.main_frame, text="UNIÓN PARA ANALIZADOR LÉXICO", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10), sticky="w")
        tk.Label(self.main_frame, text="Selecciona los AFNs a Unir y asigna los tokens").grid(row=1, column=0, columnspan=3, sticky="w")
        
        # Texto rojo conciso
        texto_rojo = "Nota: Usa el TOKEN 20001 para omitir lexemas sin valor sintáctico (ej. espacios o saltos de línea)."
        tk.Label(self.main_frame, text=texto_rojo, fg="red", font=("Arial", 9, "italic")).grid(row=2, column=0, columnspan=3, sticky="w", pady=(0, 10))
        
        # Contenedor de la tabla
        frame_tabla = tk.Frame(self.main_frame, bd=1, relief="solid")
        frame_tabla.grid(row=3, column=0, columnspan=3, pady=10, sticky="w")
        
        # Cabeceras exactas
        tk.Label(frame_tabla, text="AFN", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=15, pady=5)
        tk.Label(frame_tabla, text="Selecciona AFN", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=15, pady=5)
        tk.Label(frame_tabla, text="Token", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=15, pady=5)
        
        self.variables_seleccion = {}
        self.variables_tokens = {}
        opciones_afn = list(afns_en_memoria.keys())
        
        # Rellenar la tabla dinámica
        for idx, afn_id in enumerate(opciones_afn):
            tk.Label(frame_tabla, text=afn_id).grid(row=idx+1, column=0, padx=15, pady=5)
            
            var_chk = tk.BooleanVar()
            tk.Checkbutton(frame_tabla, variable=var_chk).grid(row=idx+1, column=1, padx=15, pady=5)
            self.variables_seleccion[afn_id] = var_chk
            
            var_tok = tk.StringVar()
            tk.Entry(frame_tabla, textvariable=var_tok, width=12).grid(row=idx+1, column=2, padx=15, pady=5)
            self.variables_tokens[afn_id] = var_tok

        # Campo final de ID
        tk.Label(self.main_frame, text="ID del AFN resultante").grid(row=4, column=0, pady=15, sticky="e")
        entrada_id_res = tk.Entry(self.main_frame, width=20)
        entrada_id_res.grid(row=4, column=1, sticky="w")
        
        def accion_union_lexica():
            id_resultado = entrada_id_res.get()
            if not id_resultado:
                messagebox.showerror("Error", "Ingresa un ID para el AFN resultante.")
                return
                
            afns_a_unir = []
            
            for afn_id, var_chk in self.variables_seleccion.items():
                if var_chk.get():
                    token_str = self.variables_tokens[afn_id].get()
                    if not token_str.isdigit():
                        messagebox.showerror("Error", f"El Token para '{afn_id}' debe ser numérico.")
                        return
                    afns_a_unir.append((afn_id, int(token_str)))
                    
            if len(afns_a_unir) < 1:
                messagebox.showerror("Error", "Selecciona al menos 1 AFN.")
                return
                
            try:
                # Lógica del backend
                from AnzLex_Completo import AFN, Estado, Transicion, EPSILON
                
                afn_lexico = AFN()
                estado_inicial_global = Estado()
                
                for afn_id, token_val in afns_a_unir:
                    afn_obj = afns_en_memoria[afn_id]
                    
                    for edo in afn_obj.EdosAcept:
                        edo.Token = token_val
                        
                    estado_inicial_global.Transiciones.add(Transicion(EPSILON, afn_obj.EdoIni))
                    afn_lexico.EdosAFN.update(afn_obj.EdosAFN)
                    afn_lexico.EdosAcept.update(afn_obj.EdosAcept)
                    afn_lexico.Alfabeto.update(afn_obj.Alfabeto)
                    
                afn_lexico.EdoIni = estado_inicial_global
                afn_lexico.EdosAFN.add(estado_inicial_global)
                
                afns_en_memoria[id_resultado] = afn_lexico
                messagebox.showinfo("Éxito", f"Unión léxica completada.\nNuevo AFN: {id_resultado}")
                
            except Exception as e:
                messagebox.showerror("Error del Backend", str(e))
                
        tk.Button(self.main_frame, text="Aplicar Unión", command=accion_union_lexica, width=15).grid(row=5, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazCompilador(root)
    root.mainloop()