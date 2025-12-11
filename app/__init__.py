from flask import Flask
from flask_assets import Environment, Bundle


def create_app(config_name="development"):
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(f"app.config.{config_name.capitalize()}Config")

    assets = Environment(app)
    assets.directory = 'app/static'
    assets.url = '/static'
    
    scss = Bundle('scss/main.scss', filters='scss', output='css/main.css')
    assets.register('scss_all', scss)
    # Register blueprints here
    # from .routes.auth import auth_bp
    # app.register_blueprint(auth_bp)
    from .routes.home import home_bp
    app.register_blueprint(home_bp)

    return app
