## Curso de data engineer
Es un curso que de 3 meses que he realizado de forma virtual en coderhouse.
El mismo constó de 4 entregas. 

### La primera entraga consistió en:
- Generar un script (formato .py o .ipynb) que funcione como prototipo (MVP) de un ETL para el proyecto final
- El script debería extraer datos desde una API en formato JSON para ser manipulado como diccionario utilizando el lenguaje Python
- Generar una tabla para ser almacenada en una base de datos a partir de información una API.

********
En mi caso elegí conectarme a la API de ticketmaster para extraer los conciertos publicados. 
********

### La segunda entraga consistió en:
- El script de la entrega 1 deberá adaptar datos leídos de la API y cargarlos en la tabla creada en la pre-entrega anterior en Redshift de forma eficiente. En esta entrega se hace énfasis en la limpieza de los datos crudos obtenidos de la API
- Generar ETLs a partir de información de APIs usando las librerías requests, json, psycopg2/SqlAlchemy y pandas
- Solucionar una situación real de ETL donde puedan llegar a aparecer duplicados, nulos y valores atípicos durante la ingesta- Transformación- Carga de la data

### La tercera entraga consistió en:
- Crear un script liviano y funcional que pueda ser utilizado en cualquier Sistema operativo y por cualquier usuario. 
- Dockerizar un script para hacerlo funcional en cualquier sistema operativo. 

### La cuarta entraga consistió en:
Crear un pipeline que extraiga datos de una API pública de forma constante combinándolos con información extraída de una base de datos (mínimamente estas 2 fuentes de datos, pero pueden utilizarse hasta 4).
Colocar los datos extraídos en un Data Warehouse. 
Automatizar el proceso que extraerá, transformará y cargará datos cuantitativos (ejemplo estos son: valores de acciones de la bolsa, temperatura de ciudades seleccionadas, valor de una moneda comparado con el dólar, casos de covid). 
Automatizar el proceso para lanzar alertas (2 máximo) por e-mail en caso de que un valor sobrepase un límite configurado en el código.
