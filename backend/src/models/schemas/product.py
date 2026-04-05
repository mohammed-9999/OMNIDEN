from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.models.enums.product_enums import ProductCategory, Currency, ProductCondition

class ReviewSummary(BaseModel):
    """Data for the Ranking Agent to assess 'Social Proof'"""
    average_rating: float = Field(0.0, ge=0, le=5)
    review_count: int = Field(0, ge=0)
    top_positive_snippet: Optional[str] = None
    top_negative_snippet: Optional[str] = None
    has_verified_purchases: bool = False

class ShippingInfo(BaseModel):
    """Data for calculating 'Total Cost' and 'Urgency'"""
    cost: float = Field(0.0, ge=0)
    currency: Currency = Field(..., description="The currency extracted from the page")
    estimated_delivery_days: Optional[int] = None
    is_free_shipping: bool = False
    ships_to_morocco: bool = True # todo : this should be a list of the countries that the product can ship into

class Product(BaseModel):
    """
    The Core Omniden Product Model.
    Designed for multi-agent processing (Harvester -> Ranker).
    """
    # 1. Identity & Tracking (Rule 6: Idempotency)
    id: str = Field(..., description="SHA-256 hash of the source_url")
    source_name: str = Field(..., description="e.g., Amazon, Jumia, Avito")
    source_url: HttpUrl
    model_number: Optional[str] = None
    
    # 2. Commercial Data
    title: str = Field(..., min_length=2)
    price: float = Field(..., gt=0)
    currency: Currency = Field(..., description="The currency extracted from the page")
    condition: ProductCondition = ProductCondition.NEW # todo : here the condition should be written by the model but it has to be written in a unified format as the currency , they will be defined in a file as rules after to give along the prompt
    is_available: bool = True  
    
    # 3. Deep Metadata (For the Ranking Agent)
    category: ProductCategory = ProductCategory.OTHER  # todo : here the product category should be written by the model but it has to be written in a unified format as the currency , they will be defined in a file as rules after to give along the prompt  
    specifications: Dict[str, Any] = Field(
        default_factory=dict, 
        description="Technical specs like 'RAM', 'Storage', 'Color'"
    )
    reviews: ReviewSummary
    shipping: ShippingInfo
    
    # 4. Visuals & UI
    image_urls: List[HttpUrl] = Field(default_factory=list)
    brand: Optional[str] = None
    
    # 5. AI Internal Metadata (Rule 1)
    extraction_confidence: float = Field(..., ge=0, le=1)
    raw_relevance_score: float = Field(0.0, description="Initial match score from Agent 1")
    extracted_at: datetime = Field(default_factory=datetime.utcnow)

class ProductListResponse(BaseModel):
    """Standardized wrapper for the 'Search' endpoint"""

    query_hash: str
    provider: str = "Gemini-1.5-Flash"  # todo : this one has to be defined in .env file 
    items: List[Product]