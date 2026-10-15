from collections import deque
EPSILON = 'EPSILON'

#Clases base: Estado y Transicion
class Estado:
    ContEdos = 0

    def __init__(self):
        self.IdEdo = Estado.ContEdos
        Estado.ContEdos += 1
        self.EdoAcept = False
        self.Token = -1
        self.Transiciones = set()

def reiniciar_contador_estados():
    """Reinicia el contador estático de estados a 0."""
    Estado.ContEdos = 0


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


#  Clases auxiliares del AFD
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
        
    def guardarArchivo(self, ruta_archivo, id_afd=None):
        """
        Serializa la tabla de transiciones del AFD en un archivo de texto plano.
        """
        try:
            with open(ruta_archivo, 'w', encoding='utf-8') as f:
                f.write(f"ID_AFD:{id_afd if id_afd else 'Sin_ID'}\n")
                f.write(f"NUM_EDOS:{self.NumEdos}\n")
                
                alfabeto_ordenado = sorted(list(self.Alfabeto))
                f.write(f"ALFABETO:{','.join(alfabeto_ordenado)}\n")
                f.write("TRANSICIONES\n")
                
                for edo in self.EdosAFD:
                    fila = [str(edo.IdAFD)]
                    for sim in alfabeto_ordenado:
                        idx = ord(sim)
                        dest = edo.TransEdo[idx]
                        fila.append(str(dest))
                    
                    token = edo.TransEdo[256]
                    fila.append(str(token))
                    f.write('\t'.join(fila) + '\n')
                    
            print(f"El AFD se ha guardado correctamente en: {ruta_archivo}")
            return True
            
        except Exception as e:
            print(f"Error al guardar el AFD en el archivo: {e}")
            raise Exception(f"No se pudo guardar el archivo: {e}")


class Sj:
    def __init__(self):
        self.Id = -1
        self.Edos = set()


#Clase AFN (incluye conversión a AFD)

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

    # Conversión AFN → AFD
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
    
    def generar_diagrama(self, nombre_archivo="diagrama_afn"):
        """
        Recorre el AFN actual y genera su diagrama de estados utilizando Graphviz.
        Genera un archivo PNG y lo abre automáticamente en el visor del sistema.
        """
        try:
            from graphviz import Digraph
            
            dot = Digraph(name=nombre_archivo, format="png")
            dot.attr(rankdir='LR')
            
            dot.node('start', shape='point')
            if self.EdoIni:
                dot.edge('start', str(self.EdoIni.IdEdo))
                
            for edo in self.EdosAFN:
                forma = 'doublecircle' if edo in self.EdosAcept else 'circle'
                dot.node(str(edo.IdEdo), label=f"q{edo.IdEdo}", shape=forma)
                
                for t in edo.Transiciones:
                    if t.SimbInf == t.SimbSup:
                        etiqueta = "EPSILON" if t.SimbInf == EPSILON else str(t.SimbInf)
                    else:
                        etiqueta = f"[{t.SimbInf}-{t.SimbSup}]"
                        
                    dot.edge(str(edo.IdEdo), str(t.EdoDest.IdEdo), label=etiqueta)
                    
            dot.render(nombre_archivo, view=True, cleanup=True)
            return True
            
        except ImportError:
            raise Exception("El módulo 'graphviz' no está instalado en Python.")
        except Exception as e:
            raise Exception(f"Error al generar el diagrama: {e}")


# analizador léxico
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

            if idx >= 257:
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
#  PRUEBAS INDEPENDIENTES
# ==============================================================
if __name__ == "__main__":
    Estado.ContEdos = 0

    afn_letras = AFN().CrearBasico('a', 'z').cerraduraPos()
    for edo in afn_letras.EdosAcept:
        edo.Token = 10

    afn_numeros = AFN().CrearBasico('0', '9').cerraduraPos()
    for edo in afn_numeros.EdosAcept:
        edo.Token = 20

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

    afd_final = afn_lexico.Convertir_a_AFD()
    print(f"=== AFD construido: {afd_final.NumEdos} estados ===")