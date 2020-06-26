from flask import Flask
from flask_cors import CORS
from authlib.integrations.flask_client import OAuth
from models import setup_db

cors = CORS()
oauth = OAuth()


def create_app(config_class=None):
    app = Flask(__name__)
    # app.config.from_object(config_class)
    cors.init_app(app)
    oauth.init_app(app)
    setup_db(app)

    from auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api')

    from casting import bp as casting_bp
    app.register_blueprint(casting_bp, url_prefix='/api')

    from errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
