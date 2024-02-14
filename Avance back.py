import pandas as pd

listaDeChunks = [];

#importa el csv
df = pd.read_csv('dataset.csv');

#guarda en arreglos las columnas
colPosicion = df['posicion'].tolist();
colReferencia = df['referencia'].tolist();
colAlteracion = df['alteracion'].tolist();

#guarda el valor de una celda especifica y lo comvierte a lista
texto = df.loc[0, 'string_a_modificar'];
colString = list(texto);

#imprime todos los datos almacenados
print(colPosicion, "\n");
print(colReferencia, "\n");
print(colAlteracion, "\n");
print(colString, "\n");

#muestra todos los campos evaluados y si deben ser evaluados
def recorrerArreglo(colString, chunk, recorrido):
    posEvaluadas = [];
    chunkEvaluado = [];
    for i in range(0, len(colString), recorrido):
        print("Letras evaluadas: ", end = "");
        for j in range(chunk):
            if i+j < len(colString):
                print(colString[i+j], end = " ");
                posEvaluadas.append(i+j);
                chunkEvaluado.append(colString[i+j]);
        print("\n\n\tPosiciones evaluadas: ", posEvaluadas);
        for k in range(len(posEvaluadas)):
            if posEvaluadas[k] in colPosicion:
                print("\n\tSe debe cambiar la posicion ", posEvaluadas[k]);
        listaDeChunks.append(chunkEvaluado);
        print("\n");
        posEvaluadas = [];
        chunkEvaluado = [];

#guarda la lista de chunks generados en un nuevo csv
def guardarChunks(listadeChunks):
    df = pd.DataFrame(listaDeChunks, columns=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']);
    df.to_csv('ListaDeChunks.csv', index=False);

recorrerArreglo(colString, 10, 5);
guardarChunks(listaDeChunks);

for i in range(len(listaDeChunks)):
    print("Chunk numero ", i, listaDeChunks[i]);