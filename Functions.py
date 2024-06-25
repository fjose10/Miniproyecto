import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr, spearmanr


def calcular_correlacion(df1, df2):

    """
    Calcula el coeficiente de correlación de Pearson y Spearmann entre dos columnas de dos DataFrames.
    
    Argumentos:
    - df1: DataFrame 1.
    - df2: DataFrame 2.

    Nota: Los dataframes se deben pasar con una columna ya con los valores normalizados.
    Esto puede generalizarse agregando dos parametros como los de abajo, pero no se hizo de esta forma.

    - col_name_df1: Nombre de la columna del DataFrame 1.
    - col_name_df2: Nombre de la columna del DataFrame 2.
    
    Reegresa:
    - Coeficiente de correlación de Pearson y Spearmann
    """
    # Verificar que las columnas existen en los DataFrames

    if 'Valores Normalizados' not in df1.columns or 'Valores Normalizados' not in df2.columns:
        raise ValueError("Las columnas especificadas no existen en los DataFrames.")
    
    # Crear una variable que almacene los valores de la columna de cada dataframe
    col_df1 = df1['Valores Normalizados']
    col_df2 = df2['Valores Normalizados']
    
    # Calcular el coeficiente de correlación de Pearson
    corr_coef, _ = pearsonr(col_df1, col_df2)
    corr_coef_1, _ = spearmanr(col_df1, col_df2)   #En la presentación no se usó este coeficiente por tiempo.
    return corr_coef, corr_coef_1,

def normalizar(df, col_df):

    """
    Esta función normaliza los valores de una columna de un dataframe para que estén en el rango de 0 a 1. 

    Argumentos: 
    -df: DataFrame
    -col_df: Un str con el nombre exacto de la columna del DataFrame con los valores a normalizar. 
    
    Regresa:
    -El mismo DataFrame con una nueva columna llamada 'Valores Normalizados'

    """

    if col_df not in df.columns:
        raise ValueError("La columna especificada no existe en el DataFrame.")

    minimum = df[col_df].min()   #Encuentra el valor minimo de la columna
    maximum = df[col_df].max()   #Encuentra el valor maximo de la columna

    df['Valores Normalizados'] = (df[col_df] - minimum) / (maximum - minimum)

def graficar(df1, df2, x, label, titulo, color, coef, x_value):

    """
    Crea una gráfica de dispersión de dos tablas de datos en términos del tiempo
    
    Args:
    - df1: DataFrame con las temperaturas de enero en los años a emplear
    - df2: DataFrame con los datos de la variable socioeconómica analizada
    - x: String con el nombre de la columna donde estan las fechas a emplear
    - label: String con el nombre de la variable socioeconómica analizada
    - titulo: String con el titulo de la grafica 
    - color: String con el color de los datos del segundo dataframe
    - coef: Valor del coeficiente de correlacion de Pearson entre los datos de ambos dataframes
    - x_value: Valor desde donde inicia el eje x
 
    Regresa:
    Una grafica de dispersion de dos variables

    """

    plt.scatter(df1[x], df1['Valores Normalizados'], color = 'blue', label='Temperatura')
    plt.scatter(df1[x], df2['Valores Normalizados'], color = color, label= label)
    
    # Etiquetas de los ejes
    plt.xlabel('Año')
    plt.ylabel('Valores normalizados')

    # Título del gráfico
    plt.title(titulo)
    plt.legend()
    plt.tight_layout()   #Para poder ajustar la gráfica

    #Cuadro de texto que muestra el coeficiente de correlación de Pearson en la gráfica
    plt.text(x_value, 0.8, 'Coeficiente de Pearson: {:.2f}'.format(coef), fontsize=10, bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))

    # Mostrar la gráfica
    plt.show()


def dividir_df(df_1, df_2, condicion):

    """
    Crea dos dataframes a partir de otros dos con condiciones específicas

    Argumentos:
    - df_1: Dataframe de la variable socioeconomica analizada.
    - df_2: Dataframe con las temperaturas superficiales
    - condicion: Año desde donde se tomarán las temperaturas
    
    """

    '''Todos los dataframes del primer argumento entrantes a esta funcion tienen una columna llamada 'date' 
    con el formato año/mes/día. Como no se quiere trabajar por mes, se convierte a formato datetime los 
    valores de esta columna para luego hacer un filtro con solo los años.
    '''
    
    df_1['date'] = pd.to_datetime(df_1['date'])
    
    '''
    Se crea un dataframe nuevo imponiendo la condicion sobre el entrante que solo se tomen los valores
    desde 2017 hacia atrás (Dentro se crea un booleano de Trues o False que filtra qué valores se admiten) 
    Esto se hace así porque los datasetes de las variables socioeconómicas poseen los datos hasta 2022, 
    mientras que las temperaturas solo se tienen hasta 2017.
    '''
    df_1_filtrado = pd.DataFrame(df_1[(pd.DatetimeIndex(df_1['date']).year <= 2017 )])


    '''
    El dataset de temperaturas posee datos desde 1900 hasta 2017. Para filtrar los años, se usa el argumento
    condición, que no es más que el mínimo año para el cual se tiene la variablesocioeconómica medida, el cual
    variaba según la variable (por ejemplo, en algunos era 1960, en otros 1950, 1990, etc.)
    '''
    df_2_filtrado = df_2.loc[(df_2['YEAR'] >= condicion), ['YEAR','JAN']]

    return df_1_filtrado, df_2_filtrado

