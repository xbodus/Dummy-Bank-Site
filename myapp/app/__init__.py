from flask import Flask, session
from flask_mysqldb import MySQL
from config import Config

mysql = MySQL()

def create_app():
        app = Flask(__name__)

        app.config.from_object(Config)

        mysql.init_app(app)
        
        from app import routes  # Import routes after app is created
        app.register_blueprint(routes.main)
        app.register_blueprint(routes.auth)

        @app.context_processor
        def inject_user():
                username = session.get('username')
                return {'injected_user': username}
        
        return app
