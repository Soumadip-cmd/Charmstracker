"""
Scraper API Routes for CharmTracker
Provides endpoints to trigger and monitor data updates
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from typing import Optional
from datetime import datetime
import logging

from services.data_aggregator import DataAggregator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/scraper", tags=["scraper"])


def get_database():
    from server import db
    return db


def get_aggregator():
    db = get_database()
    return DataAggregator(db)


@router.post("/update/{charm_id}")
async def update_charm(
    charm_id: str,
    background_tasks: BackgroundTasks
):
    """
    Trigger an update for a specific charm
    Runs in background to avoid blocking
    """
    try:
        # Run update in background
        aggregator = get_aggregator()
        background_tasks.add_task(aggregator.update_charm_data, charm_id)
        
        return {
            "message": f"Update started for charm {charm_id}",
            "status": "processing",
            "charm_id": charm_id
        }
        
    except Exception as e:
        logger.error(f"Error triggering update for {charm_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/update-all")
async def update_all_charms(
    background_tasks: BackgroundTasks,
    limit: Optional[int] = Query(None, ge=1, le=100)
):
    """
    Trigger update for all charms (or limited number)
    Runs in background
    """
    try:
        aggregator = get_aggregator()
        background_tasks.add_task(aggregator.update_all_charms, limit)
        
        return {
            "message": f"Update started for {'all' if not limit else limit} charms",
            "status": "processing",
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error triggering update-all: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
async def get_scraper_status():
    """Get status of scraper service"""
    try:
        db = get_database()
        
        # Get last update times for charms
        recent_updates = await db.charms.find(
            {},
            {"id": 1, "name": 1, "last_updated": 1}
        ).sort("last_updated", -1).limit(10).to_list(10)
        
        # Count total charms
        total_charms = await db.charms.count_documents({})
        
        # Count charms updated in last 24 hours
        from datetime import timedelta
        cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_count = await db.charms.count_documents({
            "last_updated": {"$gte": cutoff}
        })
        
        return {
            "status": "operational",
            "total_charms": total_charms,
            "updated_last_24h": recent_count,
            "recent_updates": [
                {
                    "id": charm["id"],
                    "name": charm["name"],
                    "last_updated": charm.get("last_updated", "").isoformat() if charm.get("last_updated") else None
                }
                for charm in recent_updates
            ]
        }
        
    except Exception as e:
        logger.error(f"Error getting scraper status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/marketplace-check/{charm_name}")
async def check_marketplace_availability(charm_name: str):
    """
    Check if a charm is available on each marketplace
    Quick check without full update
    """
    try:
        from scrapers.ebay_scraper import ebay_scraper
        from scrapers.etsy_scraper import etsy_scraper
        from scrapers.poshmark_scraper import poshmark_scraper
        
        # Quick search on each platform (limit 5)
        import asyncio
        tasks = [
            ebay_scraper.search_charm(charm_name, limit=5),
            etsy_scraper.search_charm(charm_name, limit=5),
            poshmark_scraper.search_charm(charm_name, limit=5),
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        return {
            "charm_name": charm_name,
            "availability": {
                "ebay": {
                    "available": len(results[0]) > 0 if not isinstance(results[0], Exception) else False,
                    "listing_count": len(results[0]) if not isinstance(results[0], Exception) else 0
                },
                "etsy": {
                    "available": len(results[1]) > 0 if not isinstance(results[1], Exception) else False,
                    "listing_count": len(results[1]) if not isinstance(results[1], Exception) else 0
                },
                "poshmark": {
                    "available": len(results[2]) > 0 if not isinstance(results[2], Exception) else False,
                    "listing_count": len(results[2]) if not isinstance(results[2], Exception) else 0
                }
            },
            "checked_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error checking marketplace availability: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))