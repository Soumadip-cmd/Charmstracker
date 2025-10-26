"""
Enhanced Scheduler with Auto-Discovery
Automatically discovers and updates charms from James Avery
Run with: Add to server.py startup
"""

import asyncio
import logging
from datetime import datetime
import os
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

# Import the auto-discovery scraper
import sys
sys.path.append('.')
from scrapers.james_avery_scraper import james_avery_scraper
from scrapers.ebay_scraper import ebay_scraper
from scrapers.etsy_scraper import etsy_scraper
from scrapers.poshmark_scraper import poshmark_scraper

logger = logging.getLogger(__name__)


class DynamicUpdateScheduler:
    """
    Manages automatic updates for CharmTracker
    
    Schedule:
    - Every 24 hours: Discover new charms from James Avery
    - Every 6 hours: Update prices from marketplaces
    - Every 12 hours: Update images
    """
    
    def __init__(self, db):
        self.db = db
        self.scheduler = AsyncIOScheduler()
        
    async def start(self):
        """Start the automatic scheduler"""
        logger.info("🚀 Starting dynamic update scheduler...")
        
        # Job 1: Auto-discover new charms (daily at 2 AM)
        self.scheduler.add_job(
            self.auto_discover_charms,
            CronTrigger(hour=2, minute=0),  # 2:00 AM daily
            id='auto_discover',
            name='Auto-discover James Avery charms',
            replace_existing=True
        )
        logger.info("   ✅ Scheduled: Auto-discovery (daily at 2 AM)")
        
        # Job 2: Update marketplace prices (every 6 hours)
        self.scheduler.add_job(
            self.update_marketplace_prices,
            CronTrigger(hour='*/6'),  # Every 6 hours
            id='update_prices',
            name='Update marketplace prices',
            replace_existing=True
        )
        logger.info("   ✅ Scheduled: Price updates (every 6 hours)")
        
        # Job 3: Update images (every 12 hours)
        self.scheduler.add_job(
            self.update_images,
            CronTrigger(hour='*/12'),  # Every 12 hours
            id='update_images',
            name='Update charm images',
            replace_existing=True
        )
        logger.info("   ✅ Scheduled: Image updates (every 12 hours)")
        
        # Start scheduler
        self.scheduler.start()
        logger.info("✅ Dynamic update scheduler started!")
        
    async def stop(self):
        """Stop the scheduler"""
        self.scheduler.shutdown()
        logger.info("🛑 Dynamic update scheduler stopped")
    
    async def auto_discover_charms(self):
        """
        Auto-discover new charms from James Avery website
        Runs daily at 2 AM
        """
        logger.info("🔍 Starting auto-discovery of James Avery charms...")
        
        try:
            # Get all charms from James Avery website
            discovered = await self._discover_from_james_avery()
            
            # Sync with database
            result = await self._sync_discovered_charms(discovered)
            
            logger.info(f"✅ Auto-discovery complete:")
            logger.info(f"   • New charms added: {result['added']}")
            logger.info(f"   • Existing updated: {result['updated']}")
            logger.info(f"   • Total in DB: {result['total']}")
            
        except Exception as e:
            logger.error(f"❌ Auto-discovery failed: {str(e)}")
    
    async def update_marketplace_prices(self):
        """
        Update prices from all marketplaces
        Runs every 6 hours
        """
        logger.info("💰 Updating marketplace prices...")
        
        try:
            # Get all charms from database
            charms = await self.db.charms.find({}).to_list(length=None)
            
            updated_count = 0
            
            for charm in charms[:20]:  # Update 20 charms per run
                try:
                    # Get prices from marketplaces
                    listings = await self._fetch_marketplace_listings(charm['name'])
                    
                    if listings:
                        # Calculate new average price
                        prices = [l['price'] for l in listings if l['price'] > 0]
                        if prices:
                            new_avg = sum(prices) / len(prices)
                            
                            # Update charm
                            await self.db.charms.update_one(
                                {'id': charm['id']},
                                {
                                    '$set': {
                                        'avg_price': round(new_avg, 2),
                                        'listings': listings,
                                        'last_updated': datetime.utcnow()
                                    }
                                }
                            )
                            updated_count += 1
                    
                    await asyncio.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error updating {charm['name']}: {str(e)}")
                    continue
            
            logger.info(f"✅ Price update complete: {updated_count} charms updated")
            
        except Exception as e:
            logger.error(f"❌ Price update failed: {str(e)}")
    
    async def update_images(self):
        """
        Update charm images from James Avery
        Runs every 12 hours
        """
        logger.info("🖼️  Updating charm images...")
        
        try:
            # Get charms with placeholder images
            charms = await self.db.charms.find({
                '$or': [
                    {'images.0': {'$regex': 'placeholder'}},
                    {'needs_image_update': True}
                ]
            }).to_list(length=50)
            
            updated_count = 0
            
            for charm in charms:
                try:
                    # Get real images from James Avery
                    details = await james_avery_scraper.get_charm_details(charm['name'])
                    
                    if details and details.get('images'):
                        # Update with real images
                        await self.db.charms.update_one(
                            {'id': charm['id']},
                            {
                                '$set': {
                                    'images': details['images'],
                                    'needs_image_update': False,
                                    'last_updated': datetime.utcnow()
                                }
                            }
                        )
                        updated_count += 1
                    
                    await asyncio.sleep(2)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error updating images for {charm['name']}: {str(e)}")
                    continue
            
            logger.info(f"✅ Image update complete: {updated_count} charms updated")
            
        except Exception as e:
            logger.error(f"❌ Image update failed: {str(e)}")
    
    async def _discover_from_james_avery(self):
        """Discover charms from James Avery website"""
        # This would use the auto_discovery_scraper.py logic
        # For now, return empty list
        # TODO: Implement full James Avery catalog scraping
        return []
    
    async def _sync_discovered_charms(self, discovered):
        """Sync discovered charms with database"""
        added = 0
        updated = 0
        
        for charm_data in discovered:
            charm_id = f"charm_{charm_data['name'].lower().replace(' ', '_')}"
            existing = await self.db.charms.find_one({'id': charm_id})
            
            if existing:
                # Update existing
                await self.db.charms.update_one(
                    {'id': charm_id},
                    {'$set': charm_data}
                )
                updated += 1
            else:
                # Add new
                await self.db.charms.insert_one({
                    'id': charm_id,
                    **charm_data
                })
                added += 1
        
        total = await self.db.charms.count_documents({})
        
        return {
            'added': added,
            'updated': updated,
            'total': total
        }
    
    async def _fetch_marketplace_listings(self, charm_name):
        """Fetch listings from all marketplaces"""
        listings = []
        
        try:
            # eBay
            ebay_listings = await ebay_scraper.search_charm(charm_name, limit=10)
            listings.extend(ebay_listings)
            
            # Etsy
            etsy_listings = await etsy_scraper.search_charm(charm_name, limit=10)
            listings.extend(etsy_listings)
            
            # Poshmark
            poshmark_listings = await poshmark_scraper.search_charm(charm_name, limit=10)
            listings.extend(poshmark_listings)
            
        except Exception as e:
            logger.error(f"Error fetching listings: {str(e)}")
        
        return listings


# Global scheduler instance
_dynamic_scheduler = None


def get_dynamic_scheduler(db):
    """Get or create scheduler instance"""
    global _dynamic_scheduler
    if _dynamic_scheduler is None:
        _dynamic_scheduler = DynamicUpdateScheduler(db)
    return _dynamic_scheduler


async def start_dynamic_scheduler(db):
    """Start the dynamic scheduler"""
    scheduler = get_dynamic_scheduler(db)
    await scheduler.start()


async def stop_dynamic_scheduler():
    """Stop the dynamic scheduler"""
    if _dynamic_scheduler:
        await _dynamic_scheduler.stop()