import pandas as pd

posEvaluadas = [];

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
for i in range(0, len(colString), 5):
    print("Letras evaluadas: ", end = "");
    for j in range(10):
        if i+j < len(colString):
            print(colString[i+j], end = " ");
            posEvaluadas.append(i+j);
    print("\n\n\tPosiciones evaluadas: ", posEvaluadas);
    for k in range(len(posEvaluadas)):
        if posEvaluadas[k] in colPosicion:
            print("\n\tSe debe cambiar la posicion ", posEvaluadas[k]);
    
    print("\n");
    posEvaluadas = [];

                 
