import json
import re
import uuid
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def get_driver():
    options = ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    return Chrome(options=options)


def get_data(url, driver, external_ids, reqid_mappings, financetype_id_map):
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    reqid, proid = extract_ids_from_scripts(soup)
    inner_id = map_proid_to_inner_id(proid, external_ids)
    reqid_inner_id = map_reqid(reqid, reqid_mappings)

    name, amount = extract_project_details(soup)
    financetype_name = extract_financetype_name(soup)
    financetype_id = financetype_id_map.get(financetype_name, "unknown")

    project_finances = [{
        "id": reqid_inner_id,  # Change id to reqid_inner_id
        "project_id": inner_id,
        "amount": amount,
        "name": name,
        "financetype_id": financetype_id
    }] if reqid and inner_id else []

    return {
        "projectfinances": project_finances
    }


def extract_ids_from_scripts(soup):
    script_elements = soup.find_all('script', type='text/javascript')
    for script in script_elements:
        script_text = script.get_text(strip=True)
        reqid_match = re.search(r"vav\.reqid\s*=\s*'(\d+)'", script_text)
        proid_match = re.search(r"vav\.proid\s*=\s*'(\d+)'", script_text)
        if reqid_match and proid_match:
            return reqid_match.group(1), proid_match.group(1)
    return None, None


def map_proid_to_inner_id(proid, external_ids):
    for external_id in external_ids:
        if proid == external_id["outer_id"]:
            return external_id["inner_id"]
    return None


def map_reqid(reqid, reqid_mappings):
    reqid_inner_id = str(uuid.uuid4())
    id = str(uuid.uuid4())
    reqid_mappings.append({
        "id": id,
        "inner_id": reqid_inner_id,
        "outer_id": reqid
    })
    return reqid_inner_id


def extract_project_details(soup):
    amount = extract_text_from_sibling(soup, 'td', 'Předpokládaná hodnota veřejné zakázky v Kč s DPH')
    name = extract_text_from_sibling(soup, 'td', 'Název') or extract_text_from_sibling(soup, 'td', 'Název akce')
    return name, amount


def extract_text_from_sibling(soup, tag, string):
    element = soup.find(tag, class_='head', string=string)
    if element:
        sibling = element.find_next_sibling('td', class_='left-align')
        if sibling:
            return sibling.get_text(strip=True).replace('&nbsp;', '').replace(' ', '').replace(',', '.')
    return None


def extract_financetype_name(soup):
    h1_element = soup.find('h1')
    if h1_element:
        h1_text = h1_element.get_text(strip=True)
        return h1_text.split('#')[0].strip() if "#" in h1_text else h1_text.strip()
    return None


def user_id(base_url_start, base_url_end):
    with open('user_ids_test.txt', 'r') as file:
        user_ids = file.readlines()
    return [f"{base_url_start}{user_id.strip()}{base_url_end}" for user_id in user_ids]


def load_existing_data(filepath):
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {
            "projectfinances": [],
            "projectfinancetypes": [],
            "externalids": [],
            "reqidmappings": []
        }


def save_data(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as result_file:
        json.dump(data, result_file, indent=4, ensure_ascii=False)


def main():
    with open("credentials.json") as f:
        credentials = json.load(f)

    existing_data = load_existing_data('dataX.json')
    external_ids = existing_data.get("externalids", [])
    reqid_mappings = existing_data.get("reqidmappings", [])
    financetype_id_map = {item["name"].strip(): item["id"] for item in existing_data["projectfinancetypes"]}

    driver = get_driver()
    driver.get(credentials["link"])

    driver.find_element(By.NAME, "username").send_keys(credentials["username"])
    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys(credentials["password"])

    # Submit the login form
    password_field.submit()  # Submitting the form by submitting the password field

    complete_urls = user_id(credentials["base_url_start"], credentials["base_url_end"])

    final_data = {
        "projectfinances": []
    }

    for url in complete_urls:
        data = get_data(url, driver, external_ids, reqid_mappings, financetype_id_map)
        final_data["projectfinances"].extend(data.get("projectfinances", []))

    # Filter out reqidmappings with outer_id as None
    final_reqidmappings = [mapping for mapping in reqid_mappings if mapping["outer_id"] is not None]

    # Update projectfinances ids to inner_ids
    reqid_to_inner_id = {mapping["outer_id"]: mapping["inner_id"] for mapping in final_reqidmappings}
    for finance in final_data["projectfinances"]:
        if finance["id"] in reqid_to_inner_id:
            finance["id"] = reqid_to_inner_id[finance["id"]]

    existing_data["projectfinances"].extend(final_data["projectfinances"])
    existing_data["reqidmappings"] = final_reqidmappings

    save_data('dataX.json', existing_data)
    driver.quit()


if __name__ == '__main__':
    main()








