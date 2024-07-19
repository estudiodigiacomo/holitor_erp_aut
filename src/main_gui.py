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

        if not clients:
            return

        client_name = [client['name'] for client in clients]

        client_var = tk.StringVar(holistor_window)
        client_var.set(client_name[0])

        tk.Label(holistor_window, text='Seleccione el cliente:').grid()

        client_menu = tk.OptionMenu(holistor_window, client_var, *client_name)
        client_menu.grid()

        def start_automation():
            selected_client = next(client for client in clients if client['name'] == client_var.get())
            login_and_open_vouchers(selected_client['name'], selected_client['cuil'], selected_client['type'])

        btn_login = tk.Button(holistor_window, text='Iniciar automatización', command=start_automation)
        btn_login.grid(row=6, column=0, columnspan=2, padx=5, pady=5, sticky='w')

        holistor_window.mainloop()
    
    except Exception as e:
        print('Error:', str(e))

def login_and_open_vouchers(client_name, cuil, client_type):
    erp_cta_cte(client_name, cuil, client_type)