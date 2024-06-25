import pandas as pd
import matplotlib.pyplot as plt


dfs= [
    pd.read_csv('Data/GlobalLandTemperaturesByCountry.csv'), 
    pd.read_csv('Data/india-gdp-gross-domestic-product.csv'), 
    pd.read_csv('Data/Country-tree-cover-loss.csv')
]

for dataframe in dfs:
    dataframe.dropna(inplace = True)
    dataframe.reset_index(drop = True, inplace = True)


def city_search(Country):

    '''Esta función permite crear una lista con las temperaturas (y su año) para una determinada ciudad en todo el DataFrame.'''

    dfs[0]['dt'] = pd.to_datetime(dfs[0]['dt'])
    dfs[0]['Year'] = dfs[0]['dt'].dt.year
    # Obtener el año inicial y final de los datos
    start_year = dfs[0]['dt'].dt.year.min()
    end_year = dfs[0]['dt'].dt.year.max()
    
    # Filtrar el DataFrame para el país específico y años completos a partir de '1960-01-01'
    country_data = dfs[0][(dfs[0]['Country'] == Country) & (dfs[0]['Year'] >= 1960)].drop_duplicates(subset=['Year'])
    #country_data = dfs[0][(dfs[0]['Country'] == Country) & (dfs[0]['dt'] >= pd.Timestamp(f'{1960}-01-01'))]
    #country_data = dfs[0][(dfs[0]['Country'] == Country) & (dfs[0]['dt'].str[:6].astype(int) >= 1960)]

    first_appearing = country_data.index.min()
    last_appearing = country_data.index.max()

    lista = dfs[0].loc[first_appearing : last_appearing, ['AverageTemperature', 'Year']]


    return lista, country_data, first_appearing, last_appearing

a = city_search('India')

print(a[1])

c = a[1].loc[a[2]: a[3], 'AverageTemperature']
#print(c.describe())
#print(c)
d = a[1].loc[a[2] : a[3], 'Year']

lista_datos_1 = []
lista_datos_2 = []

for i in range(a[2], a[3]):
    lista_datos_1.append(c.get(i))
    lista_datos_2.append(d.get(i))

#print(lista_datos_2)
#serie = pd.Series(lista_datos, index = lista_indices)

#ubicaciones = pd.date_range(start='1850', end='2020', freq='10Y')
plot = plt.scatter(lista_datos_2, lista_datos_1)
plt.gca().set_ylim([10, 22])
plt.show()

#b = city_search('Addis Abeba').sort_values(by = 'AverageTemperature', ascending = False)

#print(b)
