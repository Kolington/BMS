#Budget Managment System

#Process 1 -- Importing the necessary libraries
from flask import Flask, render_template, request, make_response
import sqlite3
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
import getpass 
import hashlib


#Security -- Encryption 2
import hashlib
string = "supremeadmin"
stringtwo = "moneyauthority"
stringthree = "secondauthority"

hashlib.sha256(string.encode()).hexdigest()
hashlib.sha256(stringtwo.encode()).hexdigest()
hashlib.sha256(stringthree.encode()).hexdigest()

#Security -- User Authentication
    

#Process 2 -- Database Creation Creating a SQLite database to store transactions.
# Create a connection to the database
conn = sqlite3.connect('transactions.db')

# Create a cursor
cursor = conn.cursor()

# Create the transactions table
cursor.execute('''CREATE TABLE transactions
                  (id INTEGER PRIMARY KEY AUTOINCREMENT
                   date TEXT NOT NULL, 
                   description TEXT, 
                   amount REAL, 
                   category TEXT);''')

conn.commit()
conn.close()

#Process 3 -- Importing Data From CSV -- For demo purposes, use a CSV file to simulate bank transactions. Import this file into a Pandas DataFrame, then convert it into a SQLite database.
# Connect to SQLite database
conn = sqlite3.connect('transactions.db')

df = pd.read_csv('Transactions.csv')
df.to_sql('transactions', conn, if_exists='replace', index = False)

# Close the database connection
conn.close()

#Process 4 -- Clustering Transactions -- using a simple K Means clustering algorithm from sklearn to cluster similar transactions.
# load transactions into csv
df = pd.read_csv('transactions.csv')

# Initialize the Count Vectorizer
cv = CountVectorizer()

# Fit and transform the processed titles
vector = cv.fit_transform(df['Description'].values.astype('U'))

#kmeans = KMeans(n_clusters = 6, init = 'k-means++', max_iter = 300, n_init = 10, random_state = 0)
y_kmeans = kmeans.fit_predict(vector)

df['Category'] = y_kmeans

#Process 5 -- Building the Flask App & In the Flask app, we'll have two routes - one for viewing transactions and one for adding transactions.
app = Flask(__name__)

def connect_db(): 
    return sqlite3.connect('transactions.db')    

@app.route('/')
#def create_table():
    
def index(): 
    #return render_template("index.html")
    response = make_response(render_template('index.html', foo=405))

def login_signup():
    conn = sqlite3.connect('transactions.db')
    cursor = conn.cursor()
    
    import getpass

    database = {"super_admin": "supremeadmin", "super_accountant": "moneyauthority", "asst_accountant": "secondauthority"}

    username = input("Enter Your Username : ").lower()
    password = getpass.getpass("Enter Your Password : ").lower()

    for key in database.keys():
        if username == key:
            while password != database.get(key):
                password = getpass.getpass("Re-enter Your Password : ")
            break
    print("User Verified")
    
    conn.commit()
    conn.close()
    return render_template("login.html")
    
def view_transactions():
    conn = sqlite3.connect('transactions.db')
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return render_template("index.html", tables=[df.to_html(classes='data')], titles=df.columns.values)

@app.route('/add_transaction', methods = ['POST'])
def add_transaction():
    date = request.form['date']
    description = request.form['description']
    amount = request.form['amount']
    category = request.form['category']
    
    #conn = sqlite3.connect('transactions.db')
    #cursor = conn.cursor()
    cursor.execute("INSERT INTO transactions (date, description, amount, category) VALUES (?,?,?,?)", (request.form['date'], request.form['description'], request.form['amount'], request.form['category']))
    conn.commit()
    
    conn.close()
    return make_response('Success', 200)

if __name__ == '__main__':
    app.run()
    app.run(debug=True)
    
#Security -- 2FA -- Google Authenticator
