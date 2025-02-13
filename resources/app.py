from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = psycopg2.connect(
        host="db",
        database="yourdatabase",
        user="yourusername",
        password="yourpassword"
    )
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS preferences (id SERIAL PRIMARY KEY, question TEXT, answer TEXT)''')
    conn.commit()
    cursor.close()
    conn.close()

# Train the model
def train_model():
    conn = psycopg2.connect(
        host="db",
        database="yourdatabase",
        user="yourusername",
        password="yourpassword"
    )
    df = pd.read_sql_query("SELECT * FROM preferences", conn)
    conn.close()

    if not df.empty:
        X = df['question']
        y = df['answer']
        model = RandomForestClassifier()
        model.fit(X, y)
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)

@app.route('/ask', methods=['GET'])
def ask_question():
    question = "Would you rather go skiing in France or sunbathing in Greece?"
    return jsonify({'question': question})

@app.route('/answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data['question']
    answer = data['answer']

    conn = psycopg2.connect(
        host="db",
        database="yourdatabase",
        user="yourusername",
        password="yourpassword"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO preferences (question, answer) VALUES (%s, %s)", (question, answer))
    conn.commit()
    cursor.close()
    conn.close()

    train_model()

    return jsonify({'status': 'success'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    question = data['question']

    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([question])

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)