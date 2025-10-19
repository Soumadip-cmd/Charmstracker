from fastapi import APIRouter, HTTPException
from backend.models.charm import MarketOverview
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["market"])

# Database will be accessed from server.py
def get_database():
    from backend.server import db
    return db


@router.get("/trending")
async def get_trending_charms():
    """Get trending charms (top 6 by popularity and price change)"""
    try:
        db = get_database()
        # Get top 6 charms sorted by popularity and positive price change
        cursor = (
            db.charms.find({})
            .sort([("popularity", -1), ("price_change_7d", -1)])
            .limit(6)
        )
        charms = await cursor.to_list(length=6)

        trending = [
            {
                "id": charm["id"],
                "name": charm["name"],
                "avg_price": charm["avg_price"],
                "price_change": charm["price_change_7d"],
                "material": charm["material"],
                "status": charm["status"],
                "image": charm["images"][0] if charm["images"] else None,
            }
            for charm in charms
        ]

        return {"trending": trending}

    except Exception as e:
        logger.error(f"Error fetching trending charms: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching trending charms: {str(e)}")


@router.get("/market-overview", response_model=MarketOverview)
async def get_market_overview():
    """Get market statistics"""
    try:
        db = get_database()
        # Get all charms for calculations
        all_charms = await db.charms.find({}).to_list(length=1000)

        if not all_charms:
            return MarketOverview(
                average_price=0,
                total_charms=0,
                active_charms=0,
                retired_charms=0,
                top_gainers=[],
                top_losers=[],
                recently_sold=[],
            )

        # Calculate statistics
        total_charms = len(all_charms)
        active_charms = sum(1 for c in all_charms if c["status"] == "Active")
        retired_charms = sum(1 for c in all_charms if c["status"] == "Retired")
        average_price = sum(c["avg_price"] for c in all_charms) / total_charms

        # Get top gainers (sorted by price_change_7d descending)
        sorted_gainers = sorted(
            all_charms, key=lambda x: x["price_change_7d"], reverse=True
        )[:5]
        top_gainers = [
            {
                "id": c["id"],
                "name": c["name"],
                "change": c["price_change_7d"],
                "avg_price": c["avg_price"],
                "image": c["images"][0] if c["images"] else None,
            }
            for c in sorted_gainers
        ]

        # Get top losers (sorted by price_change_7d ascending)
        sorted_losers = sorted(all_charms, key=lambda x: x["price_change_7d"])[:5]
        top_losers = [
            {
                "id": c["id"],
                "name": c["name"],
                "change": c["price_change_7d"],
                "avg_price": c["avg_price"],
                "image": c["images"][0] if c["images"] else None,
            }
            for c in sorted_losers
        ]

        # Recently sold (most recent by last_updated)
        sorted_recent = sorted(
            all_charms, key=lambda x: x["last_updated"], reverse=True
        )[:5]
        recently_sold = [
            {
                "id": c["id"],
                "name": c["name"],
                "avg_price": c["avg_price"],
                "image": c["images"][0] if c["images"] else None,
                "last_updated": c["last_updated"].isoformat(),
            }
            for c in sorted_recent
        ]

        return MarketOverview(
            average_price=round(average_price, 2),
            total_charms=total_charms,
            active_charms=active_charms,
            retired_charms=retired_charms,
            top_gainers=top_gainers,
            top_losers=top_losers,
            recently_sold=recently_sold,
        )

    except Exception as e:
        logger.error(f"Error fetching market overview: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching market overview: {str(e)}")