import pandas as pd
import requests
import json
import psycopg2
import sqlalchemy as sa
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.engine.url import URL
from dotenv import load_dotenv
import os

load_dotenv()

#PASO 1: CONECTARSE A LA API

API_KEY = os.getenv("API_KEY")

#url para ver todos los eventos
#url = "https://app.ticketmaster.com/discovery/v2/events.json?apikey=" + API_KEY

#url para ver solo los eventos de música
url = "https://app.ticketmaster.com/discovery/v2/events.json?classificationName=music&dmaId=324&apikey=" + API_KEY

response = requests.get(url)

if response.status_code == 200:
    datos_2 = response.json()
    eventos_musica = datos_2['_embedded']['events'] #para quedarme con los eventos que informa en el json
    df_eventos_musica = pd.DataFrame(eventos_musica)
    #PRIMER PUNTO DE CONTROL BIEN
    print("Se ha conectado a la API con éxito")
else:
    #PRIMER PUNTO DE CONTROL MAL
    print("Error al conectar a la API: " ,response)


#PASO 2: ELEGIR LOS DATOS QUE NOS INTERESAN

#columnas base
df_final = df_eventos_musica[['name','id','url','locale']]

#La demás información las tendremos que sacar de columnas cuyas celdas contienen json o diccionarios.
#VENTA
df_expand_sales = pd.json_normalize(df_eventos_musica.sales)
df_expand_sales = df_expand_sales[['public.startDateTime', 'public.endDateTime']]
df_final = pd.concat([df_final ,df_expand_sales], axis=1)

#DIA DEL EVENTO
df_expand_dates = pd.json_normalize(df_eventos_musica.dates)
df_expand_dates = df_expand_dates[['timezone','start.localDate', 'start.localTime',]]
df_final = pd.concat([df_final ,df_expand_dates], axis=1)

#PRECIO (diccionario)
df_expand_priceRanges = pd.json_normalize(df_eventos_musica.priceRanges)
data = list(df_expand_priceRanges[0])
# Filtrar los valores None de la lista de datos
filtered_data = [d if d is not None else {} for d in data]
# Convertir la lista de diccionarios en un DataFrame
df_expand_priceRanges = pd.DataFrame(filtered_data)
df_final = pd.concat([df_final ,df_expand_priceRanges], axis=1)

#borramos las filas que puedan estar duplicadas
df_final = df_final.drop_duplicates()


#SEGUNDO PUNTO DE CONTROL
print('La tabla se ha creado con éxito')


#Paso 3: importar los datos a redshift
#creo una función.
def cargar_tabla_redshift(df, table_name):
    """
    Carga un DataFrame en una tabla de Redshift.

    Args:
    - df: DataFrame que se va a cargar en Redshift.
    - table_name: Nombre de la tabla en Redshift.
    - conn_str: Cadena de conexión a la base de datos de Redshift.

    Returns:
    - str: Mensaje indicando el resultado de la operación.
    """
    try:
        # Establecer la conexión a Redshift - Cadena sqlalchemy URL
        url = URL.create(
        drivername='redshift+redshift_connector', 
        host=os.getenv("HOST"),
        port=os.getenv("PORT"), 
        database=os.getenv("DBNAME"),
        username=os.getenv("USER"),
        password = os.getenv("PASSWORD")
        )

        engine = sa.create_engine(url)
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        return f'Se cargó la tabla {table_name} exitosamente'
    except SQLAlchemyError as e:
        # Mensaje de error+
        return f"Error al cargar el DataFrame en Redshift: {str(e)}"

tabla = 'ticket_master_conciertos'
cargar_tabla_redshift(df_final, tabla)
