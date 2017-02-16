from flask import Flask, render_template, request, jsonify
import sqlite3
app = Flask(__name__)

connection = sqlite3.connect('database.db')
print('Opened database successfully')

connection.execute('')
print('Table created successfully')
connection.close()

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/enternew')
def enternew():
    return render_template('food.html')

@app.route('/addfood', methods = ['POST'])
def addfood():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        name = request.form['name']
        calories = request.form['calories']
        cuisine = request.form['cuisine']
        vegetarian = request.form['is_vegetarian']
        gluten_free = request.form['is_gluten_free']
        cursor.execute('INSERT INTO foods (name,calories,cuisine,is_vegetarian,is_gluten_free) VALUES (?,?,?,?,?)', (name,calories,cuisine,vegetarian,gluten_free))
        connection.commit()
        message = 'Food successfully posted'
    except:
        connection.rollback()
        message = 'Error in insert operation :('
    finally:
        return render_template('result.html', message = message)
        connection.close()

@app.route('/favorite', methods =['GET'])
def favorite():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM foods WHERE name = "Banana"')
    data = cursor.fetchall()
    return jsonify(data)

@app.route('/search', methods = ['GET'])
def search():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        name = (request.args.get('name'),)
        cursor.execute('SELECT * FROM foods WHERE name =?', name)
        connection.commit()
        data = cursor.fetchall()
    except:
        connection.rollback()
        data = 'Database Error'
    finally:
        return jsonify(data)
        connection.close()

@app.route('/drop')
def drop():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    try:
        cursor.execute('DROP TABLE foods')
        connection.commit()
        message = 'Table "foods" dropped'
    except:
        connection.rollback()
        message = 'Error; table not dropped'
    finally:
        return render_template('result.html', message = message)
        connection.close()
