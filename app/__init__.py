from flask import Flask
from flask_assets import Environment, Bundle
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name="development"):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")
    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    
    from app.models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    assets = Environment(app)
    assets.directory = 'app/static'
    assets.url = '/static'
    
    scss = Bundle('scss/main.scss', filters='libsass', output='css/main.css')
    assets.register('scss_all', scss)
    # Register blueprints here
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)
    from .routes.home import home_bp
    app.register_blueprint(home_bp)

    return app
