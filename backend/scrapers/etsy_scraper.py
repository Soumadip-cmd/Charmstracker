"""
Etsy Scraper for CharmTracker
Scrapes Etsy listings for James Avery charms
"""

import asyncio
import logging
from typing import List, Dict, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class EtsyScraper:
    """Etsy scraper for charm listings"""
    
    def __init__(self):
        self.base_url = "https://www.etsy.com"
        self.search_url = f"{self.base_url}/search"
        
    async def search_charm(
        self, 
        charm_name: str, 
        limit: int = 20
    ) -> List[Dict]:
        """
        Search Etsy for a specific charm
        Returns list of listings with prices and details
        """
        try:
            query = f"james avery {charm_name}"
            
            async with aiohttp.ClientSession() as session:
                params = {
                    'q': query,
                    'explicit': 1,
                    'page': 1
                }
                
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(
                    self.search_url,
                    params=params,
                    headers=headers
                ) as response:
                    if response.status != 200:
                        logger.error(f"Etsy returned status {response.status}")
                        return []
                    
                    html = await response.text()
                    return self._parse_search_results(html, limit)
                    
        except Exception as e:
            logger.error(f"Error searching Etsy: {str(e)}")
            return []
    
    def _parse_search_results(self, html: str, limit: int) -> List[Dict]:
        """Parse Etsy search results HTML"""
        listings = []
        soup = BeautifulSoup(html, 'html.parser')
        
        # Etsy uses data attributes for listings
        listing_cards = soup.find_all('div', {'data-search-results-listing': True})[:limit]
        
        for card in listing_cards:
            try:
                listing = self._parse_listing_card(card)
                if listing:
                    listings.append(listing)
            except Exception as e:
                logger.warning(f"Error parsing Etsy listing: {str(e)}")
                continue
        
        logger.info(f"Found {len(listings)} Etsy listings")
        return listings
    
    def _parse_listing_card(self, card) -> Optional[Dict]:
        """Parse individual listing card"""
        try:
            # Title
            title_elem = card.find('h3', class_='v2-listing-card__title')
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)
            
            # Price
            price_elem = card.find('span', class_='currency-value')
            if not price_elem:
                return None
            price_text = price_elem.get_text(strip=True)
            price = self._parse_price(price_text)
            
            # Link
            link_elem = card.find('a', class_='listing-link')
            listing_url = link_elem['href'] if link_elem else ""
            if listing_url and not listing_url.startswith('http'):
                listing_url = f"{self.base_url}{listing_url}"
            
            # Image
            img_elem = card.find('img', class_='wt-width-full')
            image_url = img_elem.get('src', '') if img_elem else ""
            
            # Seller
            seller_elem = card.find('p', class_='v2-listing-card__shop')
            seller_name = seller_elem.get_text(strip=True) if seller_elem else "Unknown"
            
            # Condition (Etsy is usually "handmade" or "vintage")
            condition = "Handmade"
            if 'vintage' in title.lower():
                condition = "Vintage"
            
            return {
                "title": title,
                "price": price,
                "url": listing_url,
                "image_url": image_url,
                "seller": seller_name,
                "condition": condition,
                "marketplace": "Etsy",
                "scraped_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error parsing Etsy card: {str(e)}")
            return None
    
    def _parse_price(self, price_text: str) -> float:
        """Extract numeric price from text"""
        try:
            # Remove currency symbols and convert to float
            price_str = re.sub(r'[^\d.]', '', price_text)
            return float(price_str)
        except:
            return 0.0
    
    async def get_listing_details(self, listing_url: str) -> Optional[Dict]:
        """
        Get detailed information from a specific listing page
        """
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }
                
                async with session.get(listing_url, headers=headers) as response:
                    if response.status != 200:
                        return None
                    
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Extract additional details
                    description_elem = soup.find('p', {'data-product-details-description-text-content': True})
                    description = description_elem.get_text(strip=True) if description_elem else ""
                    
                    # Shipping info
                    shipping_elem = soup.find('span', {'data-shipping-cost': True})
                    shipping = shipping_elem.get_text(strip=True) if shipping_elem else "Unknown"
                    
                    return {
                        "description": description,
                        "shipping": shipping,
                        "detailed_url": listing_url
                    }
                    
        except Exception as e:
            logger.error(f"Error getting Etsy listing details: {str(e)}")
            return None


# Create singleton instance for import
etsy_scraper = EtsyScraper()


# Testing function
async def test_etsy_scraper():
    """Test the Etsy scraper"""
    scraper = EtsyScraper()
    results = await scraper.search_charm("cross charm", limit=5)
    
    print(f"\n✅ Found {len(results)} Etsy listings:")
    for listing in results:
        print(f"  • {listing['title'][:50]}... - ${listing['price']}")
    
    return results


if __name__ == "__main__":
    asyncio.run(test_etsy_scraper())