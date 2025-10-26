"""
Auto-Discovery James Avery Scraper
Automatically discovers and syncs ALL charms from James Avery website
Run with: python auto_discovery_scraper.py
"""

import asyncio
import logging
from datetime import datetime, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import aiohttp
from bs4 import BeautifulSoup
import re

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JamesAveryAutoDiscovery:
    """Auto-discovers and syncs charms from James Avery website"""
    
    def __init__(self, db):
        self.db = db
        self.base_url = "https://www.jamesavery.com"
        self.charm_categories = [
            "/charms/sterling-silver-charms",
            "/charms/gold-charms",
            "/charms/retired-charms"
        ]
    
    async def discover_all_charms(self):
        """
        Main function: Discover ALL charms from James Avery website
        """
        logger.info("🔍 Starting James Avery auto-discovery...")
        
        discovered_charms = []
        
        for category_url in self.charm_categories:
            logger.info(f"📂 Scanning category: {category_url}")
            charms = await self._scrape_category(category_url)
            discovered_charms.extend(charms)
            
            # Rate limiting
            await asyncio.sleep(2)
        
        logger.info(f"✅ Discovered {len(discovered_charms)} charms from James Avery")
        
        # Sync with database
        await self._sync_to_database(discovered_charms)
        
        return discovered_charms
    
    async def _scrape_category(self, category_path):
        """Scrape all charms from a category page"""
        charms = []
        
        try:
            url = f"{self.base_url}{category_path}"
            
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                # Get category page
                async with session.get(url, headers=headers, timeout=30) as response:
                    if response.status != 200:
                        logger.warning(f"Failed to fetch {url}: {response.status}")
                        return charms
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find all product links
                    product_links = soup.find_all('a', href=re.compile(r'/products/'))
                    
                    logger.info(f"   Found {len(product_links)} products in category")
                    
                    # Extract unique product URLs
                    unique_urls = set()
                    for link in product_links:
                        href = link.get('href', '')
                        if '/products/' in href and 'charm' in href.lower():
                            if not href.startswith('http'):
                                href = f"{self.base_url}{href}"
                            unique_urls.add(href)
                    
                    # Scrape each product
                    for product_url in list(unique_urls)[:50]:  # Limit to 50 per category
                        charm_data = await self._scrape_charm_details(product_url, session)
                        if charm_data:
                            charms.append(charm_data)
                        
                        # Rate limiting
                        await asyncio.sleep(1)
        
        except Exception as e:
            logger.error(f"Error scraping category {category_path}: {str(e)}")
        
        return charms
    
    async def _scrape_charm_details(self, url, session):
        """Scrape detailed info for a single charm"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with session.get(url, headers=headers, timeout=20) as response:
                if response.status != 200:
                    return None
                
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract charm details
                name = self._extract_name(soup)
                if not name:
                    return None
                
                description = self._extract_description(soup)
                material = self._extract_material(soup, name)
                price = self._extract_price(soup)
                images = self._extract_images(soup)
                is_retired = 'retired' in url.lower() or 'discontinued' in html.lower()
                
                charm_data = {
                    'name': name,
                    'description': description or f"Sterling silver {name} from James Avery.",
                    'material': material,
                    'status': 'Retired' if is_retired else 'Active',
                    'is_retired': is_retired,
                    'official_price': price,
                    'images': images if images else self._generate_placeholder(name),
                    'official_url': url,
                    'discovered_at': datetime.now(timezone.utc),
                    'source': 'james_avery_auto_discovery'
                }
                
                logger.info(f"   ✅ Scraped: {name} (${price if price else 'N/A'})")
                
                return charm_data
        
        except Exception as e:
            logger.error(f"Error scraping charm {url}: {str(e)}")
            return None
    
    def _extract_name(self, soup):
        """Extract charm name"""
        # Try multiple selectors
        name_elem = (
            soup.find('h1', class_=re.compile(r'product.*name', re.I)) or
            soup.find('h1', {'itemprop': 'name'}) or
            soup.find('h1')
        )
        
        if name_elem:
            name = name_elem.get_text(strip=True)
            # Clean up name
            name = re.sub(r'\s+', ' ', name)
            return name
        return None
    
    def _extract_description(self, soup):
        """Extract charm description"""
        desc_elem = (
            soup.find('div', class_=re.compile(r'description', re.I)) or
            soup.find('div', {'itemprop': 'description'}) or
            soup.find('meta', {'name': 'description'})
        )
        
        if desc_elem:
            if desc_elem.name == 'meta':
                return desc_elem.get('content', '')
            return desc_elem.get_text(strip=True)
        return None
    
    def _extract_material(self, soup, name):
        """Extract material type"""
        text = soup.get_text().lower()
        name_lower = name.lower()
        
        if 'gold' in name_lower or 'gold' in text:
            return 'Gold'
        return 'Silver'  # Default for James Avery
    
    def _extract_price(self, soup):
        """Extract official price"""
        price_elem = (
            soup.find('span', class_=re.compile(r'price', re.I)) or
            soup.find('span', {'itemprop': 'price'}) or
            soup.find('meta', {'property': 'product:price:amount'})
        )
        
        if price_elem:
            price_text = price_elem.get('content') or price_elem.get_text()
            price_match = re.search(r'[\$]?([\d,]+\.?\d*)', price_text)
            if price_match:
                return float(price_match.group(1).replace(',', ''))
        return None
    
    def _extract_images(self, soup):
        """Extract product images"""
        images = []
        
        # Try multiple selectors
        img_elements = (
            soup.find_all('img', class_=re.compile(r'product.*image', re.I))[:4] or
            soup.find_all('img', {'itemprop': 'image'})[:4] or
            soup.find_all('img', src=re.compile(r'product|item|charm', re.I))[:4]
        )
        
        for img in img_elements:
            src = img.get('src') or img.get('data-src')
            if src and 'placeholder' not in src.lower():
                if not src.startswith('http'):
                    src = f"{self.base_url}{src}"
                images.append(src)
        
        return images[:4] if images else []
    
    def _generate_placeholder(self, name):
        """Generate placeholder if no images found"""
        encoded_name = name.replace(' ', '+')
        return [f"https://via.placeholder.com/400x400/C0C0C0/666666?text={encoded_name}"]
    
    async def _sync_to_database(self, discovered_charms):
        """
        Sync discovered charms with database
        - Add new charms
        - Update existing charms
        - Mark missing charms as retired
        """
        logger.info("📊 Syncing with database...")
        
        added_count = 0
        updated_count = 0
        
        for charm_data in discovered_charms:
            charm_id = f"charm_{charm_data['name'].lower().replace(' ', '_').replace('/', '_')}"
            
            # Check if charm exists
            existing = await self.db.charms.find_one({'id': charm_id})
            
            if existing:
                # Update existing charm
                update_data = {
                    'name': charm_data['name'],
                    'description': charm_data['description'],
                    'material': charm_data['material'],
                    'status': charm_data['status'],
                    'is_retired': charm_data['is_retired'],
                    'official_url': charm_data['official_url'],
                    'last_updated': datetime.now(timezone.utc)
                }
                
                # Update images only if better than placeholder
                if charm_data['images'] and 'placeholder' not in charm_data['images'][0]:
                    update_data['images'] = charm_data['images']
                
                # Update price if available
                if charm_data.get('official_price'):
                    update_data['avg_price'] = charm_data['official_price']
                
                await self.db.charms.update_one(
                    {'id': charm_id},
                    {'$set': update_data}
                )
                
                updated_count += 1
                logger.info(f"   🔄 Updated: {charm_data['name']}")
            
            else:
                # Add new charm
                new_charm = {
                    'id': charm_id,
                    **charm_data,
                    'avg_price': charm_data.get('official_price', 0) or 50.0,
                    'price_change_7d': 0.0,
                    'price_change_30d': 0.0,
                    'price_change_90d': 0.0,
                    'popularity': 70,
                    'listings': [],
                    'price_history': [],
                    'related_charm_ids': [],
                    'created_at': datetime.now(timezone.utc),
                    'last_updated': datetime.now(timezone.utc)
                }
                
                await self.db.charms.insert_one(new_charm)
                
                added_count += 1
                logger.info(f"   ✨ Added NEW: {charm_data['name']}")
        
        logger.info(f"✅ Sync complete: {added_count} added, {updated_count} updated")
        
        return {
            'added': added_count,
            'updated': updated_count,
            'total_discovered': len(discovered_charms)
        }


async def run_auto_discovery():
    """Main execution function"""
    
    logger.info("=" * 80)
    logger.info("James Avery Auto-Discovery Scraper")
    logger.info("=" * 80)
    
    # Connect to database
    mongo_url = os.getenv('MONGO_URL')
    if not mongo_url:
        logger.error("❌ MONGO_URL not found in environment")
        return
    
    client = AsyncIOMotorClient(mongo_url)
    db_name = os.getenv('DB_NAME', 'charmtracker_production')
    db = client[db_name]
    
    logger.info(f"✅ Connected to database: {db_name}")
    
    # Run discovery
    scraper = JamesAveryAutoDiscovery(db)
    charms = await scraper.discover_all_charms()
    
    # Summary
    logger.info("=" * 80)
    logger.info("Summary")
    logger.info("=" * 80)
    logger.info(f"✅ Discovered {len(charms)} charms from James Avery")
    logger.info(f"📊 Database now has {await db.charms.count_documents({})} total charms")
    
    client.close()


if __name__ == "__main__":
    try:
        asyncio.run(run_auto_discovery())
    except KeyboardInterrupt:
        logger.info("\n⚠️  Interrupted by user")
    except Exception as e:
        logger.error(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()