from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid


class PriceHistoryEntry(BaseModel):
    date: datetime
    price: float
    source: str


class Listing(BaseModel):
    platform: str  # "eBay", "Poshmark", "Etsy", "JamesAvery"
    price: float
    url: str
    condition: str
    seller: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)


class Charm(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    material: str  # "Silver", "Gold", "Mixed"
    status: str  # "Active", "Retired"
    is_retired: bool
    avg_price: float
    price_history: List[PriceHistoryEntry] = []
    price_change_7d: float
    price_change_30d: float
    price_change_90d: float
    popularity: int  # 0-100
    images: List[str]
    listings: List[Listing] = []
    related_charm_ids: List[str] = []
    last_updated: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class CharmCreate(BaseModel):
    name: str
    description: str
    material: str
    status: str
    is_retired: bool
    avg_price: float
    price_change_7d: float
    price_change_30d: float
    price_change_90d: float
    popularity: int
    images: List[str]


class CharmResponse(BaseModel):
    id: str
    name: str
    description: str
    material: str
    status: str
    is_retired: bool
    avg_price: float
    price_change_7d: float
    price_change_30d: float
    price_change_90d: float
    popularity: int
    images: List[str]
    listings: List[Listing]
    price_history: List[PriceHistoryEntry]
    related_charm_ids: List[str]
    last_updated: datetime


class CharmListResponse(BaseModel):
    id: str
    name: str
    material: str
    status: str
    avg_price: float
    price_change_7d: float
    popularity: int
    images: List[str]
    last_updated: datetime


class MarketOverview(BaseModel):
    average_price: float
    total_charms: int
    active_charms: int
    retired_charms: int
    top_gainers: List[dict]
    top_losers: List[dict]
    recently_sold: List[dict]
    last_updated: datetime = Field(default_factory=datetime.utcnow)