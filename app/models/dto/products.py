from typing import Any

from pydantic import BaseModel, Field


class BaseResponse(BaseModel):
    error: bool
    message: str
    payload: Any


class CategoryDTO(BaseModel):
    id: int = Field(exclude=True)
    name: str


class ProductDTO(BaseModel):
    id: int = Field(exclude=True)
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
