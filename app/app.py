from flask import Flask

from app.api.endpoints.product import product_api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(product_api)
    return app


app = create_app()
