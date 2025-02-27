from flask import Flask, render_template, jsonify, url_for
from flask_pymongo import PyMongo
from flask_mysqldb import MySQL
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = getenv('MONGO_URI')
mongo = PyMongo(app)

motos_collection = mongo.db.motos

app.config['MYSQL_HOST'] = getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = getenv('MYSQL_DB')

mysql = MySQL(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/motos_mongodb')
def motos_mongodb():
    motos_mongodb = motos_collection.find()
    return jsonify(motos_mongodb)


@app.route('/motos_mysql')
def motos_mysql():
    cursor = mysql.connection.cursor()
    sql = "SELECT * FROM motos;"
    cursor.execute(sql)
    data = cursor.fetchall()
    motos = []
    for row in data:
        moto = {
            'id': row[0],
            'marca': row[1],
            'modelo': row[2],
            'color': row[3],
            'cilindrada': row[4]
        }
        motos.append(moto)

    return jsonify(motos)



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)