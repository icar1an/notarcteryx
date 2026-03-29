from fastapi import APIRouter, HTTPException

from app.models.domain import Product
from app.models.schemas import ProductListResponse, ProductResponse

router = APIRouter()

# Hardcoded product catalog — expand as needed
PRODUCTS: dict[str, Product] = {
    "bird-head-toque": Product(
        id="bird-head-toque",
        name="Bird Head Toque",
        category="Accessories",
        base_price=60.00,
        description="Warm, comfortable toque made from a blend of wool and recycled polyester.",
        colors=["Ether", "Arctic Silk", "Black"],
        image_url="/static/bird-head-toque.jpg",
    ),
    "beta-ar-jacket": Product(
        id="beta-ar-jacket",
        name="Beta AR Jacket",
        category="Shell Jackets",
        base_price=599.00,
        description="Versatile GORE-TEX shell for all-round use in severe weather.",
        colors=["Black", "Dynasty", "Solitude"],
        image_url="/static/beta-ar-jacket.jpg",
    ),
    "atom-hoody": Product(
        id="atom-hoody",
        name="Atom Hoody",
        category="Insulated Jackets",
        base_price=280.00,
        description="Lightweight, breathable insulated hoody with Coreloft compact insulation.",
        colors=["Black", "Forage", "Serene"],
        image_url="/static/atom-hoody.jpg",
    ),
}


def _to_response(p: Product) -> ProductResponse:
    return ProductResponse(
        id=p.id,
        name=p.name,
        category=p.category,
        base_price=p.base_price,
        description=p.description,
        colors=p.colors,
        image_url=p.image_url,
    )


@router.get("", response_model=ProductListResponse)
async def list_products():
    return ProductListResponse(
        products=[_to_response(p) for p in PRODUCTS.values()]
    )


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str):
    product = PRODUCTS.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return _to_response(product)
