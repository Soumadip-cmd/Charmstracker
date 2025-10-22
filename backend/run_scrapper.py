"""
Run scrapers to fetch charm data from marketplaces
This can be run manually or scheduled as a cron job
"""

import asyncio
import sys
import logging
from datetime import datetime

sys.path.append('.')

from database import get_database
from scrapers.ebay_scraper import EbayScraper
from scrapers.etsy_scraper import EtsyScraper
from services.price_calculator import PriceCalculator

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def scrape_charm_prices(charm_name: str, charm_id: str):
    """Scrape prices for a single charm from all marketplaces"""
    
    logger.info(f"🔍 Scraping prices for: {charm_name}")
    
    # Initialize scrapers
    ebay_scraper = EbayScraper()
    etsy_scraper = EtsyScraper()
    
    # Scrape from both marketplaces
    ebay_listings = await ebay_scraper.search_charm(charm_name, limit=20)
    etsy_listings = await etsy_scraper.search_charm(charm_name, limit=20)
    
    all_listings = ebay_listings + etsy_listings
    
    if not all_listings:
        logger.warning(f"⚠️ No listings found for {charm_name}")
        return None
    
    logger.info(f"✅ Found {len(all_listings)} listings for {charm_name}")
    
    # Calculate average price
    prices = [listing['price'] for listing in all_listings if listing['price'] > 0]
    
    if prices:
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)
        
        # Update database
        db = await get_database()
        
        price_data = {
            "date": datetime.utcnow().isoformat(),
            "average": round(avg_price, 2),
            "min": round(min_price, 2),
            "max": round(max_price, 2),
            "count": len(prices)
        }
        
        await db.charms.update_one(
            {"_id": charm_id},
            {
                "$set": {
                    "averagePrice": round(avg_price, 2),
                    "lastUpdated": datetime.utcnow()
                },
                "$push": {
                    "priceHistory": {
                        "$each": [price_data],
                        "$slice": -90  # Keep last 90 days
                    }
                }
            }
        )
        
        logger.info(f"💰 Updated {charm_name}: ${round(avg_price, 2)} (${min_price}-${max_price})")
        
        return price_data
    
    return None


async def run_all_scrapers():
    """Run scrapers for all charms in database"""
    
    logger.info("🚀 Starting scraper run...")
    
    try:
        db = await get_database()
        
        # Get all charms
        charms_cursor = db.charms.find({})
        charms = await charms_cursor.to_list(length=None)
        
        if not charms:
            logger.warning("⚠️ No charms found in database. Run seed_charms.py first!")
            return
        
        logger.info(f"📊 Found {len(charms)} charms to scrape")
        
        success_count = 0
        failed_count = 0
        
        # Scrape each charm (with delay to avoid rate limiting)
        for i, charm in enumerate(charms, 1):
            try:
                logger.info(f"[{i}/{len(charms)}] Processing: {charm['name']}")
                
                result = await scrape_charm_prices(
                    charm_name=charm['name'],
                    charm_id=charm['_id']
                )
                
                if result:
                    success_count += 1
                else:
                    failed_count += 1
                
                # Delay between requests to avoid rate limiting
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Error scraping {charm['name']}: {str(e)}")
                failed_count += 1
                continue
        
        logger.info(f"✅ Scraper run complete!")
        logger.info(f"   Success: {success_count}")
        logger.info(f"   Failed: {failed_count}")
        logger.info(f"   Total: {len(charms)}")
        
    except Exception as e:
        logger.error(f"❌ Fatal error in scraper run: {str(e)}")
        raise


async def scrape_single_charm(charm_name: str):
    """Scrape a single charm by name (for testing)"""
    
    try:
        db = await get_database()
        charm = await db.charms.find_one({"name": charm_name})
        
        if not charm:
            logger.error(f"❌ Charm not found: {charm_name}")
            return
        
        await scrape_charm_prices(charm['name'], charm['_id'])
        
    except Exception as e:
        logger.error(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Scrape specific charm
        charm_name = " ".join(sys.argv[1:])
        logger.info(f"🎯 Scraping single charm: {charm_name}")
        asyncio.run(scrape_single_charm(charm_name))
    else:
        # Scrape all charms
        logger.info("🎯 Scraping all charms")
        asyncio.run(run_all_scrapers())