from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the CSV file into a DataFrame
df = pd.read_csv('../../data/transactions.csv')
records = df.to_dict('records')
current_record = -1

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

if __name__ == '__main__':
    app.run(debug=True)
