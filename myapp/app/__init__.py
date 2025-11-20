from flask import Flask, session
from flask_login import LoginManager, UserMixin
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

mysql = MySQL()
login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def get_id(self):
        return str(self.id)


def create_app():
        app = Flask(__name__)

        app.config.from_object(Config)

        mysql.init_app(app)

        app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

        login_manager.init_app(app)
        login_manager.login_view = "/login"
        
        from app import routes  # Import routes after app is created
        app.register_blueprint(routes.main)
        app.register_blueprint(routes.auth)

        @app.context_processor
        def inject_user():
                username = session.get('username', None)
                app.config["USERNAME"] = username
                return {'injected_user': username}
        
        return app

@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor(DictCursor)

    cursor.execute("SELECT user_id, username FROM users WHERE user_id=%s", (user_id,))
    user = cursor.fetchone()

    cursor.close()

    if user:
        return User(user["user_id"], user["username"])


    return None