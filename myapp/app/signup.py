import mysql.connector
import json

def signup(environ):
    try: 
        request_body_size = int(environ.get("CONTENT_LENGTH", 0))
        request_body = environ["wsgi.input"].read(request_body_size)
        data = json.loads(request_body.decode("utf-8"))
        
        email = data.get("email")
        username = data.get("username")
        password = data.get("password")

        conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="P@ssw0rd",
                database="honeypot",
                ssl_disabled=True
            )

        cursor = conn.cursor()
        sql = "INSERT INTO bau_users (username, password, email) VALUES (%s, %s, %s)"
        cursor.execute(sql, (username, password, email))
        conn.commit()

        cursor.close()
        conn.close()

        response = {"message": "User created successfully"}
        
    except mysql.connector.IntegrityError:
        response= {"error": "Username already exists"}

    except Exception as e:
        response = {"error": str(e)}

    body = json.dumps(response)
    return body
