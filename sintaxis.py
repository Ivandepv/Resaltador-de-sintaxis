"""
    Jorge Ivan Coronado Villegas A01254785
    Daniel Antonio Lujan - A01254903
    Bruno Garxiola
"""
import re

def analizar_lexico(codigo, expresiones_regulares):
    tokens = []
    posicion = 0

    while posicion < len(codigo):
        match = None
        for categoria, expresion in expresiones_regulares.items():
            regex = re.compile(expresion)
            match = regex.match(codigo, posicion)
            if match:
                valor = match.group()
                if categoria == "funcion": 
                    # Extraer solo el nombre de la función (sin paréntesis)
                    nombre_funcion = valor.split("(")[0]
                    tokens.append(("funcion", nombre_funcion))  
                    posicion = match.end() - 1  # Ajustar la posición para no incluir el paréntesis en el siguiente token
                else:
                    tokens.append((categoria, valor))
                    posicion = match.end()
                break

        if not match:
            # Si no hay coincidencia, avanzar un carácter como texto normal
            tokens.append(("texto", codigo[posicion]))
            posicion += 1

    return tokens

def generar_html(tokens):
    html = """<html><head><meta charset="UTF-8"><style>
    .reservado { color: blue; }  
    .operador { color: red; }   
    .numero { color: green; }  
    .cadena { color: purple; }  
    .comentario { color: gray; } 
    .booleano { color: orange; } 
    .funcion { color: yellow; }
    .ciclo { color: pink; }
    .condicion { color: brown; }
    </style></head><body><pre>"""
    for categoria, token in tokens:
        html += f'<span class="{categoria}">{token}</span>'
    html += "</pre></body></html>"
    return html

# Expresiones regulares
expresiones_regulares = {}
with open("expresiones.txt", "r") as f:
    for linea in f:
        categoria, expresion = linea.split(":", 1)
        expresiones_regulares[categoria.strip()] = expresion.strip()

# Código fuente a analizar
codigo_fuente = ""

with open("codigo.txt", "r") as f:
    codigo_fuente = f.read()

tokens = analizar_lexico(codigo_fuente, expresiones_regulares)
html = generar_html(tokens)

# Guardar el resultado en un archivo HTML con estilos
if html:
    with open("resultado.html", "w") as f:
        f.write(html)
else:
    print("Error al generar el HTML.")
