from pydantic import BaseModel, Field


class CategoryDTO(BaseModel):
    id: int = Field(exclude=True)
    name: str


class ProductDTO(BaseModel):
    id: int = Field(exclude=True)
    name: str = Field()
    category: CategoryDTO


class ProductsResponseDTO(BaseModel):
    products: list[ProductDTO] = Field(default_factory=list)
