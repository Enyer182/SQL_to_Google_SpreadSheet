import mysql.connector as mariadb
import pandas as pd
from df2gspread import df2gspread as d2g
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#Bloque para autorizar permisos para google sheets junto con las credenciales
#Se deben crear las credenciales en la consola de Developers de Google 
#el file .json que contiene los parametros necesarios para autorizar
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'credenciales_google_json', scope)
gc = gspread.authorize(credentials)

#Nos conectamos a la base con los parametros para autorizar.
mariadb_conexion = mariadb.connect(host='host', port='puerto', user='usuario', password='contraseña', database='nombre de la base')
cursor = mariadb_conexion.cursor()

try:
    
    sql_query = pd.read_sql_query("SELECT NOMBRE, VINCULADO, ID_AGENTE FROM fichada_user", mariadb_conexion) #Instanciamos dentro del metodo pd.read_sql_query que nos proporciona la libreria pandas para hacer lectura de la tabla de datos
    df = pd.DataFrame(sql_query, columns=['NOMBRE','VINCULADO','ID_AGENTE']) #Armamos el dataframe o dataset #con las columnas correspondientes en este caso mi tabla se llama fichada_user
    print (df)
    spreadsheet_key ='1TWabuh0PCtPbw4RJ_P70CaBNj_nskAHACm5vfeM0chc' #este es el ID o key de SpreadSheet la encontramos en la URL del documento del Spreadsheet en donde trabajaremos
    wks_name = 'new_mariadb' #Nombre de la pestaña/solapa
    wks = gc.open('new_mariadb').sheet1
    wks = d2g.upload(df, spreadsheet_key, credentials=credentials, row_names=True) #Subimos la data con el metodo que nos proporciona la libreria d2gspread

except mariadb.Error as error:
    print("Error: {}".format(error))

mariadb_conexion.close()