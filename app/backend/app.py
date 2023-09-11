from dotenv import load_dotenv
from flask import Flask, jsonify, request
import pandas as pd
from flask_cors import CORS
import logging
import csv
import openai
import os
from prompts.prompts import generate_prompt

load_dotenv('../../')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

app = Flask(__name__)
CORS(app)

# Load the CSV file into a DataFrame
df = pd.read_csv('./data/transactions.csv')
records = df.to_dict('records')
current_record = -1

def read_records_from_csv():
    records = {}
    
    try:
        
        with open('labeled_data/labels.csv', 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                
                logging.info(row[0], row[1])
                if len(row) >= 2:
                    logging.debug(row)
                    records[row[0]] = row[1]
    except FileNotFoundError:
        pass
    return records

def write_records_to_csv(records):
    with open('labeled_data/labels.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for record_id, label in records.items():
            writer.writerow([record_id, label])

@app.route('/get_prediction', methods=['POST'])
def get_prediction():
    description = request.form.get('description')
    categories = request.form.get('categories')
    prompt = generate_prompt(description, categories)

    openai.api_key = os.getenv("OPENAI_API_KEY")
    prediction = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=7,
        temperature=0
    )

    return prediction

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
    label = request.form.get('label')
    logging.info('This is an info message')
    if record_id and label:
        # Read existing records from the CSV file
        records = read_records_from_csv()
        logging.info(f"*****records: {records}******")
        
        # if records[record_id]
        # Add or update the record in the dictionary
        records[record_id] = label
        
        # Write the updated records back to the CSV file
        write_records_to_csv(records)

        # Write 'id' and 'label' to a file on the disk
        
        return jsonify(status='success', message=f'{record_id,label}Record added/updated successfully'), 200
    else:
        return jsonify(status='failure', message='Invalid input'), 400

if __name__ == '__main__':
    app.run(debug=True)
