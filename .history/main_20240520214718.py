from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def get_data(url, driver)-> list:
    user_id()
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
    
    username = credentials["username"]
    password = credentials["password"]
    link = credentials["link"]
    #link2 = credentials["link2"]

    

    base_url_start = "https://vav.unob.cz/request/home/"
    base_url_end = "#tabs-request-index=3"

    driver = Chrome()
    driver.get(link)

    #print("Username:", username)
    #print("Password:", password)

    # Získání elementů pro jméno a heslo
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    # Vyplnění přihlašovacích údajů
    username_field.send_keys(username)
    password_field.send_keys(password)

    # Odeslání formuláře
    password_field.submit()

    complete_urls = user_id(base_url_start, base_url_end, driver)

    for url in complete_urls:
        print(url)

    #data = get_data(link2, driver)
 
    # Získání HTML obsahu stránky po přihlášení
    



    #with open("dataX.json", "w") as d:
    #    d.write(data)

    #print (page_source)


if __name__ == '__main__':
    main()
