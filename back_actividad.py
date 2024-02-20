"""Programa que abre un csv, recorre la celda con chunks, aplica cambios y genera combinaciones."""

#LIBRERIAS
import os
from itertools import combinations
import pandas as pd

#FACTORIAL DE UN NUMERO
def fact(n):
    if n < 2:
        return 1
    return n * fact(n - 1)

#FUNCION QUE BUSCA EL ARCHIVO CSV
def obtener_archivo():
    nombre = input("\nIngresa el nombre del archivo .csv a buscar: ")
    if not nombre:
        return None
    for root, _, files in os.walk("/"):
        if nombre + ".csv" in files:
            return os.path.join(root, f"{nombre}.csv")
    return None

#FUNCION QUE RECORRE EL ARREGLO Y OBTIENE TODOS LOS CHUNKS
def recorrer_arreglo(dataf, string_original, chunk, recorrido):
    lista_strings = []
    posiciones = set(dataf['posicion'].values)
    for i in range(0, len(string_original), recorrido):
        copia_string = string_original.copy()
        cambio = False
        #se obtienen todos los valores de col_String desde 'i' hasta 'i+chunk'
        chuns_evaluado = string_original[i:i+chunk]
        pos_evaluadas = list(range(i, i+chunk))
        #f-string permite intercambiar entre texto y varibles, usando {}
        #' '.join une tuplas o caracteres separados mas lo que este dentro de ' '
        print(f"Letras evaluadas: {' '.join(chuns_evaluado)}")
        print(f"\n\tPosiciones evaluadas: {pos_evaluadas}")
        for pos in pos_evaluadas:
            #si el numero de posicion esta en la conlumna de posicion del csv
            if pos in posiciones:
                cambio = True
                print(f"\n\t\tSe debe cambiar la posicion {pos}")
                #eq(pos) arroja True/False si la celda de la columa es igual a pos
                #idmax() devuelve la posicion del valor maximo, osea el primer True
                indice = dataf['posicion'].eq(pos).idxmax()
                #dataf.at solo devuelve el valor de una celda
                referencia_actual = dataf.at[indice, 'referencia']
                alteracion_nueva = dataf.at[indice, 'alteracion']
                print(f"\n\t\tEsa posicion esta indicada en la celda {indice} del csv")
                print(f"\n\t\tLa letra actual es {referencia_actual}")
                print(f"\n\t\tLa letra nueva  es {alteracion_nueva}")
                copia_string[pos] = alteracion_nueva.lower()
                #eliminamos la posicion para que no se vuelva a cambiar
                posiciones.remove(pos)
                print(f"\n\tEl string modificado es: {copia_string}")
        if cambio:
            #guarda el chunk evaluado en una lista
			#col_String es mutable y actualizara las anteriores, debemos guardar una copia con .copy()
            lista_strings.append(copia_string.copy())
        print("\n\n")
    print("\nSe han realizado todos los cambios necesarios\n\n")
    return lista_strings

#GUARDA LA LISTA DE STRIGNS MODIFICADOS EN UN NUEVO ARCHIVO CSV
def guardar_strings(strings_a_guardar):
    #une las letras de cada chunk
    strings_unidos = [''.join(strings) for strings in strings_a_guardar]
    #convierte la lista de chunks en un DataFrame
    df_strings = pd.DataFrame(strings_unidos, columns=['strings generados'])
    #guarda el DataFrame en un archivo CSV
    df_strings.to_csv('lista_de_strings.csv', index=False)
    print("\nSe han guardado los strings modificados en 'lista_de_strings.csv'\n\n")

def generar_combinaciones(strings_a_combinar):
    strings_combinados = []
    #generar todas las combinaciones posibles de 2 a n elementos
    for r in range(2, len(strings_a_combinar) + 1):
        #combinations() usa una lista y un iterador que es el numero de elementos que se tomen
        #esta funcion retorna todas las combinaciones de r elementos de strings_a_combinar
        for subset in combinations(strings_a_combinar, r):
            #llama a la funcion que hace la comparacion con una de las combinaciones generadas
            string_resultado = generar_combinacion(subset)
            strings_combinados.append(string_resultado)
    print("\nGenerando todas las combinaciones posibles\n\n")
    for i in strings_combinados:
        print(f"\n\tCombinacion: {i}")
    print("\nSe han hecho todas las combinaciones posibles\n\n")
    return strings_combinados

def generar_combinacion(subset):
    #se inicializa como el primer string que tenga, para solo modificar los otros
    string_combinado = list(subset[0])
    #cada iteracion tomara uno de los string que haya, a partir del segundo
    for i in range(1, len(subset)):
        #toma el string a comparar
        string_comparado = subset[i]
        #recorre cada letra del string
        for k in range(len(string_combinado)):
            #si el string comparado es diferente al original y al resultado actual
            if string_comparado[k] != col_string[k] and string_comparado[k] != string_combinado[k]:
                string_combinado[k] = string_comparado[k]
    return string_combinado

#GUARDA LA LISTA DE STRIGNS COMBINADOS EN UN NUEVO ARCHIVO CSV
def guardar_combinaciones(combinaciones_a_guardar):
    #une las letras de cada string
    combinaciones_unidas = [''.join(string) for string in combinaciones_a_guardar]
    #convierte la lista de strings en un DataFrame
    df_combinaciones = pd.DataFrame(combinaciones_unidas, columns=['Strings Combinados'])
    #guarda el DataFrame en un archivo CSV
    df_combinaciones.to_csv('ListaDeCombinaciones.csv', index=False)
    print(f"\nSe han guardado {len(combinaciones_unidas)} strings en ListaDeCombinaciones.csv\n")
    #Puedes calcular con formula el numero de combinaciones totales
    num_combinaciones = 0
    for i in range(2,8):
        num_combinaciones += fact(len(lista_de_strings))/(fact(len(lista_de_strings)-i)*fact(i))
    print(f"\nCalculandolo, se obtienen {num_combinaciones} combinaciones\n\n")

#UNIR PARES ESPECIFICOS DE STRINGS
def unir_pares(strings_a_elegir):
    print("\n----- Uniendo pares especificos de strings -----\n\n")
    while True:
        #pide el numero del primer string
        string1 = input("\nIndica el primer string que quieres unir (0:119): ")
        if int(string1) < 0 or int(string1) > len(strings_a_elegir):
            print("\nIndique un numero valido")
        else:
            #convierte la variable al string indicado
            string1 = strings_a_elegir[int(string1)]
            break
    while True:
        #pide el numero del segundo string
        string2 = input("\nIndica el segundo string que quieres unir (0:119): ")
        if int(string2) < 0 or int(string2) > len(strings_a_elegir) or string2 == string1:
            print("\nIndique un numero valido")
        else:
            #convierte la variable al string indicado
            string2 = strings_a_elegir[int(string2)]
            break
    #manda a llamar a la funcion que combina
    par_combinado = generar_combinacion([string1, string2])
    print(f"\nUnir el string:\n{string1}\ny el string:\n{string2}\nda:\n{par_combinado}")
    return 0

#UNIR UN RANGO DE STRINGS
def unir_rango(lista_combinaciones):
    print("\n----- Uniendo un rango de strings -----\n\n")
    while True:
        #pide el inicio del rango
        inicio = input("\nIndica el inicio del rango que quieres unir (0:119): ")
        if int(inicio) < 0 or int(inicio) >= len(lista_combinaciones):
            print("\nIndique un numero valido")
        else:
            inicio = int(inicio)
            break
    while True:
        #pide el fin del rango
        fin = input("\nIndica el fin del rango que quieres unir (0:119): ")
        if int(fin) <= inicio or int(fin) > len(lista_combinaciones):
            print("\nIndique un numero valido")
        else:
            fin = int(fin)
            break
    #crea una lista con los valores de listaCombinados desde inicio hasta fin
    rango = lista_combinaciones[inicio:fin+1]
    #manda a llamar a la funcion que combina todos los strings dentro del rango
    rango_resultado = generar_combinacion(rango)
    print("\nSe unieron los siguinetes strings: ")
    for i in rango:
        print(f"\n{i}")
    print(f"\nLa union de los strings desde el {inicio} hasta el {fin} es: \n{rango_resultado}")
    return 0

#LINEAS PRINCIPALES DEL ARCHIVO
ruta = obtener_archivo()
if ruta is None:
    print("No se encontro ese archivo")
else:
    df = pd.read_csv(ruta)
    col_string = list(df.loc[0, 'string_a_modificar'])
    lista_de_strings = recorrer_arreglo(df, col_string, 10, 5)
    guardar_strings(lista_de_strings)
    lista_combinados = generar_combinaciones(lista_de_strings)
    guardar_combinaciones(lista_combinados)
    unir_pares(lista_combinados)
    unir_rango(lista_combinados)
