import tkinter as tk
from tkcalendar import DateEntry
from read_sheet_afip import get_clients_from_sheets
from erp_cta_cte import erp_cta_cte
import time

def main_gui():
    try:
        holistor_window = tk.Tk()
        holistor_window.title('Automatizacion de Holistor')
        holistor_window.geometry('400x200')
        clients = get_clients_from_sheets()

        client_name = [client['name'] for client in clients]

        client_var = tk.StringVar(holistor_window)
        client_var.set(client_name[0])

        tk.Label(holistor_window, text='Seleccione el cliente:').grid()

        client_menu = tk.OptionMenu(holistor_window, client_var, *client_name)
        client_menu.grid()

        for client in clients:
            if client['name'] == client_var.get():
                cuil = client['cuil']

        companys_types = ["0000000003 - DI GIÁCOMO NICOLAS", "0000000001 - DI GIACOMO FRANCISCO", "0000000002 - DI GIÁCOMO JUAN EZEQUIEL"]
        companys_var = tk.StringVar(holistor_window)
        companys_var.set(companys_types[0])
        tk.Label(holistor_window, text='Selecciona el tipo de empresa:').grid()
        companys_menu = tk.OptionMenu(holistor_window, companys_var, *companys_types)
        companys_menu.grid()

        #Inicio de automatizacion
        btn_login = tk.Button(holistor_window, text='Iniciar automatizacion', command=lambda: login_and_open_vouchers(client_var.get(), companys_var.get(), cuil))
        btn_login.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='w')

        holistor_window.mainloop()
    
    except Exception as e:
        print('Error:', str(e))

def login_and_open_vouchers(client_name, company, cuil):
    print(client_name, cuil)
    erp_cta_cte(client_name, company, cuil)