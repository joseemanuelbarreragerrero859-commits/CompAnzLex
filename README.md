# Generador y Analizador Léxico (AFN → AFD)

Herramienta interactiva con interfaz gráfica desarrollada en Python utilizando `tkinter`, destinada a la asignatura de **Compiladores**. Permite la construcción, manipulación y visualización de Autómatas Finitos No Deterministas (AFN) mediante la construcción de Thompson, la agrupación de patrones léxicos con asignación de tokens, la conversión determinista a AFD mediante el algoritmo de subconjuntos y la persistencia de datos en archivos planos.


## Características Principales

- **Construcción de AFNs Básicos:** Definición de caracteres individuales y rangos de la tabla ASCII.  
- **Operaciones de Thompson:**  
  - Unión de AFNs  
  - Concatenación de AFNs  
  - Cerradura Positiva ($+$)  
  - Cerradura de Kleene ($*$)  
  - Operación Opcional ($?$)  
- **Unión para Analizador Léxico:** Agrupación de múltiples AFNs con asignación de tokens numéricos, incluyendo soporte para el Token 20001 para ignorar caracteres de espacio y saltos de línea.  
- **Conversión a AFD:** Implementación del algoritmo de construcción de subconjuntos ($\text{Cerradura}-\varepsilon$ e $\text{IrA}$), con renderizado dinámico en tabla de transiciones.  
- **Persistencia:** Exportación de la matriz de transiciones del AFD en formato `.txt`.  
- **Visualización Gráfica:** Generación automática y visualización de diagramas de estados en formato PNG mediante Graphviz.  

## Requisitos del Sistema e Instalación

Se requiere **Python 3.8+** y la instalación del motor gráfico **Graphviz** en el sistema operativo.

### Instalación del Motor Graphviz

El ejecutable de Graphviz debe estar registrado en las variables de entorno (`PATH`) del sistema operativo.

**Windows:**
1. Descargar el instalador de 64 bits desde la página oficial de Graphviz.  
2. Ejecutar el archivo `.exe`.  
3. Durante la instalación, marcar la opción:  
   - **`Add Graphviz to the system PATH for all users`** (o *for current user*).  
4. Reiniciar el editor de código o la terminal.  
5. Verificar la instalación con:  
   ```powershell
   dot -V
   ```

**Linux (Ubuntu / Debian):**
```bash
sudo apt update
sudo apt install graphviz
```

**macOS:**
```bash
brew install graphviz
```



### Instalación de la Librería de Python

```bash
python -m pip install graphviz
```

## Estructura del Código

- **`AnzLex_Completo.py` (Backend):**  
  - `Estado` y `Transicion`: Representación nodal del grafo.  
  - `AFN`: Construcciones de Thompson, algoritmo de subconjuntos, $\text{Cerradura}-\varepsilon$, integración con Graphviz.  
  - `AFD` y `EdoAFD`: Matriz determinista y exportación a archivo `.txt`.  
  - `AnalizadorLexico`: Motor de simulación y coincidencia de cadenas (`yylex`).  

- **`viGeneral.py` (Frontend):**  
  - Interfaz Tkinter con menú navegable.  
  - Renderizado de la matriz de transiciones con `ttk.Treeview`.  
  - Integración con el explorador de archivos `filedialog`.  



## Guía de Uso

1. **Ejecutar la aplicación:**
   ```bash
   python viGeneral.py
   ```
2. **Crear AFN Básico:**  
   - Ingresar el carácter inicial en `Simb 1`.  
   - Para rangos (ej. `a` a `z`), especificar el límite superior en `Simb 2`.  
   - Para secuencias de varios caracteres (ej. `/*`), crear los básicos individualmente y unirlos con **Concatenar**.  
3. **Aplicar Thompson:**  
   - Utilizar el menú desplegable **AFN's** para realizar operaciones simples o dobles.  
4. **Unión Léxica:**  
   - Asignar tokens numéricos a cada patrón y generar el AFN resultante.  
5. **Convertir y Guardar AFD:**  
   - Generar la tabla determinista y utilizar el botón **Guardar en .txt** para exportar la matriz.  
6. **Visualización:**  
   - Seleccionar **Ver AFN** para generar el diagrama PNG del autómata seleccionado.  
