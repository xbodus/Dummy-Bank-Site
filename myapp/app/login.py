import os
import json
import mysql.connector
from urllib.parse import parse_qs

def login(environ, sessions, start_response):
    """Create DB connection and check if login information is in the database"""
    request_body_size = int(environ.get("CONTENT_LENGTH", 0))
    request_body = environ["wsgi.input"].read(request_body_size)
    form_data = json.loads(request_body.decode("utf-8"))
 
    username = form_data.get("username")
    password = form_data.get("password")

    try:
        conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="P@ssw0rd",
                database="honeypot",
                ssl_disabled=True
            )

        cursor = conn.cursor()
        sql = "SELECT * FROM bau_users WHERE username=%s AND password=%s"
        cursor.execute(sql, (username, password))
        
        user = cursor.fetchall()

        if user:
            session_id = os.urandom(16).hex()
            sessions[session_id] = {'username': username}
            response = {"message": "User Authorized"}
            headers = [('Set-Cookie', f'session_id={session_id}; Path=/')]
            start_response('302 Found', headers + [('Content-Type', 'application/json')])
            return [json.dumps(response).encode("utf-8")]
        else:
            # Invalid credentials
            response = {"message": "Credentials Invalid"}
            start_response('401 Unauthorized', [('Content-Type', 'application/json')])
            return [json.dumps(response).encode("utf-8")]

    except Exception as e:
        # Handle database connection or cursor issues
        response = {"error": str(e)}
        start_response('500 Internal Server Error', [('Content-Type', 'application/json')])
        return [json.dumps(response).encode("utf-8")]

    finally:
        # Ensure proper closure of resources
        if cursor:
            cursor.close()
        if conn:
            conn.close()
