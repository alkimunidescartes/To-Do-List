import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Goal2012"
)
cursor = connection.cursor()

# Read SQL file
with open('setup.sql', 'r') as sql_file:
    sql_script = sql_file.read()

# Execute the SQL script
for statement in sql_script.split(';'):
    if statement.strip():
        cursor.execute(statement)

connection.commit()
connection.close()
print("Database and tables have been set up.")

def connect_to_db():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",  # Your MySQL username
        password="Goal2012",  # Your MySQL root password
        database="todo_list_db"  # The database you've set up
    )
    return connection