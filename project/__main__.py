from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from . import logger
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] = 'thisisPetStore'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config['DEBUG'] = True
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    from .models import Token
    from .models import Carts
    from .models import CartItems
    from .models import Transactions
    from .models import TransactionDetails
    
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))   

    #blueprint for auth routes in the app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    #blueprint for non auth routes in the app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    #blueprint for admin in the app
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)
    
    return app

def main():
    app = create_app()
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(7979)   
    IOLoop.instance().start()

if __name__ == "__main__":
    logger.info("Welcome to Petstore")
    main()
    