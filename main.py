
import pandas as pd
from Functions import normalizar, graficar, calcular_correlacion, dividir_df
import matplotlib.pyplot as plt

dfs = [        #Creación de los datasets a utilizar
    pd.read_csv('Data/temperatures.csv'),
    pd.read_csv('Data/india-gdp-gross-domestic-product.csv'),
    pd.read_csv('Data/india-population.csv'),
    pd.read_csv('Data/india-exports.csv'),
    pd.read_csv('Data/india-carbon-co2-emissions.csv'),
    pd.read_csv('Data/india-manufacturing-output.csv'),
    pd.read_csv('Data/Country-tree-cover-loss.csv')
]

dfs[1]['date'] = pd.to_datetime(dfs[1]['date'])   
dfs[1]['Year'] = dfs[1]['date'].dt.year

#### Análisis de cobertura arbórea vs temperatura

'''Aqui no se usó la función "dividir_df" pues el dataframe de perdida arbórea no sigue el mismo formato de los demás'''

#Creación de dataset con las temperaturas para el año 2001 en adelante (Hasta 2017)
temp_filtradas = dfs[0].loc[(dfs[0]['YEAR'] >= 2001), ['YEAR','JAN']]  

'''
Sobre este dataset existen diferentes valores de 'treshold' que indica en resumidas cuentas qué tanto
de las áreas analiadas se considera "cobertura arbórea". Según el dataset, se recomendaba los datos para
un valor >= 30%. La función iloc crea otro dataset con las columnas 6 hasta la 23 (Que son aquellas donde
están los datos de cobertura arbórea) y hace .melt() para convertir todo a una sola columna con los valores
de estas columnas y así tener un dataset con una sola columna y distintos índices para iterarlo.
'''
tree_cover_loss = pd.DataFrame(dfs[6][(dfs[6]['threshold'] == 30)]).iloc[:, 6:23].melt()

normalizar(temp_filtradas, 'JAN')
normalizar(tree_cover_loss, 'value')

coef_1 = calcular_correlacion(temp_filtradas, tree_cover_loss)
print('El coeficiente de correlación de pearson es {}'.format(coef_1[0]))

graficar(temp_filtradas, tree_cover_loss, 'YEAR','Perdida de cobertura arbórea', 'Pérdida de cobertura arbórea y temperatura superficial desde 2001 hasta 2017', 'magenta', coef_1[0], 2001)


#### Creación de las gráficas de las variables PIB, Población, Exportaciones, Emisiones de CO2 y Producción manufacturera

# Estos 5 dataframes tenían un formato muy parecido y es por eso que fue más eficiente analizarlos de esta forma 

claves = [' GDP ( Billions of US $)', ' Population', 'Exports Billions of US $', ' Kilotons of Co2', 'Output Billions of US $']
condiciones = [1960, 1950, 1960, 1990, 1960]
label = ['PIB', 'Población', 'Exportaciones', 'Emisiones de CO2', 'Producción manufacturera']
titulos = ['Temperatura superficial y PIB de India desde 1960 hasta 2017', 'Población de la india y temperatura superficial desde 1950 hasta 2017', 'Dinero de exportaciones y temperatura superficial en la India desde 1960 hasta 2017',
            'Emisiones de CO2 y temperatura superficial en la India desde 1990 hasta 2017', 'Producción manufacturera y temperatura superficial en la India desde 1960 hasta 2017']
colores = ['red', 'green', 'orange', 'black', 'purple']

suma_1 = 0

for i in range(1,6):

    df = dividir_df(dfs[i], dfs[0], condiciones[i - 1])

    normalizar(df[0], claves[i - 1])
    normalizar(df[1], 'JAN')

    coef= calcular_correlacion(df[1], df[0])
    print('El coeficiente de correlación de pearson es {}'.format(coef[0]))
    graficar(df[1], df[0], 'YEAR', label[i - 1], titulos[i - 1], colores[i - 1], coef[0], condiciones[i - 1] )
    suma_1 = suma_1 + coef[0]


print('El promedio del coeficiente de Pearson de la actividad humana es de {:.2f}'.format((suma_1 + coef_1[0])/6))


#### Gráfica de temperatura vs tiempo para visualizar la problemática del proyecto

plt.scatter(dfs[0]['YEAR'], dfs[0]['JAN'])
plt.xlabel('Año')
plt.ylabel('Temperatura (°C)')
plt.title('Temperatura superficial de la India desde 1901 hasta 2017')
plt.legend()
plt.tight_layout()

plt.show()


