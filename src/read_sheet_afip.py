#Read Sheets
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError
from googleapiclient.errors import HttpError
from tkinter import messagebox

#Leer datos de hoja de google sheets
def get_clients_from_sheets():
    #Api spreadsheets
    SCOPE = ['https://www.googleapis.com/auth/spreadsheets']
    #Ruta del archivo con las credenciales
    KEY = 'keys.json'
    #ID del documento de Google Sheets
    SPREADSHEET_ID = '1H9XZNTUqqa-MsOXjm2LjelfnFAtXbNIIv_55yRj_aGI'

    try:
        creds = service_account.Credentials.from_service_account_file(KEY, scopes= SCOPE)
        service = build('sheets' , 'v4', credentials= creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId= SPREADSHEET_ID, range='erp_db!A2:B118').execute()
        values = result.get('values', [])
        
        #Busqueda de datos
        if values:
            #Almaceno los clientes en una lista
            clients = []
            for row in values:
                client_name, cuil = row
                clients.append({
                    'name': client_name, 
                    'cuil': cuil
                    })
            return clients
        else: 
            messagebox.showerror('Error', 'No se encontraron datos en la hoja de Google Sheets')
            return []
    #Excepcion para manejo de errores varios
    except GoogleAuthError as auth_error:
        messagebox.showerror('Error de autenticacion', str(auth_error))
        return []
    except HttpError as http_error:
        messagebox.showerror('Error HTTP', str(http_error))
        return []
    except Exception as e:
        messagebox.showerror('Error inesperado', str(e))
        return []
    
get_clients_from_sheets()
