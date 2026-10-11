# ==============================================================
#  AFNLexProba.py  —  Ejemplo 3 COMPLETO y CORREGIDO
# ==============================================================
from collections import deque

EPSILON = 'ε'

# --------------------------------------------------------------
#  Clases base: Estado y Transicion
# --------------------------------------------------------------
class Estado:
    ContEdos = 0

    def __init__(self):
        self.IdEdo = Estado.ContEdos
        Estado.ContEdos += 1
        self.EdoAcept = False
        self.Token = -1
        self.Transiciones = set()


class Transicion:
    def __init__(self, *args):
        if len(args) == 2:
            self.SimbInf = args[0]
            self.SimbSup = args[0]
            self.EdoDest = args[1]
        elif len(args) == 3:
            self.SimbInf = args[0]
            self.SimbSup = args[1]
            self.EdoDest = args[2]


# --------------------------------------------------------------
#  Clases auxiliares del AFD
# --------------------------------------------------------------
class EdoAFD:
    def __init__(self):
        self.TransEdo = [-1] * 257
        self.IdAFD = 0
        self.EdoAcept = False
        self.Transiciones = dict()

    def PonerTransicion(self, sim, edo_dest):
        self.Transiciones[sim] = edo_dest


class AFD:
    def __init__(self):
        self.Alfabeto = set()
        self.EdosAFD = []
        self.EdoIni = None
        self.EdosAcept = set()
        self.NumEdos = 0


class Sj:
    def __init__(self):
        self.Id = -1
        self.Edos = set()


# --------------------------------------------------------------
#  Clase AFN (con conversión a AFD)
# --------------------------------------------------------------
class AFN:
    def __init__(self):
        self.Alfabeto = set()
        self.EdoIni = None
        self.EdosAcept = set()
        self.EdosAFN = set()

    def CrearBasico(self, simb1, simb2=None):
        f = AFN()
        e1 = Estado()
        e2 = Estado()

        if simb2 is None:
            t = Transicion(simb1, e2)
            f.Alfabeto.add(simb1)
        else:
            t = Transicion(simb1, simb2, e2)
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

        self.EdosAFN.update(f2.EdosAFN)
        self.EdosAFN.add(e1)
        self.EdosAFN.add(e2)

        self.EdoIni = e1
        self.EdosAcept.clear()
        self.EdosAcept.add(e2)
        self.Alfabeto.update(f2.Alfabeto)
        return self

    def Concatenar(self, f2):
        for e in self.EdosAcept:
            for t in f2.EdoIni.Transiciones:
                e.Transiciones.add(t)
            e.EdoAcept = False

        self.EdosAFN.update(f2.EdosAFN)
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
        self.cerraduraPos()
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

    # ---------------- Conversión AFN → AFD ----------------
    def CerraduraEpsilon(self, c_edos):
        R = set()
        S = []
        if isinstance(c_edos, Estado):
            S.append(c_edos)
        else:
            for e in c_edos:
                S.append(e)

        while len(S) != 0:
            EdoAux = S.pop()
            R.add(EdoAux)
            for t in EdoAux.Transiciones:
                if t.SimbInf == EPSILON and t.SimbSup == EPSILON:
                    if t.EdoDest not in R and t.EdoDest not in S:
                        S.append(t.EdoDest)
        return R

    def Mover(self, c_edos, simb):
        R = set()
        if isinstance(c_edos, Estado):
            edos = {c_edos}
        else:
            edos = c_edos

        for e in edos:
            for t in e.Transiciones:
                if t.SimbInf != EPSILON and t.SimbInf <= simb <= t.SimbSup:
                    R.add(t.EdoDest)
        return R

    def IrA(self, C, S_simb):
        return self.CerraduraEpsilon(self.Mover(C, S_simb))

    def Convertir_a_AFD(self):
        NumConjSj = 0
        ConjSjSinAnalizar = deque()
        ConjTodosSj = []
        QEdosAFD = deque()

        def BuscarSj(conj_sj, sj_temp):
            for sj in conj_sj:
                if sj.Edos == sj_temp.Edos:
                    return sj.Id
            return -1

        SjAux = Sj()
        SjAux.Edos = self.CerraduraEpsilon(self.EdoIni)
        SjAux.Id = NumConjSj
        NumConjSj += 1

        ConjSjSinAnalizar.append(SjAux)
        ConjTodosSj.append(SjAux)

        while len(ConjSjSinAnalizar) != 0:
            SjAux = ConjSjSinAnalizar.popleft()
            EdojAFD = EdoAFD()
            EdojAFD.IdAFD = SjAux.Id

            # Iteración determinista para que los IDs sean reproducibles
            for sim in sorted(self.Alfabeto):
                SjTemp = Sj()
                SjTemp.Edos = self.IrA(SjAux.Edos, sim)

                if len(SjTemp.Edos) == 0:
                    continue

                IdEdo = BuscarSj(ConjTodosSj, SjTemp)

                if IdEdo == -1:
                    SjTemp.Id = NumConjSj
                    NumConjSj += 1
                    ConjTodosSj.append(SjTemp)
                    ConjSjSinAnalizar.append(SjTemp)
                    EdojAFD.TransEdo[ord(sim)] = SjTemp.Id
                    EdojAFD.PonerTransicion(sim, SjTemp.Id)
                else:
                    EdojAFD.TransEdo[ord(sim)] = IdEdo
                    EdojAFD.PonerTransicion(sim, IdEdo)

            QEdosAFD.append(EdojAFD)

        ConvAFD = AFD()
        ConvAFD.NumEdos = NumConjSj
        ConvAFD.EdosAFD = [EdoAFD() for _ in range(NumConjSj)]
        ConvAFD.Alfabeto.update(self.Alfabeto)

        for i in range(NumConjSj):
            ConvAFD.EdosAFD[i].IdAFD = i

        while len(QEdosAFD) != 0:
            EdoAFDTemp = QEdosAFD.popleft()

            for j in range(257):
                ConvAFD.EdosAFD[EdoAFDTemp.IdAFD].TransEdo[j] = EdoAFDTemp.TransEdo[j]

            edos_sj_actual = set()
            for sj in ConjTodosSj:
                if sj.Id == EdoAFDTemp.IdAFD:
                    edos_sj_actual = sj.Edos
                    break

            EdoAceptAFD = list(self.EdosAcept.intersection(edos_sj_actual))

            if len(EdoAceptAFD) == 0:
                continue

            ConvAFD.EdosAFD[EdoAFDTemp.IdAFD].EdoAcept = True
            ConvAFD.EdosAFD[EdoAFDTemp.IdAFD].TransEdo[256] = EdoAceptAFD[0].Token

            if len(EdoAceptAFD) >= 2:
                print(f"Advertencia: ambigüedad en AFD estado {EdoAFDTemp.IdAFD}, "
                      f"tokens candidatos: {[e.Token for e in EdoAceptAFD]}")

        return ConvAFD


# --------------------------------------------------------------
#  Analizador léxico
# --------------------------------------------------------------
class AnalizadorLexico:
    def __init__(self, afd_lexico=None, cadena_sigma=""):
        self.yytext = ""
        self.AFD_Lexico = afd_lexico
        self.sigma = cadena_sigma
        self.PasoPorEdoAcept = False
        self.IndCaracActual = 0
        self.IndIniLexema = 0
        self.IndFinLexema = -1

    def AnaliLexic(self, cadena_sigma):
        self.sigma = cadena_sigma
        self.PasoPorEdoAcept = False
        self.IndCaracActual = 0
        self.IndIniLexema = 0
        self.IndFinLexema = -1

    def yylex(self):
        self.PasoPorEdoAcept = False
        self.IndIniLexema = self.IndCaracActual
        EdoActual = 0
        token = -1

        if self.IndCaracActual >= len(self.sigma):
            return 0

        while self.IndCaracActual < len(self.sigma):
            caracter = self.sigma[self.IndCaracActual]
            idx = ord(caracter)

            if idx >= 257:          # protección contra caracteres fuera de rango
                break

            EdoActual = self.AFD_Lexico.EdosAFD[EdoActual].TransEdo[idx]

            if EdoActual != -1:
                if self.AFD_Lexico.EdosAFD[EdoActual].TransEdo[256] != -1:
                    self.IndFinLexema = self.IndCaracActual
                    self.PasoPorEdoAcept = True
                    token = self.AFD_Lexico.EdosAFD[EdoActual].TransEdo[256]

                self.IndCaracActual += 1
                continue
            else:
                break

        if self.PasoPorEdoAcept:
            self.yytext = self.sigma[self.IndIniLexema : self.IndFinLexema + 1]
            self.IndCaracActual = self.IndFinLexema + 1
            return token
        else:
            self.yytext = self.sigma[self.IndIniLexema : self.IndIniLexema + 1]
            self.IndCaracActual = self.IndIniLexema + 1
            return -1


# ==============================================================
#  EJEMPLO 3 — Analizador léxico completo
# ==============================================================

# Reinicio para reproducibilidad
Estado.ContEdos = 0

# ---- 1. Patrones léxicos ----
afn_letras = AFN().CrearBasico('a', 'z').cerraduraPos()
for edo in afn_letras.EdosAcept:
    edo.Token = 10

afn_numeros = AFN().CrearBasico('0', '9').cerraduraPos()
for edo in afn_numeros.EdosAcept:
    edo.Token = 20

# ---- 2. Unión léxica (mega-AFN con nuevo estado inicial ε) ----
afn_lexico = AFN()
estado_inicial_global = Estado()

estado_inicial_global.Transiciones.add(Transicion(EPSILON, afn_letras.EdoIni))
estado_inicial_global.Transiciones.add(Transicion(EPSILON, afn_numeros.EdoIni))

afn_lexico.EdoIni = estado_inicial_global
afn_lexico.EdosAFN.add(estado_inicial_global)
afn_lexico.EdosAFN.update(afn_letras.EdosAFN)
afn_lexico.EdosAFN.update(afn_numeros.EdosAFN)
afn_lexico.EdosAcept.update(afn_letras.EdosAcept)
afn_lexico.EdosAcept.update(afn_numeros.EdosAcept)
afn_lexico.Alfabeto.update(afn_letras.Alfabeto)
afn_lexico.Alfabeto.update(afn_numeros.Alfabeto)

# ---- 3. Conversión a AFD ----
afd_final = afn_lexico.Convertir_a_AFD()

if afd_final is None:
    raise RuntimeError("Convertir_a_AFD() devolvió None")

print(f"=== AFD construido: {afd_final.NumEdos} estados ===")
print()

# ---- 4. Análisis léxico sobre varias cadenas ----
TOKEN_NOMBRES = {10: "IDENTIFICADOR", 20: "NUMERO"}


def analizar(cadena):
    lexer = AnalizadorLexico(afd_final, cadena)
    print(f"Analizando: '{cadena}'")
    print("-" * 55)

    token = lexer.yylex()
    while token != 0:
        if token == -1:
            print(f"  [ERROR] Carácter inválido: '{lexer.yytext}'")
        else:
            nombre = TOKEN_NOMBRES.get(token, f"DESCONOCIDO({token})")
            print(f"  [TOKEN {token:>2}] {nombre:<13}: '{lexer.yytext}'")
        token = lexer.yylex()

    print("  [EOF]")
    print()


# ---- 5. Casos de prueba ----
analizar("hola123mundo")
analizar("abc")
analizar("123")
analizar("a1b2c3")
analizar("123abc456")
analizar("hola@mundo")
analizar("@abc")
analizar("abc@")
analizar("")


#Ej. 1: Imprimimos un afn de prueba para verficar el funcionamiento.
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



# ----- Ej2: Prueba de la clase AFD y convesiones. -----
if __name__ == "__main__":
    # ---------------------------------------------------------------
    # Ejemplo: construir AFN para  a (b|c)*
    # ---------------------------------------------------------------
    print("=== Construcción del AFN ===")

    # AFN para 'a'
    afn_a = AFN().CrearBasico('a')
    print(f"AFN 'a'  -> Estados: {len(afn_a.EdosAFN)}, Alfabeto: {afn_a.Alfabeto}")

    # AFN para 'b'
    afn_b = AFN().CrearBasico('b')

    # AFN para 'c'
    afn_c = AFN().CrearBasico('c')

    # Unión: (b|c)
    afn_bc = afn_b.UnirAFN(afn_c)
    print(f"AFN 'b|c' -> Estados: {len(afn_bc.EdosAFN)}, Alfabeto: {afn_bc.Alfabeto}")

    # Cerradura de Kleene: (b|c)*
    afn_bc_estrella = afn_bc.cerraduraKleen()
    print(f"AFN '(b|c)*' -> Estados: {len(afn_bc_estrella.EdosAFN)}, Alfabeto: {afn_bc_estrella.Alfabeto}")

    # Concatenación: a(b|c)*
    afn_final = afn_a.Concatenar(afn_bc_estrella)
    print(f"AFN final 'a(b|c)*' -> Estados: {len(afn_final.EdosAFN)}, Alfabeto: {afn_final.Alfabeto}")

    # ---------------------------------------------------------------
    # Marcar token de aceptación (para que se propague al AFD)
    # ---------------------------------------------------------------
    for edo in afn_final.EdosAcept:
        edo.Token = 42   # token arbitrario de ejemplo

    # ---------------------------------------------------------------
    # Conversión AFN -> AFD
    # ---------------------------------------------------------------
    print("\n=== Conversión AFN -> AFD ===")
    afd = afn_final.Convertir_a_AFD()

    print(f"AFD -> Número de estados: {afd.NumEdos}")
    print(f"AFD -> Alfabeto: {sorted(afd.Alfabeto)}")

    print("\n=== Tabla de transiciones del AFD ===")
    for edo in afd.EdosAFD:
        print(f"\nEstado AFD {edo.IdAFD}  (Aceptación: {edo.EdoAcept})")
        if edo.EdoAcept:
            print(f"  Token: {edo.TransEdo[256]}")
        for sim, dest in sorted(edo.Transiciones.items()):
            print(f"  --{sim}--> {dest}")

    # ---------------------------------------------------------------
    # Simulación manual de cadenas sobre el AFD
    # ---------------------------------------------------------------
    def simular(afd, cadena):
        #Recorre el AFD con la cadena. Devuelve (aceptada, token).
        edo_actual = afd.EdosAFD[0]  # El estado inicial es el IdAFD 0
        for c in cadena:
            idx = ord(c)
            if idx >= len(edo_actual.TransEdo):
                return False, -1
            sig = edo_actual.TransEdo[idx]
            if sig == -1:
                return False, -1
            edo_actual = afd.EdosAFD[sig]
        if edo_actual.EdoAcept:
            return True, edo_actual.TransEdo[256]
        return False, -1

    print("\n=== Simulación de cadenas ===")
    pruebas = ["a", "ab", "ac", "abc", "abcbcc", "b", "abb", ""]
    for cadena in pruebas:
        aceptada, token = simular(afd, cadena)
        etiqueta = f"'{cadena}'" if cadena else "(cadena vacía)"
        print(f"  {etiqueta:15} -> Aceptada: {aceptada}   Token: {token}")
