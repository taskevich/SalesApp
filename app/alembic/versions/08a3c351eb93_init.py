"""init

Revision ID: 08a3c351eb93
Revises: 
Create Date: 2025-03-18 06:39:46.150567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text

# revision identifiers, used by Alembic.
revision: str = '08a3c351eb93'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


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


def downgrade() -> None:
    op.drop_table("category")
    op.drop_table("product")
    op.drop_table("sale")
