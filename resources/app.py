from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS preferences (id SERIAL PRIMARY KEY, question TEXT, answer TEXT, justification TEXT)''')
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
        X = df[['question', 'justification']]
        y = df['answer']

        # Combine question and justification into a single text feature
        X['text'] = X['question'] + " " + X['justification']

        # Vectorize the text data
        vectorizer = TfidfVectorizer()
        X_vec = vectorizer.fit_transform(X['text'])

        # Train the model
        model = RandomForestClassifier()
        model.fit(X_vec, y)

        # Save the model and vectorizer
        with open('model.pkl', 'wb') as f:
            pickle.dump(model, f)
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(vectorizer, f)

@app.route('/ask', methods=['GET'])
def ask_question():
    question = "Would you rather go skiing in France or sunbathing in Greece?"
    return jsonify({'question': question})

@app.route('/answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data['question']
    answer = data['answer']
    justification = data.get('justification', '')

    conn = psycopg2.connect(
        host="db",
        database="yourdatabase",
        user="yourusername",
        password="yourpassword"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO preferences (question, answer, justification) VALUES (%s, %s, %s)", (question, answer, justification))
    conn.commit()
    cursor.close()
    conn.close()

    train_model()

    return jsonify({'status': 'success'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    question = data['question']
    justification = data.get('justification', '')

    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    text = question + " " + justification
    text_vec = vectorizer.transform([text])

    prediction = model.predict(text_vec)

    return jsonify({'prediction': prediction[0]})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)