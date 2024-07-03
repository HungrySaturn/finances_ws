import aiohttp
import json
from config import DOMAIN, PORT




async def insertFinanceTypes(financetype_id, financetype_name):
    async with aiohttp.ClientSession() as session:
        url = f"{DOMAIN}:{PORT}/gql/"
    
        headers = {
            "Content-Type": "application/json",
        }

        # Define the mutation string
        query = f'''
        mutation insert {{
            financeTypeInsert(projectfinancetypes: {{
                id: "{financetype_id}",
                financetypeId: "{financetype_name}"
            }}) {{
                id
                msg
            }}
        }}
        '''

        data = json.dumps({"query": query, "operationName": "insert"})
        
        async with session.post(url, headers=headers, data=data) as response:
            if response.status != 200:
                raise Exception(f"GraphQL request failed with status code {response.status}")
            
            result = await response.json()
            print("GraphQL response for projectFinanceInsert:", result)  # Add this line for debugging
            
            if 'errors' in result:
                errors = result['errors']
                if isinstance(errors, list):
                    duplicate_key_error = any('duplicate key' in str(error).lower() for error in errors)
                    if duplicate_key_error:
                        print(f"Duplicate key error for project ID: {project_id}. Skipping...")
                        return None
                raise Exception(f"GraphQL errors: {result['errors']}")

            if 'data' in result and 'projectFinanceInsert' in result['data']:
                project_id = result["data"]["projectFinanceInsert"]["id"]
                return project_id
            else:
                raise Exception(f"Unexpected GraphQL response format: {result}")

