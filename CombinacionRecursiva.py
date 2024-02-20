#LIBRERIAS
from itertools import combinations
import pandas as pd
import os

#FUNCION QUE BUSCA EL ARCHIVO CSV
def obtenerArchivo():
    nombre = input("\nIngresa el nombre del archivo .csv a buscar: ")
    if not nombre:
        return None
    for root, dirs, files in os.walk("/"):
        if nombre + ".csv" in files:
            return os.path.join(root, f"{nombre}.csv")
    return None
    
#FUNCION QUE RECORRE EL ARREGLO Y OBTIENE TODOS LOS CHUNKS
def recorrerArreglo(df, colString, chunk, recorrido):
    listaDeChunks = []
    posiciones = set(df['posicion'].values)
    for i in range(0, len(colString), recorrido):
        #se obtienen todos los valores de colString desde 'i' hasta 'i+chunk'
        chunkEvaluado = colString[i:i+chunk]
        posEvaluadas = list(range(i, i+chunk))
        #f-string permite intercambiar entre texto y varibles, usando {}
        #' '.join une tuplas o caracteres separados mas lo que este dentro de ' '
        print(f"----- Letras evaluadas: {' '.join(chunkEvaluado)} -----")
        print(f"\n      Posiciones evaluadas: {posEvaluadas}")
        for pos in posEvaluadas:
            #si el numero de posicion esta en la conlumna de posicion del csv
            if pos in posiciones:
                print(f"\n\t - Se debe cambiar la posicion {pos}")
               	#de la columna posicion, eq(pos) arroja True/False si la celda de la columa es igual a pos
                #idmax() devuelve la posicion del valor maximo, en este caso el primer true que encuentre
                indice = df['posicion'].eq(pos).idxmax()
                #df.at solo devuelve el valor de una celda
                referencia_actual = df.at[indice, 'referencia']
                alteracion_nueva = df.at[indice, 'alteracion']
                print(f"\n\t\tEsa posicion esta indicada en la celda {indice} del csv")
                print(f"\n\t\tLa letra actual es {referencia_actual}")
                print(f"\n\t\tLa letra nueva  es {alteracion_nueva}")
                copiaString = colString.copy()
                copiaString[pos] = alteracion_nueva.lower()
                #eliminamos la posicion para que no se vuelva a cambiar
                posiciones.remove(pos)
				#guarda el chunk evaluado en una lista
				#como colString es mutable y actualizara a las listas que se guardaron antes, debemos guardar una copia de la lista con .copy()
                listaDeChunks.append(copiaString.copy())
        print("\n\n")
    return listaDeChunks

#GUARDA LA LISTA DE STRIGNS MODIFICADOS EN UN NUEVO ARCHIVO CSV
def guardarChunks(listaDeChunks):
    #une las letras de cada chunk
    ChunksUnidos = [''.join(chunk) for chunk in listaDeChunks]
    #convierte la lista de chunks en un DataFrame
    df = pd.DataFrame(ChunksUnidos, columns=['Chunks generados'])
    #guarda el DataFrame en un archivo CSV
    df.to_csv('ListaDeChunks.csv', index=False)    

def generarCombinaciones(listaDeChunks):
    stringsCombinados = []
    #generar todas las combinaciones posibles de 2 a n elementos
    for r in range(2, len(listaDeChunks) + 1):
        #combinations() toma la lista de chunks y al iterable r que se convierte en el numero de elementos que se seleccionaran a la vez
        #esta funcion retorna todas las combinaciones de r elementos de listaDeChunks
        for subset in combinations(listaDeChunks, r):
            #llama a la funcion que hace la comparacion con una de las combinaciones generadas
            stringResultado = generarCombinacion(subset)
            stringsCombinados.append(stringResultado)
    return stringsCombinados

def generarCombinacion(subset):
    #se inicializa como el primer string que tenga subset, para solo modificar las partes necesarias
    stringResultado = list(subset[0])
    #cada iteracion del for tomara uno de los string que haya en el subset, a partir del segundo
    for i in range(1, len(subset)):
        #toma el string a comparar
        stringComparado = subset[i]
        #recorre cada letra del string
        for k in range(len(stringResultado)):
            # Si el string comparado es diferente al original y al resultado actual
            if stringComparado[k] != colString[k] and stringComparado[k] != stringResultado[k]:
                stringResultado[k] = stringComparado[k]
    return stringResultado

#GUARDA LA LISTA DE STRIGNS COMBINADOS EN UN NUEVO ARCHIVO CSV
def guardarCombinaciones(stringsCombinados):
    #une las letras de cada string
    stringsUnidos = [''.join(string) for string in stringsCombinados]
    #convierte la lista de strings en un DataFrame
    df = pd.DataFrame(stringsUnidos, columns=['Strings Combinados'])
    #guarda el DataFrame en un archivo CSV
    df.to_csv('ListaDeCombinaciones.csv', index=False)  

#LINEAS PRINCIPALES DEL ARCHIVO
ruta = obtenerArchivo()
if ruta is None:
    print("No se encontro ese archivo")
else:
    df = pd.read_csv(ruta)
    colString = list(df.loc[0, 'string_a_modificar'])
    listaDeChunks = recorrerArreglo(df, colString, 10, 5)
    guardarChunks(listaDeChunks)
    listaCombinados = generarCombinaciones(listaDeChunks)
    guardarCombinaciones(listaCombinados)