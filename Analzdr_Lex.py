EPSILON = 'ε'  # Constante global para evitar errores tipográficos

class Estado:
    ContEdos = 0  # Atributo de clase (estático)
    
    def __init__(self):
        self.IdEdo = Estado.ContEdos
        Estado.ContEdos += 1
        self.EdoAcept = False
        self.Transiciones = set()

class Transicion:
    # Usamos argumentos variables (*args) para simular los diferentes constructores
    def __init__(self, *args):
        if len(args) == 2:  # Constructor para un solo símbolo (simb, edo_dest)
            self.SimbInf = args[0]
            self.SimbSup = args[0]
            self.EdoDest = args[1]
        elif len(args) == 3:  # Constructor para un rango (simb1, simb2, edo_dest)
            self.SimbInf = args[0]
            self.SimbSup = args[1]
            self.EdoDest = args[2]

class AFN:
    def __init__(self):
        self.Alfabeto = set()
        self.EdoIni = None
        self.EdosAcept = set()
        self.EdosAFN = set()

    # Se unifican los dos CrearBasico en uno solo usando un parámetro opcional
    def CrearBasico(self, simb1, simb2=None):
        f = AFN()
        e1 = Estado()
        e2 = Estado()
        
        if simb2 is None:
            # Caso para un solo símbolo
            t = Transicion(simb1, e2)
            f.Alfabeto.add(simb1)
        else:
            # Caso para un rango de símbolos
            t = Transicion(simb1, simb2, e2)
            # Agregamos todo el rango al alfabeto usando su valor ASCII (ord/chr)
            for val in range(ord(simb1), ord(simb2) + 1):
                f.Alfabeto.add(chr(val))

        e1.Transiciones.add(t)
        e2.EdoAcept = True
        
        f.EdoIni = e1
        f.EdosAcept.add(e2)
        f.EdosAFN.add(e1)
        f.EdosAFN.add(e2)

        return f

    def UnirAFN(self, f2):
        e1 = Estado()
        e2 = Estado()
        
        e1.Transiciones.add(Transicion(EPSILON, self.EdoIni))
        e1.Transiciones.add(Transicion(EPSILON, f2.EdoIni))
        
        for edo in self.EdosAcept:
            edo.Transiciones.add(Transicion(EPSILON, e2))
            edo.EdoAcept = False
            
        for edo in f2.EdosAcept:
            edo.Transiciones.add(Transicion(EPSILON, e2))
            edo.EdoAcept = False
            
        e2.EdoAcept = True
        
        # En Python, update() modifica el set actual agregando los elementos
        self.EdosAFN.update(f2.EdosAFN)
        self.EdosAFN.add(e1)
        self.EdosAFN.add(e2)
        
        # Faltaba actualizar atributos del propio AFN tras la unión
        self.EdoIni = e1
        self.EdosAcept.clear()
        self.EdosAcept.add(e2)
        self.Alfabeto.update(f2.Alfabeto)
        
        return self

    def Concatenar(self, f2):
        for e in self.EdosAcept:
            # Corrección: iterar sobre las transiciones del estado, no sobre el estado en sí
            for t in f2.EdoIni.Transiciones:
                e.Transiciones.add(t)
            e.EdoAcept = False
            
        self.EdosAFN.update(f2.EdosAFN)
        # Verificamos que f2.EdoIni exista en el set antes de eliminarlo para evitar errores
        if f2.EdoIni in self.EdosAFN:
            self.EdosAFN.remove(f2.EdoIni)
            
        self.EdosAcept.clear()
        self.EdosAcept.update(f2.EdosAcept)
        self.Alfabeto.update(f2.Alfabeto)

        return self

    def cerraduraPos(self): 
        e1 = Estado()
        e2 = Estado()
        
        e2.EdoAcept = True
        e1.Transiciones.add(Transicion(EPSILON, self.EdoIni))
        
        for e in self.EdosAcept:
            e.Transiciones.add(Transicion(EPSILON, e2))
            e.Transiciones.add(Transicion(EPSILON, self.EdoIni))
            e.EdoAcept = False
            
        self.EdosAFN.add(e1)
        self.EdosAFN.add(e2)
        self.EdoIni = e1
        self.EdosAcept.clear()
        self.EdosAcept.add(e2)
        
        return self

    def cerraduraKleen(self):
        # La cerradura de Kleene se apoya en la Positiva
        self.cerraduraPos()
        
        # Como cerraduraPos ya dejó un único estado de aceptación (e2), 
        # solo falta puentear el nuevo inicio con el nuevo final.
        for e in self.EdosAcept:
            self.EdoIni.Transiciones.add(Transicion(EPSILON, e))
            
        return self

    def Opcional(self): 
        e1 = Estado()
        e2 = Estado()
        
        e2.EdoAcept = True
        e1.Transiciones.add(Transicion(EPSILON, self.EdoIni))
        
        for e in self.EdosAcept:
            e.Transiciones.add(Transicion(EPSILON, e2))
            e.EdoAcept = False
            
        e1.Transiciones.add(Transicion(EPSILON, e2))
        
        self.EdosAFN.add(e1)
        self.EdosAFN.add(e2)
        self.EdoIni = e1
        self.EdosAcept.clear()
        self.EdosAcept.add(e2)
        
        return self


def imprimir_afn(afn, nombre):
    print(f"\n================ {nombre} ================")
    print(f"Estado Inicial: q{afn.EdoIni.IdEdo}")
    print(f"Alfabeto: {sorted(list(afn.Alfabeto))}")
    
    estados_aceptacion = [f"q{e.IdEdo}" for e in afn.EdosAcept]
    print(f"Estados de Aceptación: {estados_aceptacion}")
    
    print("\nTransiciones:")
    # Ordenamos los estados por ID para imprimir de forma clara
    for estado in sorted(afn.EdosAFN, key=lambda e: e.IdEdo):
        aceptacion_tag = " (ACEPTACIÓN)" if estado.EdoAcept else ""
        print(f"  Estado q{estado.IdEdo}{aceptacion_tag}:")
        if not estado.Transiciones:
            print("    (Sin transiciones)")
        for t in estado.Transiciones:
            if t.SimbInf == t.SimbSup:
                simbolo = t.SimbInf
            else:
                simbolo = f"[{t.SimbInf}-{t.SimbSup}]"
            print(f"    --({simbolo})--> q{t.EdoDest.IdEdo}")

# --- PRUEBA DE USO ---

# 1. Crear AFN básico para el carácter 'a'
afn_a = AFN().CrearBasico('a')

# 2. Crear AFN básico para el rango de dígitos '0' a '2'
afn_num = AFN().CrearBasico('0', '2')

# 3. Aplicar unión: ('a' | ['0'-'2'])
afn_union = afn_a.UnirAFN(afn_num)

# 4. Aplicar Cerradura de Kleene: ('a' | ['0'-'2'])*
afn_final = afn_union.cerraduraKleen()

# Imprimir el AFN resultante
imprimir_afn(afn_final, "AFN Final: ('a' | ['0'-'2'])*")
