from django.apps import AppConfig


class MyappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myApp'
from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import Error
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database connection details
DB_NAME = 'your_dbname'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_HOST = 'your_host'
DB_PORT = 'your_port'

def create_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

@app.route('/registrations', methods=['POST'])
def create_registration():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    dob = data.get('dob')

    if not name or not email or not dob:
        return jsonify({"error": "Name, email, and date of birth are required"}), 400

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Registration (Name, Email, DateOfBirth) VALUES (%s, %s, %s)",
            (name, email, dob)
        )
        conn.commit()
        return jsonify({"message": "Registration created successfully"}), 201
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/registrations', methods=['GET'])
def get_registrations():
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Registration")
        registrations = cursor.fetchall()
        result = []
        for row in registrations:
            result.append({
                "ID": row[0],
                "Name": row[1],
                "Email": row[2],
                "DateOfBirth": row[3],
                "RegistrationDate": row[4]
            })
        return jsonify(result), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/registrations/<int:id>', methods=['PUT'])
def update_registration(id):
    data = request.json
    name = data.get('name')
    
    if not name:
        return jsonify({"error": "Name is required"}), 400

    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Registration SET Name = %s WHERE ID = %s",
            (name, id)
        )
        conn.commit()
        return jsonify({"message": "Registration updated successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@app.route('/registrations/<int:id>', methods=['DELETE'])
def delete_registration(id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Registration WHERE ID = %s", (id,))
        conn.commit()
        return jsonify({"message": "Registration deleted successfully"}), 200
    except Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
