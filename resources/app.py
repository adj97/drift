from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

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

    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)