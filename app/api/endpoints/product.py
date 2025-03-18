from flask import Blueprint, request
from sqlalchemy import select

from app.models.database.base import create_session, Product
from app.models.dto.products import ProductsResponseDTO, ProductDTO, CategoryDTO

product_api = Blueprint("product", __name__, url_prefix="/api/products")


@product_api.get("/")
def get_products():
    """
    Роут на получения списка всех продуктов.
    """
    with create_session() as session:
        products = session.execute(select(Product)).scalars().all()
        return ProductsResponseDTO(
            products=[
                ProductDTO(
                    id=product.id,
                    name=product.name,
                    category=CategoryDTO(
                        id=product.category.id,
                        name=product.category.name,
                    )
                )
                for product in products
            ],
        ).model_dump()


@product_api.post("/")
def create_product():
    """
    Роут для создание нового продукта.
    """
    return "OK"


@product_api.put("/<int:product_id>")
def update_product():
    """
    Роут для обновления продукта.
    """
    return "OK"


@product_api.delete("/<int:product_id>")
def delete_product(product_id: int):
    """
    Роут для удаления продукта
    """
    return "OK"
