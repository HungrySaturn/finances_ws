from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

pip install beautifulsoup4 requests


def get_data(url, driver)-> list:
    
    driver.get(url)

    data = driver.page_source

    driver.quit()
    

    return data

def user_id(base_url_start, base_url_end, driver):
    with open('user_ids_test.txt', 'r') as file:
        user_ids = file.readlines()


    complete_urls = []
    for user_id in user_ids:
        complete_url = f"{base_url_start}{user_id}{base_url_end}"
        complete_urls.append(complete_url)

    return complete_urls


def main():
    with open("credentials.json") as f:
        credentials = json.load(f)
    
    #Příjem dat ze souboru credentials
    username = credentials["username"]
    password = credentials["password"]

    #Příjem dat ze souboru credentials
    link = credentials["link"]
    
    #Příjem dat ze souboru credentials
    base_url_start = credentials["base_url_start"]
    base_url_end = credentials["base_url_end"]

    #Nastavení driveru
    driver = Chrome()
    #Nastavení adresy pro přihlášení do systému
    driver.get(link)

    #Nalezení elementů jména a hesla
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    #Vyplnění přihlašovacích údajů
    username_field.send_keys(username)
    password_field.send_keys(password)

    #Odeslání formuláře
    password_field.submit()

    #Vyvolání funkce, která používá první i druhou část url adresy a driver
    complete_urls = user_id(base_url_start, base_url_end, driver)

    User_data = []
    for url in complete_urls:#Pro každou adresu v listu complete_urls vyvolá funkci get_data
        data = get_data(url, driver)
        User_data.append(data)
    
    print(User_data)

    #Zapíše výsledek do souboru dataX.json
    with open("dataX.json", "w") as vysledek:
        vysledek.write(str(User_data))

    #print (page_source)


if __name__ == '__main__':
    main()
