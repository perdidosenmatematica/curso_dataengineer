import pandas as pd
import requests
import json
import psycopg2
from sqlalchemy import create_engine


#PASO 1: CONECTARSE A LA API

API_KEY = "R2G7fFI8rrBZJefdtU18G69CH4sMhEff"

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
print('la tabla se ha creado con éxito')


#Paso 3: importar los datos a redshift
# Establecer la conexión a Redshift
host = ' http://data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com/'
port = '5439'
dbname = 'data-engineer-database'
user = 'danielarbrot_coderhouse'
password = 'xxxx'

# Construir la cadena de conexión
conn_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'

# Crear un motor de SQLAlchemy
engine = create_engine(conn_str)

# Nombre de la tabla en Redshift
table_name = 'daniela_brot.ticket_master_conciertos'

# Trasladar el DataFrame a Redshift dond ese pisará
df_final.to_sql(table_name, engine, index=False, if_exists='replace')

#En caso de querer volcarlos últimos el DataFrame en la tabla en Redshift
#df_final.to_sql(table_name, engine, index=False, if_exists='append')


print("DataFrame trasladado exitosamente a Redshift.")