from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import Integer, String, BigInteger, ForeignKey, DateTime, text, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker, relationship

from app.core.config import settings


class Base(DeclarativeBase):
    pass


class Category(Base):
    __tablename__ = "category"
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
    )


class Product(Base):
    __tablename__ = "product"
    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        unique=False,
        index=True,
    )
    category_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "category.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    category: Mapped[Category] = relationship("Category")


class Sale(Base):
    __tablename__ = "sale"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "product.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )
    sold_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

    product = relationship("Product")


engine = create_engine(
    url=settings.get_dbs(),
    pool_recycle=3600,
    pool_size=10,
    max_overflow=25
)
session_maker = sessionmaker(bind=engine)


# Понимаю, что у flask есть app_context, но
# думаю лучше, когда все интуитивно и понятно.
@contextmanager
def create_session():
    """
    Открытие сессии.
    """
    with session_maker() as session:
        try:
            yield session
        except Exception:
            session.rollback()
        finally:
            session.close()
