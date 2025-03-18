from flask import Blueprint, request
from pydantic import ValidationError
from sqlalchemy import select, insert, update, delete

from app.models.database.base import create_session, Product
from app.models.dto.products import ProductsResponseDTO, ProductDTO, CategoryDTO, AddProductDTO, AddProductResponseDTO, \
    PatchProductDTO, PatchProductResponseDTO, DeleteProductResponseDTO

product_api = Blueprint("product", __name__, url_prefix="/api/products")


@product_api.get("/")
def get_products():
    """
    Роут на получения списка всех продуктов.
    """
    with create_session() as session:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))
        search = request.args.get("search", "")

        if offset < 0:
            offset = 0

        if limit < 0:
            limit = 1

        products = session.execute(
            select(Product)
            .where(Product.name.ilike(f"%{search}%"))
            .limit(limit)
            .offset(offset)
            .order_by(Product.id)
        ).scalars().all()
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
    try:
        product_dto = AddProductDTO(**request.json)
    except ValidationError as ex:
        return AddProductResponseDTO(
            error=True,
            message=str(ex),
        ).model_dump()
    with create_session() as session:
        session.execute(
            insert(Product).values({
                Product.name: product_dto.name,
                Product.category_id: product_dto.categoryId
            }).returning(Product.id)
        )
        session.commit()
    return AddProductResponseDTO(
        error=False,
        message="OK",
        payload=product_dto
    ).model_dump()


@product_api.put("/<int:product_id>")
def update_product(product_id: int):
    """
    Роут для обновления продукта.
    """
    try:
        patch_product = PatchProductDTO(**request.json)
    except ValidationError as ex:
        return PatchProductResponseDTO(
            error=True,
            message=str(ex)
        ).model_dump()
    with create_session() as session:
        session.execute(update(Product).values({
            Product.name: patch_product.name,
        }).where(
            Product.id == product_id
        ))
        session.commit()
    return PatchProductResponseDTO(
        error=False,
        message="OK",
        payload=patch_product
    ).model_dump()


@product_api.delete("/<int:product_id>")
def delete_product(product_id: int):
    """
    Роут для удаления продукта
    """
    with create_session() as session:
        if session.get(Product, product_id) is None:
            session.execute(delete(Product).where(
                Product.id == product_id
            ))
            session.commit()
            return DeleteProductResponseDTO(error=False, message="OK", payload=None).model_dump()
    return DeleteProductResponseDTO(error=True, message="Product doesn't exists", payload=None).model_dump()
