from flask import Flask

from app.api.endpoints.product import product_api
from app.api.endpoints.sale import sale_api


def create_app():
    app = Flask(__name__)
    app.register_blueprint(product_api)
    app.register_blueprint(sale_api)
    return app


app = create_app()
