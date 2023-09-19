import azure.cosmos.exceptions as exceptions
from azure.cosmos import CosmosClient, PartitionKey
from azure.identity import DefaultAzureCredential

from dotenv import load_dotenv
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import logging
import openai
import os

current_directory = os.getcwd()
print("Current Directory:", current_directory)

from prompts.prompts import generate_messages

openai.api_type = "azure"
openai.api_base = "https://remmey-aoai.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("AZ_OPENAI_API_KEY")

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

load_dotenv('../../.env')

ENDPOINT = os.getenv("COSMOSDB_ENDPOINT")
KEY = os.getenv("COSMOSDB_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")
CONTAINER_ID = os.getenv("CONTAINER_ID")
BLOB_URL = os.getenv('BLOB_SAS_URL')
BLOB_CONTAINER = os.getenv('CONTAINER_NAME')
BLOB_CREDENTIAL = os.getenv('BLOB_SAS_TOKEN')

logging.info(f"*****\n\nBLOB_CONTAINER: {BLOB_CONTAINER}\n\n******")

client = CosmosClient(url=ENDPOINT, credential=KEY)
database = client.create_database_if_not_exists(id=DATABASE_ID)
container = database.create_container_if_not_exists(
    id=CONTAINER_ID, partition_key='/id', offer_throughput=400
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.debug("***Starting Debugger**")


app = Flask(__name__)
CORS(app)

# Load the CSV file into a DataFrame


@app.route('/upload_to_blob', methods=['POST'])
def upload_to_blob():
    # Get 'form_data' and upload to blob storage
    # request_data = request.get_json()
    file = request.files['file']
    app.logger.info("Received request with data: %s", file)
    app.logger.info("File Name: %s", file.filename)
    
    # logging.debug("*****request.form: ", request.form)
    # form_data = request.form.get('form_data')
    # logging.info("*****form_data: ", form_data)
    
    
    
    blobClient = BlobClient(account_url=BLOB_URL, 
                            container_name=BLOB_CONTAINER,
                            blob_name=file.filename)

    res = blobClient.upload_blob(file.read(), blob_type="BlockBlob")


    return jsonify({'message': 'File uploaded successfully'}), 200

@app.route('/get_prediction', methods=['POST'])
def get_prediction():
    description = request.form.get('description')
    categories = request.form.get('categories') #["Online Subscription", "CC_Payment", "Hardware", "Other"]
    messages = generate_messages(description, categories)
    logging.debug(f"***Messages: {messages}****")
    # print(f"*******messages: ****", messages)
    openai.api_key = os.getenv("AZ_OPENAI_API_KEY")
    response = openai.ChatCompletion.create(
                engine="chat",
                messages = messages,
                temperature=0.7,
                max_tokens=800,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None)
    logging.debug(f"***Response: {response}****")
    logging.debug(f"***response.choices: {response.choices[0].message.content}****")
    return jsonify(response.choices[0].message.content)

@app.route('/get_record', methods=['GET'])
def get_record():
    df = pd.read_csv("./personal_finance/app/data/transactions.csv") #C:\\Users\\markremmey\\sandbox\\personal_finance\\app\\backend\\data\\transactions.csv
    records = df.to_dict('records')
    current_record = -1
    
    # global current_record
    if current_record < len(records) - 1:
        current_record += 1
        records[current_record].pop('Labels')
        records[current_record].pop('Notes')
        return jsonify(records[current_record])
    else:
        return jsonify({"error": "No more records"}), 404
    
@app.route('/label_data', methods=['POST'])
def label_data():
    # Get 'id' and 'label' from the POST request
    record_id = request.form.get('id')
    description = request.form.get('description')
    label = request.form.get('label')
    logging.debug('Upserting labeled data into cosmos')    

    labeled_data = {
        "id": record_id,
        "description": description,
        "label": label
    }
    container.upsert_item(labeled_data)
        
    return jsonify(status='success', message=f'{record_id,label}Record added/updated successfully'), 200

if __name__ == '__main__':
    app.run(debug=True)
    #app.env = 'development'
    