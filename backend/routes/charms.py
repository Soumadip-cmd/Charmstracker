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
    material: Optional[str] = Query(None, regex="^(Silver|Gold)$"),
    status: Optional[str] = Query(None, regex="^(Active|Retired)$"),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    page: int = Query(1, ge=1),
    limit: int = Query(100, ge=1, le=500),  # Increased max limit to 500
    load_all: bool = Query(False)  # New parameter to load all charms
):
    """
    Get all charms with filtering and sorting
    
    Parameters:
    - sort: Sort order (price_asc, price_desc, popularity, name)
    - material: Filter by material (Silver, Gold)
    - status: Filter by status (Active, Retired)
    - min_price: Minimum price filter
    - max_price: Maximum price filter
    - page: Page number (ignored if load_all=True)
    - limit: Items per page (max 500, ignored if load_all=True)
    - load_all: If True, returns all charms without pagination
    """
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

        # Handle load_all parameter
        if load_all:
            # Load all charms without pagination
            cursor = db.charms.find(filter_query).sort(list(sort_query.items()))
            charms = await cursor.to_list(length=None)  # Load all
            
            logger.info(f"Loading all {len(charms)} charms")
        else:
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

        if load_all:
            return {
                "charms": [charm.dict() for charm in charm_list],
                "total": total,
                "page": 1,
                "total_pages": 1,
                "limit": total,
                "load_all": True
            }
        else:
            return {
                "charms": [charm.dict() for charm in charm_list],
                "total": total,
                "page": page,
                "total_pages": (total + limit - 1) // limit,
                "limit": limit,
                "load_all": False
            }

    except Exception as e:
        logger.error(f"Error fetching charms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching charms: {str(e)}")


@router.get("/count")
async def get_charm_count():
    """Get total number of charms in database"""
    try:
        db = get_database()
        
        total = await db.charms.count_documents({})
        active = await db.charms.count_documents({"status": "Active"})
        retired = await db.charms.count_documents({"status": "Retired"})
        silver = await db.charms.count_documents({"material": "Silver"})
        gold = await db.charms.count_documents({"material": "Gold"})
        
        return {
            "total": total,
            "active": active,
            "retired": retired,
            "silver": silver,
            "gold": gold
        }
        
    except Exception as e:
        logger.error(f"Error getting charm count: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-ids")
async def get_all_charm_ids():
    """Get list of all charm IDs (lightweight endpoint)"""
    try:
        db = get_database()
        
        cursor = db.charms.find({}, {"id": 1, "name": 1, "_id": 0})
        charms = await cursor.to_list(length=None)
        
        return {
            "charm_ids": [{"id": c["id"], "name": c["name"]} for c in charms],
            "total": len(charms)
        }
        
    except Exception as e:
        logger.error(f"Error getting charm IDs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


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


@router.get("/search/name")
async def search_charms_by_name(
    query: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=100)
):
    """Search charms by name (case-insensitive partial match)"""
    try:
        db = get_database()
        
        # Use regex for case-insensitive partial matching
        filter_query = {
            "name": {"$regex": query, "$options": "i"}
        }
        
        cursor = db.charms.find(filter_query).limit(limit)
        charms = await cursor.to_list(length=limit)
        
        charm_list = [
            {
                "id": charm["id"],
                "name": charm["name"],
                "material": charm["material"],
                "status": charm["status"],
                "avg_price": charm["avg_price"],
                "image": charm["images"][0] if charm["images"] else None
            }
            for charm in charms
        ]
        
        return {
            "results": charm_list,
            "count": len(charm_list),
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Error searching charms: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))