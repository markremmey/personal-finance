import azure.cosmos.exceptions as exceptions
from azure.cosmos import CosmosClient, PartitionKey

from dotenv import load_dotenv
import os


load_dotenv('../../.env')
from azure.identity import DefaultAzureCredential

ENDPOINT = os.getenv("COSMOSDB_ENDPOINT")
KEY = os.environ.get("COSMOSDB_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")
CONTAINER_ID = os.getenv("CONTAINER_ID")

client = CosmosClient(url=ENDPOINT, credential=KEY)
db = client.get_database_client(database=DATABASE_ID)
container = db.get_container_client(CONTAINER_ID)

def retrieve_few_shots(categories):
    examples = []
    
    items = list(container.read_all_items(max_item_count=10))
    
    # Iterate over all JSONs in the Cosmos DB
    for item in items:
        print(item)
        print(item['description'])
        transaction = {item['description']}
        user_msg = f"""Classify the transaction based on a list of categories. Only respond with the category, nothing else.
        Categories: {categories}
        Transaction: {transaction}"""
        examples.append({"role": "user", "content": user_msg})
        examples.append({"role": "assistant", "content": f"{item['label']}"})
    return examples

def generate_messages(description, categories):

    
    system_prompt = "You are a bot that classifies credit card transactions into a number of predefined categories"

    user_msg = f"""Classify the transaction based on a list of categories. Only respond with the category, nothing else.
        Categories: {categories}
        Transaction: {description}"""
    mess = [{"role": "system", "content": system_prompt}]
    
    mess += retrieve_few_shots(categories)
    
    return mess


def generate_prompt(categories, transaction):
    prompt = f"""You are a bot that classifies credit card and bank transactions into a number of user-specified categories.

    Categories:
    {categories}

    Transaction:
    {transaction}

    Category:
"""
    
    return prompt