from selenium import webdriver
from login_holistor_erp import login_erp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
from utils.folder_report import folders_report
import os
import time
import shutil

def erp_cta_cte(client_name, cuil, client_type):
    try:
        companys_true = ["0000000003 - DI GIÁCOMO NICOLAS"]
        companys_false = [
            "0000000003 - DI GIÁCOMO NICOLAS", 
            "0000000001 - DI GIACOMO FRANCISCO", 
            "0000000002 - DI GIÁCOMO JUAN EZEQUIEL"
        ]

        companys = companys_true if client_type == "TRUE" else companys_false
        values_must = []

        driver = login_erp()
        time.sleep(5)

        # Si encuentra elemento de alerta
        try:
            window_alert = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div/div")))

            btn_close_alert = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div[3]/button[1]')))
            btn_close_alert.click()

        except TimeoutException:
            print("Alerta no encontrada, continuar")

        btn_erp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[3]/ng-component/plataforma-dashboard/div[2]/div/div[1]/div/div[1]/div/img')))
        btn_erp.click()

        # Cambio de iframe (ventana)
        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[0])
        driver.switch_to.window(window_to_select[1])

        time.sleep(5)

        for index, company in enumerate(companys):
            # Selección de empresa en dropdown
            select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'W0012vEMPRESA')))
            select = Select(select_element)
            for option in select.options:
                if company in option.text:
                    option.click()
                    break
            btn_into = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'W0012INGRESAR')))
            btn_into.click()
            print('btn into')
            time.sleep(5)
            hamburger = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'BTNTOGGLEMENU_MPAGE')))
            hamburger.click()
            time.sleep(3)
            buys_btn_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[2]/a/span[1]')))
            buys_btn_dropdown.click()
            time.sleep(3)
            cta_btn_dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[2]/ul/li[5]/a/span[1]')))
            cta_btn_dropdown.click()
            time.sleep(3)
            
            cta_cte_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/form/div[2]/div[2]/div/div[2]/div[1]/div/div/div/div/aside/nav/ul/li[2]/ul/li[5]/ul/li[1]/a/span')))
            cta_cte_btn.click() 

            time.sleep(5)
            
            input_search_client = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'vGENERICFILTER_GRIDCLIENTE')))
            input_search_client.send_keys(client_name)
            time.sleep(5)

            td_client = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="GridclienteContainerRow_0001"]/td[2]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", td_client)
            img_client = td_client.find_element(By.XPATH, ".//img[@alt='Consultar' and contains(@class, 'Image_Action')]")
            driver.execute_script("arguments[0].click();", img_client)

            # Cambio de iframe (ventana)
            time.sleep(3)
            window_to_select = driver.window_handles
            driver.switch_to.window(window_to_select[1])
            driver.switch_to.window(window_to_select[2])

            date_actualy = datetime.now()
            date_actualy_formated = date_actualy.strftime('%d-%m-%Y')
            # Retroceder tres meses
            three_months_ago = date_actualy - relativedelta(months=3)
            date_formated_three_months = three_months_ago.strftime('%d/%m/%Y')
        
            date_from = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'vFECHADESDE')))
            driver.execute_script("arguments[0].value = '';", date_from)        
            time.sleep(1)
            date_from.send_keys(date_formated_three_months)            
            time.sleep(1)
            search_date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vFECHADESDE_dp_container"]/div/span')))
            search_date.click()
            individual_must = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'span_vVALDEU'))).text
            if(individual_must) == '0,00':
                user_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="vUSERAVATARSMALL_MPAGE"]')))
                user_btn.click()
                time.sleep(2)
                change_company_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="CHANGEEMPRESA_MPAGE"]/a')))
                change_company_btn.click()

                time.sleep(5)
                continue
            else:
                number_format = individual_must.replace('.', '').replace(',', '.')
                number_float = float(number_format)
                values_must.append(number_float)

            current_month = datetime.now().month
            current_year = datetime.now().year
            tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GridContainerTbl"]/tbody')))
            rows = tbody.find_elements(By.TAG_NAME, 'tr')

            # Formateo nombre de cliente a capitalize
            client_name_formated = client_name.title()
            # Ruta del directorio de descarga 
            folder_date_emision = folders_report(client_name_formated)

            downloaded_vouchers = set()

            while True:
                tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GridContainerTbl"]/tbody')))
                rows = tbody.find_elements(By.TAG_NAME, 'tr')
                all_rows_processed = True

                for row in rows:
                    first_cell = row.find_element(By.TAG_NAME, 'td')
                    date_text = first_cell.text.strip()
                    try:
                        date_obj = datetime.strptime(date_text, "%d/%m/%Y")
                        if date_obj.month == current_month and date_obj.year == current_year:
                            # Obtener número de factura
                            voucher_td = row.find_elements(By.TAG_NAME, 'td')[1]
                            number_voucher = voucher_td.find_element(By.TAG_NAME, 'span').text
                            
                            if number_voucher in downloaded_vouchers:
                                continue  # Saltar si la factura ya ha sido descargada

                            driver.execute_script("arguments[0].scrollIntoView(true);", row)
                            td_to_click = row.find_elements(By.TAG_NAME, 'td')[11]
                            img_client = td_to_click.find_element(By.XPATH, ".//img[@alt='Imprimir' and contains(@class, 'Image_Action')]")
                            driver.execute_script("arguments[0].click();", img_client)

                            iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'gxp0_ifrm')))
                            print_voucher = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'DOWNLOADFILE1')))
                            print_voucher.click()
                            time.sleep(5)
                            driver.switch_to.default_content()
                            popup = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "gxp0_t")))
                            close_button = popup.find_element(By.XPATH, ".//span[@class='PopupHeaderButton gx-popup-close' and @id='gxp0_cls']")
                            driver.execute_script("arguments[0].click();", close_button)
                            time.sleep(5)
                            formatted_date_vouchers = date_obj.strftime("%d-%m-%Y")
                            # Busco archivos en el directorio
                            route_base = r'c:\bot_resumen_cta_cte'
                            list_of_files = os.listdir(route_base)
                            find_file = max(list_of_files, key=lambda f: os.path.getctime(os.path.join(route_base, f)))
                            # Mover el archivo más reciente al directorio de destino
                            shutil.move(os.path.join(route_base, find_file), folder_date_emision)
                            # Verificar que el archivo se haya movido correctamente
                            name_file_pdf = f'Holistor ERP - Factura - {client_name} - {number_voucher} - Emisión {formatted_date_vouchers}.pdf'
                            rute_destiny = os.path.join(folder_date_emision, find_file)
                            new_file_path = os.path.join(folder_date_emision, name_file_pdf)
                            os.rename(rute_destiny, new_file_path)
                            if os.path.exists(new_file_path):
                                print("El archivo de factura se movió correctamente")

                            downloaded_vouchers.add(number_voucher)  # Marcar la factura como descargada

                            all_rows_processed = False
                            break  # Salir del bucle para volver a localizar las filas

                    except ValueError:
                        print(f"Invalid date format: {date_text}")

                if all_rows_processed:
                    break
            time.sleep(5)
            try:
                print_resume_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'IMPRIME')))
                print_resume_btn.click()

                time.sleep(5)
                iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'gxp0_ifrm')))        
                print_resume = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'DOWNLOADFILE1')))
                print_resume.click()
                time.sleep(3)
                driver.switch_to.default_content()
                popup = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "gxp0_t")))
                close_button = popup.find_element(By.XPATH, ".//span[@class='PopupHeaderButton gx-popup-close' and @id='gxp0_cls']")
                driver.execute_script("arguments[0].click();", close_button)

                date_three_months_ago = date_actualy - relativedelta(months=3)
                formated_three_months = date_three_months_ago.strftime('%d-%m-%Y')

                # Busco archivos en el directorio
                route_base = r'c:\bot_resumen_cta_cte'
                list_of_files = os.listdir(route_base)
                find_file = max(list_of_files, key=lambda f: os.path.getctime(os.path.join(route_base, f)))
                # Mover el archivo más reciente al directorio de destino
                shutil.move(os.path.join(route_base, find_file), folder_date_emision)
                # Verificar que el archivo se haya movido correctamente
                name_file_pdf = f'Holistor ERP - Resumen - {client_name} - Desde {formated_three_months} - Hasta {date_actualy_formated} - Emisión {date_actualy_formated}.pdf'
                rute_destiny = os.path.join(folder_date_emision, find_file)
                new_file_path = os.path.join(folder_date_emision, name_file_pdf)
                os.rename(rute_destiny, new_file_path)
                if os.path.exists(new_file_path):
                    print("El archivo de resumen se movió correctamente")
            except ValueError:
                print(f"Falla al procesar el resumen")

            # Si solo se procesa "0000000003 - DI GIÁCOMO NICOLAS", cerrar el navegador
            if client_type == "TRUE":
                driver.quit()
                break
            # Volver a la selección de empresa
            user_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="vUSERAVATARSMALL_MPAGE"]')))
            user_btn.click()

            change_company_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="CHANGEEMPRESA_MPAGE"]/a')))
            change_company_btn.click()

            time.sleep(5)

        # Guardar la suma de values_must en un archivo txt
        total_value = sum(values_must)
        total_str = str(total_value)
        with open(os.path.join(folder_date_emision, 'total_deuda.txt'), 'w') as file:
            file.write(total_str)

    except Exception as e:
        print('Error:', str(e))
        driver.quit()
