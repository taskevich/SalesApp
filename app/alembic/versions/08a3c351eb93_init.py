"""init

Revision ID: 08a3c351eb93
Revises: 
Create Date: 2025-03-18 06:39:46.150567

"""
import datetime
import random
import sqlalchemy as sa

from typing import Sequence, Union
from alembic import op
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '08a3c351eb93'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

categories = ["Electronics", "Clothing", "Books"]
products = {
    "Electronics": ["Laptop", "Smartphone", "Tablet", "Smartwatch", "Camera"],
    "Clothing": ["T-shirt", "Jeans", "Jacket", "Sneakers", "Hat"],
    "Books": ["Novel", "Biography", "Science Fiction", "Mystery", "History"]
}


def upgrade() -> None:
    op.create_table(
        "category",
        sa.Column(
            "id",
            sa.Integer,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=32),
            nullable=False,
            unique=True,
        )
    )
    op.create_table(
        "product",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "name",
            sa.String(length=64),
            nullable=False,
            unique=False,
            index=True,
        ),
        sa.Column(
            "category_id",
            sa.Integer,
            sa.ForeignKey(
                "category.id",
                ondelete="CASCADE"
            ),
            nullable=False,
        )
    )
    op.create_table(
        "sale",
        sa.Column(
            "id",
            sa.BigInteger,
            primary_key=True,
            autoincrement=True,
            nullable=False,
        ),
        sa.Column(
            "product_id",
            sa.Integer,
            sa.ForeignKey(
                "product.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column(
            "total_sold",
            sa.Integer,
            server_default=text("0"),
        ),
        sa.Column(
            "sold_at",
            sa.DateTime,
            server_default=text("CURRENT_TIMESTAMP"),
            nullable=False,
        )
    )

    conn = op.get_bind()
    category_ids = {}
    for cat in categories:
        result = conn.execute(
            text("INSERT INTO category (name) VALUES (:name) RETURNING id"),
            {"name": cat}
        )
        category_ids[cat] = result.fetchone()[0]

    product_ids = {}
    for cat, prod_list in products.items():
        product_ids[cat] = []
        for prod in prod_list:
            result = conn.execute(
                text("INSERT INTO product (name, category_id) VALUES (:name, :category_id) RETURNING id"),
                {"name": prod, "category_id": category_ids[cat]}
            )
            product_ids[cat].append(result.fetchone()[0])

    for cat, prod_list in product_ids.items():
        for prod_id in prod_list:
            for month in range(6):
                date = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=30 * month)
                total_sold = random.randint(10, 100)
                conn.execute(text(
                    "INSERT INTO sale (product_id, total_sold, sold_at) VALUES (:product_id, :total_sold, :sold_at)"),
                    {"product_id": prod_id, "total_sold": total_sold, "sold_at": date}
                )


def downgrade() -> None:
    op.drop_table("category")
    op.drop_table("product")
    op.drop_table("sale")
