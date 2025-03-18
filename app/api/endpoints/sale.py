from flask import Blueprint, request
from sqlalchemy import select, func, desc
from app.models.database.base import create_session, Sale, Product, Category
from app.models.dto.products import TotalSalesResponseDTO, TopSalesResponseDTO, TopSaleDTO
from app.utils.database_utils import time_range_condition_builder

sale_api = Blueprint("sale", __name__, url_prefix="/api/sales")


@sale_api.get("/total")
def get_total_sales():
    """
    Роут для получения общей суммы продаж.
    """
    with create_session() as session:
        condition = Sale.id != None
        start_date = request.args.get("start_date", None)
        end_date = request.args.get("end_date", None)
        condition = time_range_condition_builder(condition, start_date, end_date)
        stmt = select(func.sum(Sale.total_sold))
        total = session.execute(stmt.where(condition)).scalar()
        return TotalSalesResponseDTO(total=total).model_dump()


@sale_api.get("/top-products")
def get_top_products():
    """
    Роут для получения самых продаваемых товаров.
    """
    with create_session() as session:
        stmt = (
            select(
                Product.id,
                Product.name,
                Category.name,
                func.sum(Sale.total_sold).label("total_sales")
            )
            .join(Product, Sale.product_id == Product.id)
            .join(Category, Product.category_id == Category.id)
            .group_by(Product.id, Product.name, Category.name)
            .order_by(desc("total_sales"))
        )

        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        if start_date or end_date:
            stmt = stmt.where(time_range_condition_builder(Sale.sold_at, start_date, end_date))

        limit = request.args.get("limit")
        if limit:
            stmt = stmt.limit(int(limit))

        result = session.execute(stmt).all()

        return TopSalesResponseDTO(
            topSaleProducts=[
                TopSaleDTO(
                    id=id,
                    name=name,
                    category=category,
                    total=total_sales
                )
                for id, name, category, total_sales in result
            ]
        ).model_dump()
