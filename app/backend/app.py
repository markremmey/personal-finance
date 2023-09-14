import azure.cosmos.exceptions as exceptions
from azure.cosmos import CosmosClient, PartitionKey

from dotenv import load_dotenv
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import logging
import csv
import openai
import os
from prompts.prompts import generate_messages

openai.api_type = "azure"
openai.api_base = "https://remmey-aoai.openai.azure.com/"
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("AZ_OPENAI_API_KEY")


load_dotenv('../../.env')

ENDPOINT = os.getenv("COSMOSDB_ENDPOINT")
KEY = os.getenv("COSMOSDB_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")
CONTAINER_ID = os.getenv("CONTAINER_ID")


client = CosmosClient(url=ENDPOINT, credential=KEY)
database = client.create_database_if_not_exists(id=DATABASE_ID)
container = database.create_container_if_not_exists(
    id=CONTAINER_ID, partition_key='/id', offer_throughput=400
)

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.debug("***Starting Debugger**")

import subprocess

# result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)



app = Flask(__name__)
CORS(app)

# Load the CSV file into a DataFrame
df = pd.read_csv("./data/transactions.csv") #C:\\Users\\markremmey\\sandbox\\personal_finance\\app\\backend\\data\\transactions.csv
records = df.to_dict('records')
current_record = -1

def write_records_to_csv(records):
    with open('labeled_data/labels.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for record_id, label in records.items():
            writer.writerow([record_id, label])

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
    global current_record
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
    app.run() #debug=True


    # print("Database\t", database.id

    # if record_id and label and description:
    #     # Check to see if the record_id exists in the CSV
        
    #     if record_id in 

    
    # if record_id and label:
    #     # Read existing records from the CSV file
    #     records = read_records_from_csv()
    #     logging.info(f"*****records: {records}******")
        
    #     # if records[record_id]
    #     # Add or update the record in the dictionary
    #     records[record_id] = label
        
    #     # Write the updated records back to the CSV file
    #     write_records_to_csv(records)

    #     # Write 'id' and 'label' to a file on the disk
    # def read_records_from_csv():
#     #function that reads the records from the CSV file and returns a dictionary
    
#     records = {}    
#     try:
        
#         with open('labeled_data/labels.csv', 'r') as f:
#             reader = csv.reader(f)
#             for row in reader:
                
#                 logging.info(row[0], row[1])
#                 if len(row) >= 2:
#                     logging.debug(row)
#                     records[row[0]] = row[1]
#     except FileNotFoundError:
#         pass
#     return records