import logging
import os
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection
MONGODB_URL = os.environ.get("MONGODB_URL", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGODB_URL)
db = client.ecommerce

# Create FastAPI app
app = FastAPI(
    title="E-Commerce API",
    description="E-Commerce API with FastAPI and MongoDB",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/", include_in_schema=False)
async def root() -> Dict[str, str]:
    return {
        "message": "Welcome to E-Commerce API!",
        "docs_url": "/api/docs",
        "health_endpoint": "/health"
    }

# Health check
@app.get("/health", include_in_schema=False)
async def health() -> Dict[str, str]:
    return {"status": "healthy"}

# Product endpoints
@app.post("/api/v1/products", status_code=201)
async def create_product(product: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new product."""
    # Add timestamp
    from datetime import datetime
    product["created_at"] = datetime.utcnow()
    product["updated_at"] = datetime.utcnow()
    
    # Insert into database
    result = await db.products.insert_one(product)
    
    # Return created product
    created_product = await db.products.find_one({"_id": result.inserted_id})
    if created_product:
        created_product["id"] = str(created_product.pop("_id"))
        return created_product
    
    raise HTTPException(status_code=500, detail="Failed to create product")

@app.get("/api/v1/products")
async def list_products(
    category: Optional[str] = None,
    brand: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    size: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 10,
    skip: int = 0
) -> Dict[str, Any]:
    """Get a list of products with optional filtering."""
    # Build query
    query = {}
    
    if category:
        query["category"] = category
    if brand:
        query["brand"] = brand
    if min_price is not None:
        query.setdefault("price", {})["$gte"] = min_price
    if max_price is not None:
        query.setdefault("price", {})["$lte"] = max_price
    if size:
        query["sizes.size"] = size
    if search:
        query["$or"] = [
            {"name": {"$regex": search, "$options": "i"}},
            {"description": {"$regex": search, "$options": "i"}},
        ]
    
    # Get total count
    total_count = await db.products.count_documents(query)
    
    # Get products
    cursor = db.products.find(query).skip(skip).limit(limit)
    products = []
    async for product in cursor:
        product["id"] = str(product.pop("_id"))
        products.append(product)
    
    # Return paginated response
    return {
        "items": products,
        "total": total_count,
        "limit": limit,
        "skip": skip
    }

@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: str) -> Dict[str, Any]:
    """Get a product by ID."""
    from bson import ObjectId
    
    # Validate ObjectId
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="Invalid product ID")
    
    # Get product
    product = await db.products.find_one({"_id": ObjectId(product_id)})
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Convert _id to string
    product["id"] = str(product.pop("_id"))
    
    return product 