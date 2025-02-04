from flask import Flask, render_template, request, redirect, url_for
import snowflake.connector
import os

app = Flask(__name__)

# Load configuration from environment variables (for containerization)
SNOWFLAKE_ACCOUNT= "pigaxln-qmb03958"
SNOWFLAKE_USER= "JRK"
SNOWFLAKE_PASSWORD= "Jayaram@3"
SNOWFLAKE_DATABASE= "my_database"
SNOWFLAKE_SCHEMA= "my_schema"
SNOWFLAKE_WAREHOUSE= "my_warehouse"

# Function to connect to Snowflake
def get_snowflake_connection():
    return snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
        warehouse=SNOWFLAKE_WAREHOUSE
    )

# Home page - Fetch and display records
@app.route('/')
def index():
    conn = get_snowflake_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, age FROM users;")  # Modify as per your table
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', records=data)

# Update record in Snowflake
# @app.route('/update', methods=['POST'])
# def update_record():
#     record_id = request.form['id']
#     new_name = request.form['name']
#     new_age = request.form['age']

#     conn = get_snowflake_connection()
#     cursor = conn.cursor()
#     cursor.execute(f"UPDATE users SET name = '{new_name}', age = {new_age} WHERE id = {record_id};")
#     conn.commit()
#     cursor.close()
#     conn.close()

#     return redirect('/')

@app.route('/insert', methods=['POST'])
def insert_record():
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        # Check what data is being received
        print("Received Form Data:", request.form)

        record_id = request.form.get("id")
        new_name = request.form.get("name")
        new_age = request.form.get("age")

        # Debug: Print the SQL query
        insert_query = f"INSERT INTO USERS (ID, NAME, AGE) VALUES ('{record_id}', '{new_name}', '{new_age}');"
        print("Executing Query:", insert_query)

        # Execute update query
        cur.execute(insert_query)
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for("index"))
    
    except Exception as e:
        print("Error occurred:", e)
        return f"Update failed: {e}", 500

@app.route('/update', methods=['POST'])
def update_record():
    try:
        conn = get_snowflake_connection()
        cur = conn.cursor()

        # Check what data is being received
        print("Received Form Data:", request.form)

        record_id = request.form.get("id")
        new_name = request.form.get("name")
        new_age = request.form.get("age")

        # Debug: Print the SQL query
        update_query = f"UPDATE users SET name = '{new_name}', age = '{new_age}' WHERE id = '{record_id}';"
        print("Executing Query:", update_query)

        # Execute update query
        cur.execute(update_query)
        conn.commit()

        cur.close()
        conn.close()

        return redirect(url_for("index"))

    except Exception as e:
        print("Error occurred:", e)
        return f"Update failed: {e}", 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
