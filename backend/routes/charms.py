from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from models.charm import (
    Charm,
    CharmCreate,
    CharmResponse,
    CharmListResponse,
    MarketOverview,
)
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/charms", tags=["charms"])

# Database will be accessed from server.py
def get_database():
    from server import db
    return db


@router.get("", response_model=dict)
async def get_all_charms(
    sort: Optional[str] = Query("popularity", regex="^(price_asc|price_desc|popularity|name)$"),
    material: Optional[str] = Query(None, regex="^(Silver|Gold|Mixed)$"),
    status: Optional[str] = Query(None, regex="^(Active|Retired)$"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
):
    """Get all charms with filtering and sorting"""
    try:
        db = get_database()
        # Build filter query
        filter_query = {}
        if material:
            filter_query["material"] = material
        if status:
            filter_query["status"] = status
        if min_price is not None or max_price is not None:
            filter_query["avg_price"] = {}
            if min_price is not None:
                filter_query["avg_price"]["$gte"] = min_price
            if max_price is not None:
                filter_query["avg_price"]["$lte"] = max_price

        # Build sort query
        sort_query = {}
        if sort == "price_asc":
            sort_query["avg_price"] = 1
        elif sort == "price_desc":
            sort_query["avg_price"] = -1
        elif sort == "popularity":
            sort_query["popularity"] = -1
        elif sort == "name":
            sort_query["name"] = 1

        # Get total count
        total = await db.charms.count_documents(filter_query)

        # Get paginated results
        skip = (page - 1) * limit
        cursor = db.charms.find(filter_query).sort(list(sort_query.items())).skip(skip).limit(limit)
        charms = await cursor.to_list(length=limit)

        # Format response
        charm_list = [
            CharmListResponse(
                id=charm["id"],
                name=charm["name"],
                material=charm["material"],
                status=charm["status"],
                avg_price=charm["avg_price"],
                price_change_7d=charm["price_change_7d"],
                popularity=charm["popularity"],
                images=charm["images"],
                last_updated=charm["last_updated"],
            )
            for charm in charms
        ]

        return {
            "charms": [charm.dict() for charm in charm_list],
            "total": total,
            "page": page,
            "total_pages": (total + limit - 1) // limit,
            "limit": limit,
        }

    except Exception as e:
        logger.error(f"Error fetching charms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching charms: {str(e)}")


@router.get("/{charm_id}", response_model=CharmResponse)
async def get_charm_by_id(charm_id: str):
    """Get detailed charm information"""
    try:
        db = get_database()
        charm = await db.charms.find_one({"id": charm_id})
        if not charm:
            raise HTTPException(status_code=404, detail="Charm not found")

        return CharmResponse(
            id=charm["id"],
            name=charm["name"],
            description=charm["description"],
            material=charm["material"],
            status=charm["status"],
            is_retired=charm["is_retired"],
            avg_price=charm["avg_price"],
            price_change_7d=charm["price_change_7d"],
            price_change_30d=charm["price_change_30d"],
            price_change_90d=charm["price_change_90d"],
            popularity=charm["popularity"],
            images=charm["images"],
            listings=charm.get("listings", []),
            price_history=charm.get("price_history", []),
            related_charm_ids=charm.get("related_charm_ids", []),
            last_updated=charm["last_updated"],
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching charm {charm_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching charm: {str(e)}")


@router.post("", response_model=CharmResponse)
async def create_charm(charm: CharmCreate):
    """Create a new charm"""
    try:
        db = get_database()
        charm_dict = Charm(
            **charm.dict(),
            price_history=[],
            listings=[],
            related_charm_ids=[],
        ).dict()

        result = await db.charms.insert_one(charm_dict)
        if result.inserted_id:
            created_charm = await db.charms.find_one({"_id": result.inserted_id})
            return CharmResponse(**created_charm)
        else:
            raise HTTPException(status_code=500, detail="Failed to create charm")

    except Exception as e:
        logger.error(f"Error creating charm: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating charm: {str(e)}")