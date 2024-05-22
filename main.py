from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

import requests
from bs4 import BeautifulSoup


import re
from bs4 import BeautifulSoup

def get_data(url, driver, seen_financetype_ids) -> dict:
    # Otevření URL pomocí Selenium WebDriver
    driver.get(url)
    # Získání zdrojového kódu stránky
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    # Inicializace proměnných
    reqid = None
    proid = None
    financetype_id = None
    name = None
    amount = None
    financetype_name = None

    # Extrakce reqid a proid ze skriptu na stránce
    script_elements = soup.find_all('script', type='text/javascript')
    for script in script_elements:
        script_text = script.get_text(strip=True)
        # Vyhledání reqid a proid pomocí regulárních výrazů
        reqid_match = re.search(r"vav\.reqid\s*=\s*'(\d+)'", script_text)
        proid_match = re.search(r"vav\.proid\s*=\s*'(\d+)'", script_text)
        
        if reqid_match and proid_match:
            reqid = reqid_match.group(1)
            proid = proid_match.group(1)

    # Extrakce částky
    amount_row = soup.find('td', class_='head', text='Předpokládaná hodnota veřejné zakázky v Kč s DPH')
    if amount_row:
        amount_value = amount_row.find_next_sibling('td', class_='left-align').get_text(strip=True)
        amount = amount_value.replace('&nbsp;', '').replace(' ', '').replace(',', '.')

    # Extrakce názvu
    name_row = soup.find('td', class_='head', text='Název')
    if name_row:
        name = name_row.find_next_sibling('td', class_='left-align').get_text(strip=True)

    # Extrakce financetype_id a financetype_name
    financetype_row = soup.find('td', class_='head', text='Rozpočtová položka')
    if financetype_row:
        financetype_div = financetype_row.find_next_sibling('td', class_='left').find('div')
        if financetype_div:
            financetype_text = financetype_div.get_text(strip=True)
            split_text = financetype_text.split(' - ', 1)
            if len(split_text) == 2:
                financetype_id, financetype_name = split_text
            else:
                financetype_id = split_text[0]
                financetype_name = ''

  
    
    project_finances = []
    project_financetypes = []
    

    if reqid and proid and amount and name and financetype_id is not None:
        project_finance = {
            "id": reqid,
            "project_id": proid,
            "amount": amount,
            "name": name,
            "financetype_id": financetype_id
        }
        project_finances.append(project_finance)
        # Kontrola, zda financetype_id nebylo již zaznamenáno nebo neni null
        if financetype_id not in seen_financetype_ids and financetype_id != '-':
            project_financetype = {
                "id": financetype_id,
                "name": financetype_name
            }
            project_financetypes.append(project_financetype)
            seen_financetype_ids.add(financetype_id)

    return {
        "projectfinances": project_finances,
        "projectfinancetypes": project_financetypes
    }

def user_id(base_url_start, base_url_end, driver):
    # Načtení uživatelských ID z textového souboru
    with open('user_ids_test.txt', 'r') as file:
        user_ids = file.readlines()


    complete_urls = []
    for user_id in user_ids:
        complete_url = f"{base_url_start}{user_id}{base_url_end}"
        complete_urls.append(complete_url)

    return complete_urls

def main():
    # Načtení přihlašovacích údajů z JSON souboru
    with open("credentials.json") as f:
        credentials = json.load(f)
    
    username = credentials["username"]
    password = credentials["password"]
    link = credentials["link"]
    base_url_start = credentials["base_url_start"]
    base_url_end = credentials["base_url_end"]

    driver = Chrome()
    driver.get(link)

    # Přihlášení pomocí Selenium
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.submit()

    complete_urls = user_id(base_url_start, base_url_end, driver)

    # Inicializace finálních datových struktur
    final_data = {
        "projectfinances": [],
        "projectfinancetypes": [],
        "projectfinancecategories": []
    }
    #Kontrola, zda "projectfinancecategories" klíč existuje a není prázdný
    seen_financetype_ids = set()
    for url in complete_urls:
        data = get_data(url, driver,seen_financetype_ids)
        final_data["projectfinances"].extend(data.get("projectfinances", []))
        final_data["projectfinancetypes"].extend(data.get("projectfinancetypes", []))
        final_data["projectfinancecategories"].extend(data.get("projectfinancecategories", []))
    
    # Výpis a uložení finálních dat do JSON souboru
    # print(final_data)

    with open("dataX.json", "w", encoding='utf-8') as result_file:
        json.dump(final_data, result_file, indent=4, ensure_ascii=False)

    driver.quit()

if __name__ == '__main__':
    main()
