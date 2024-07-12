#login_holistor_erp
from selenium import webdriver
from login_holistor_erp import login_erp
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from datetime import datetime
from dateutil.relativedelta import relativedelta
from selenium.webdriver.common.action_chains import ActionChains
import os
import time

def erp_cta_cte(client_name, company, cuil):
    try:
        driver = login_erp()
        time.sleep(5)
        btn_erp = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By. XPATH, '/html/body/app-root/ng-component/div/default-layout/div/div[2]/div/div[2]/div[3]/ng-component/plataforma-dashboard/div[2]/div/div[1]/div/div[1]/div/img')))
        btn_erp.click()

        #Cambio de iframe (ventana)
        time.sleep(5)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[0])
        driver.switch_to.window(window_to_select[1])

        time.sleep(5)

        #Seleccion de empresa en dropdown
        select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'W0012vEMPRESA')))
        select = Select(select_element)
        for option in select.options:
            if company in option.text:
                option.click()
                break

        btn_into = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'W0012INGRESAR')))
        btn_into.click()

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

        #Formateo de cuit/cuil 
        number_str = str(cuil)
        formatted_cuil = f'{number_str[:2]}-{number_str[2:10]}-{number_str[10]}'

        time.sleep(5)
        
        input_search_client = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'vGENERICFILTER_GRIDCLIENTE')))
        input_search_client.send_keys(client_name)
        time.sleep(5)
        try:
            td_client = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="GridclienteContainerRow_0001"]/td[2]')))
            driver.execute_script("arguments[0].scrollIntoView(true);", td_client)
            img_client = td_client.find_element(By.XPATH, ".//img[@alt='Consultar' and contains(@class, 'Image_Action')]")
            driver.execute_script("arguments[0].click();", img_client)
        except Exception as e:
            print(f"Error al interactuar con la imagen: {e}")

        #Cambio de iframe (ventana)
        time.sleep(3)
        window_to_select = driver.window_handles
        driver.switch_to.window(window_to_select[1])
        driver.switch_to.window(window_to_select[2])

        date_actualy = datetime.now()
        date_actualy_formated = date_actualy.strftime('%d-%m-%Y')
        # Retroceder tres meses
        three_months_ago = date_actualy - relativedelta(months=3)
        date_formated = three_months_ago.strftime('%d/%m/%Y')

        date_from = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'vFECHADESDE')))
        driver.execute_script("arguments[0].value = '';", date_from)        
        time.sleep(1)
        date_from.send_keys(date_formated)            
        time.sleep(1)
        search_date = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="vFECHADESDE_dp_container"]/div/span')))
        search_date.click()

        #Almacena los values en una lista para su posterior suma 
        values_must= []
        individual_must = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,'span_vVALDEU'))).text
        print(individual_must)
        values_must.append(individual_must)

        current_month = datetime.now().month
        current_year = datetime.now().year
        tbody = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="GridContainerTbl"]/tbody')))
        rows = tbody.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            first_cell = row.find_element(By.TAG_NAME, 'td')
            date_text = first_cell.text.strip()
            try:
                date_obj = datetime.strptime(date_text, "%d/%m/%Y")
                if date_obj.month == current_month and date_obj.year == current_year:
                    driver.execute_script("arguments[0].scrollIntoView(true);", row)
                    td_to_click = row.find_elements(By.TAG_NAME, 'td')[11]
                    img_client = td_to_click.find_element(By.XPATH, ".//img[@alt='Imprimir' and contains(@class, 'Image_Action')]")
                    driver.execute_script("arguments[0].click();", img_client)

                    iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'gxp0_ifrm')))        
                    print_resume = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'DOWNLOADFILE1')))
                    print_resume.click()
                    time.sleep(5)
                    driver.switch_to.default_content()
                    popup = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "gxp0_t")))
                    close_button = popup.find_element(By.XPATH, ".//span[@class='PopupHeaderButton gx-popup-close' and @id='gxp0_cls']")
                    driver.execute_script("arguments[0].click();", close_button)
                    
            except ValueError:
                print(f"Invalid date format: {date_text}")

        time.sleep(20)

        print_resume_btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'IMPRIME')))
        print_resume_btn.click()
        time.sleep(5)
        iframe = WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'gxp0_ifrm')))        
        print_resume = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,'DOWNLOADFILE1')))
        print_resume.click()
        driver.switch_to.default_content()

        # Obtener la lista de archivos en la carpeta
        new_name = f'Emision de Cuentas Corrientes {date_formated} - {date_actualy_formated}'
        folder_path = r'c:\bot_resumen_cta_cte'
        file = [os.path.join(folder_path, archivo) for archivo in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, archivo))]
        end_file = max(file, key=os.path.getctime)
        extension = os.path.splitext(end_file)[1]
        new_name_file = os.path.join(folder_path, new_name + extension)
        os.rename(end_file, new_name_file)
        print(f"El archivo '{end_file}' ha sido renombrado a '{new_name_file}'.")
        time.sleep(5)

    except Exception as e:
        print('Error:', str(e))
