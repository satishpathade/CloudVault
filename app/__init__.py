import os
from flask import Flask

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.join(BASE_DIR, "templates"),
        static_folder=os.path.join(BASE_DIR, "static"),
        static_url_path="/static"
    )

    from app.routes.upload_routes import upload_bp
    app.register_blueprint(upload_bp)

    return app
