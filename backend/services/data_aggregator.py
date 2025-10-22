"""
Data Aggregator Service for CharmTracker
Combines data from all scrapers and updates database
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import asyncio
from statistics import mean, median

from scrapers.ebay_scraper import ebay_scraper
from scrapers.etsy_scraper import etsy_scraper
from scrapers.poshmark_scraper import poshmark_scraper
from scrapers.james_avery_scraper import james_avery_scraper

logger = logging.getLogger(__name__)


class DataAggregator:
    """Aggregates data from all sources"""
    
    def __init__(self, db):
        self.db = db
        self.scrapers = {
            'ebay': ebay_scraper,
            'etsy': etsy_scraper,
            'poshmark': poshmark_scraper,
            'james_avery': james_avery_scraper
        }
    
    async def update_charm_data(self, charm_id: str) -> bool:
        """
        Update all data for a specific charm
        Fetches from all marketplaces and James Avery
        """
        try:
            # Get existing charm data
            charm = await self.db.charms.find_one({"id": charm_id})
            if not charm:
                logger.error(f"Charm {charm_id} not found")
                return False
            
            charm_name = charm['name']
            logger.info(f"Updating data for: {charm_name}")
            
            # Fetch data from all sources in parallel
            tasks = [
                self._fetch_marketplace_data(charm_name, 'ebay'),
                self._fetch_marketplace_data(charm_name, 'etsy'),
                self._fetch_marketplace_data(charm_name, 'poshmark'),
                self._fetch_james_avery_data(charm_name)
            ]
            
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            ebay_data = results[0] if not isinstance(results[0], Exception) else []
            etsy_data = results[1] if not isinstance(results[1], Exception) else []
            poshmark_data = results[2] if not isinstance(results[2], Exception) else []
            ja_data = results[3] if not isinstance(results[3], Exception) else None
            
            # Combine all listings
            all_listings = ebay_data + etsy_data + poshmark_data
            
            if not all_listings and not ja_data:
                logger.warning(f"No data found for {charm_name}")
                return False
            
            # Calculate aggregated data
            update_data = await self._calculate_aggregated_data(
                charm, 
                all_listings, 
                ja_data
            )
            
            # Update database
            result = await self.db.charms.update_one(
                {"id": charm_id},
                {"$set": update_data}
            )
            
            logger.info(f"Updated {charm_name}: {result.modified_count} documents modified")
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating charm {charm_id}: {str(e)}")
            return False
    
    async def _fetch_marketplace_data(
        self, 
        charm_name: str, 
        platform: str
    ) -> List[Dict]:
        """Fetch data from a specific marketplace"""
        try:
            scraper = self.scrapers.get(platform)
            if not scraper:
                return []
            
            listings = await scraper.search_charm(charm_name, limit=20)
            logger.info(f"Found {len(listings)} listings on {platform}")
            return listings
            
        except Exception as e:
            logger.error(f"Error fetching from {platform}: {str(e)}")
            return []
    
    async def _fetch_james_avery_data(
        self, 
        charm_name: str
    ) -> Optional[Dict]:
        """Fetch official James Avery data"""
        try:
            ja_scraper = self.scrapers['james_avery']
            details = await ja_scraper.get_charm_details(charm_name)
            
            if details:
                logger.info(f"Found James Avery details for {charm_name}")
            else:
                logger.info(f"No James Avery details found for {charm_name}")
                
            return details
            
        except Exception as e:
            logger.error(f"Error fetching James Avery data: {str(e)}")
            return None
    
    async def _calculate_aggregated_data(
        self, 
        existing_charm: Dict,
        listings: List[Dict],
        ja_data: Optional[Dict]
    ) -> Dict:
        """Calculate aggregated pricing and metadata"""
        update_data = {
            "last_updated": datetime.utcnow()
        }
        
        # Update from James Avery official data if available
        if ja_data:
            if ja_data.get('name'):
                update_data['name'] = ja_data['name']
            if ja_data.get('description'):
                update_data['description'] = ja_data['description']
            if ja_data.get('material'):
                update_data['material'] = ja_data['material']
            if ja_data.get('status'):
                update_data['status'] = ja_data['status']
                update_data['is_retired'] = ja_data['is_retired']
            if ja_data.get('images'):
                # Prefer official images
                update_data['images'] = ja_data['images']
        
        # Update listings
        if listings:
            # Format listings for database
            formatted_listings = []
            for listing in listings[:20]:  # Keep top 20
                formatted_listings.append({
                    'platform': listing['platform'],
                    'title': listing['title'],
                    'price': listing['price'],
                    'url': listing['url'],
                    'condition': listing['condition'],
                    'image_url': listing.get('image_url', ''),
                    'seller': listing.get('seller', ''),
                    'shipping': listing.get('shipping', 0.0),
                    'scraped_at': listing['scraped_at']
                })
            
            update_data['listings'] = formatted_listings
            
            # Calculate price statistics
            prices = [l['price'] for l in listings if l['price'] > 0]
            
            if prices:
                avg_price = mean(prices)
                median_price = median(prices)
                
                update_data['avg_price'] = round(avg_price, 2)
                update_data['median_price'] = round(median_price, 2)
                update_data['min_price'] = round(min(prices), 2)
                update_data['max_price'] = round(max(prices), 2)
                
                # Add new price to history
                new_price_entry = {
                    'date': datetime.utcnow(),
                    'price': round(avg_price, 2),
                    'source': 'aggregated',
                    'listing_count': len(prices)
                }
                
                # Get existing price history
                price_history = existing_charm.get('price_history', [])
                
                # Only add if price is different or it's been more than 12 hours
                should_add = True
                if price_history:
                    last_entry = price_history[-1]
                    last_date = last_entry.get('date')
                    last_price = last_entry.get('price')
                    
                    if isinstance(last_date, datetime):
                        time_diff = datetime.utcnow() - last_date
                        if time_diff < timedelta(hours=12) and abs(last_price - avg_price) < 1.0:
                            should_add = False
                
                if should_add:
                    price_history.append(new_price_entry)
                    # Keep last 180 days of history
                    cutoff_date = datetime.utcnow() - timedelta(days=180)
                    price_history = [
                        entry for entry in price_history 
                        if isinstance(entry.get('date'), datetime) and entry['date'] >= cutoff_date
                    ]
                    
                    update_data['price_history'] = price_history
                    
                    # Calculate price changes
                    price_changes = self._calculate_price_changes(price_history, avg_price)
                    update_data.update(price_changes)
                
                # Update popularity based on listing count and recency
                listing_count = len(listings)
                popularity = min(100, int((listing_count / 30) * 100))
                update_data['popularity'] = max(
                    existing_charm.get('popularity', 50), 
                    popularity
                )
        
        return update_data
    
    def _calculate_price_changes(
        self, 
        price_history: List[Dict], 
        current_price: float
    ) -> Dict:
        """Calculate price change percentages"""
        changes = {
            'price_change_7d': 0.0,
            'price_change_30d': 0.0,
            'price_change_90d': 0.0
        }
        
        try:
            now = datetime.utcnow()
            
            # Get prices for different time periods
            price_7d = None
            price_30d = None
            price_90d = None
            
            for entry in reversed(price_history):
                date = entry.get('date')
                if not isinstance(date, datetime):
                    continue
                
                days_ago = (now - date).days
                
                if days_ago >= 7 and price_7d is None:
                    price_7d = entry.get('price')
                if days_ago >= 30 and price_30d is None:
                    price_30d = entry.get('price')
                if days_ago >= 90 and price_90d is None:
                    price_90d = entry.get('price')
            
            # Calculate percentage changes
            if price_7d and price_7d > 0:
                changes['price_change_7d'] = round(
                    ((current_price - price_7d) / price_7d) * 100, 1
                )
            
            if price_30d and price_30d > 0:
                changes['price_change_30d'] = round(
                    ((current_price - price_30d) / price_30d) * 100, 1
                )
            
            if price_90d and price_90d > 0:
                changes['price_change_90d'] = round(
                    ((current_price - price_90d) / price_90d) * 100, 1
                )
                
        except Exception as e:
            logger.error(f"Error calculating price changes: {str(e)}")
        
        return changes
    
    async def update_all_charms(self, limit: Optional[int] = None) -> Dict:
        """
        Update data for all charms in database
        Returns statistics about the update
        """
        try:
            # Get all charm IDs
            cursor = self.db.charms.find({}, {"id": 1})
            if limit:
                cursor = cursor.limit(limit)
            
            charms = await cursor.to_list(length=limit or 1000)
            charm_ids = [charm['id'] for charm in charms]
            
            logger.info(f"Starting update for {len(charm_ids)} charms")
            
            # Update charms with rate limiting (avoid overwhelming scrapers)
            success_count = 0
            fail_count = 0
            
            for i, charm_id in enumerate(charm_ids):
                try:
                    logger.info(f"Updating charm {i+1}/{len(charm_ids)}: {charm_id}")
                    success = await self.update_charm_data(charm_id)
                    
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                    
                    # Rate limiting - wait between requests
                    if i < len(charm_ids) - 1:
                        await asyncio.sleep(2)  # 2 second delay between charms
                        
                except Exception as e:
                    logger.error(f"Error updating charm {charm_id}: {str(e)}")
                    fail_count += 1
            
            stats = {
                'total': len(charm_ids),
                'success': success_count,
                'failed': fail_count,
                'updated_at': datetime.utcnow()
            }
            
            logger.info(f"Update complete: {stats}")
            return stats
            
        except Exception as e:
            logger.error(f"Error in update_all_charms: {str(e)}")
            return {
                'total': 0,
                'success': 0,
                'failed': 0,
                'error': str(e)
            }