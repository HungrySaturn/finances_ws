import asyncio
import os
import json
from endpointFiller.insert_projectfinances import insertProjectFinances
from endpointFiller.insert_financetypes import insertFinanceTypes
from config import BASE_DIR



async def fillendpoint(base_folder):
    # Load the systemdata.json file
    with open(os.path.join(base_folder, 'dataX.json'), 'r', encoding='utf-8') as file:
        system_data = json.load(file)
    
    # Insert projects
    for projectfinances in system_data['projectfinances']:
        result = await insertProjectFinances(
            request_id=projectfinances['id'],
            project_id=projectfinances['project_id'],
            amount=projectfinances['amount'],
            name=projectfinances['name'],
            financetype_id=projectfinances['financetype_id']
        )
        if result is None:
            continue  # Skip to the next project if there's a duplicate key error

 # Insert financetypes
    for projectfinancetypes in system_data['projectfinancetypes']:
        result = await insertFinanceTypes(
            financetype_id=projectfinances['id'],
            financetype_name=projectfinances['name'],
        )
        if result is None:
            continue  # Skip to the next project if there's a duplicate key error

if __name__ == "__main__":
    asyncio.run(fillendpoint(base_folder=BASE_DIR))
