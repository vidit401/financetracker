from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("SELECT * FROM transactions")
    transactions = c.fetchall()
    conn.close()
    return render_template('index.html', transactions=transactions)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    transaction_type = request.form['type']
    category = request.form['category']
    amount = request.form['amount']
    date = request.form['date']

    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, category, amount, date) VALUES (?, ?, ?, ?)",
              (transaction_type, category, amount, date))
    conn.commit()
    conn.close()
    return index()

@app.route('/clear_history', methods=['POST'])
def clear_history():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("DELETE FROM transactions")
    conn.commit()
    conn.close()
    return index()

@app.route('/data')
def data():
    conn = sqlite3.connect('transactions.db')
    c = conn.cursor()
    c.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    rows = c.fetchall()
    conn.close()

    types = [row[0] for row in rows]
    amounts = [row[1] for row in rows]
    return jsonify({'types': types, 'amounts': amounts})

if __name__ == '__main__':
    app.run(debug=True)