from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    error: bool
    message: str
    payload: Any


class CategoryDTO(BaseModel):
    id: int
    name: str


class ProductDTO(BaseModel):
    id: int
    name: str = Field()
    category: CategoryDTO


class ProductsResponseDTO(BaseModel):
    products: list[ProductDTO] = Field(default_factory=list)


class AddProductDTO(BaseModel):
    name: str
    categoryId: int


class AddProductResponseDTO(BaseResponse):
    payload: AddProductDTO | None = None


class PatchProductDTO(BaseModel):
    name: str


class PatchProductResponseDTO(BaseResponse):
    payload: PatchProductDTO | None = None


class DeleteProductResponseDTO(BaseResponse):
    pass


class TotalSalesResponseDTO(BaseModel):
    total: int


class TopSaleDTO(BaseModel):
    id: int
    name: str
    category: str
    total: int


class TopSalesResponseDTO(BaseModel):
    topSaleProducts: list[TopSaleDTO] = Field(default_factory=list)
