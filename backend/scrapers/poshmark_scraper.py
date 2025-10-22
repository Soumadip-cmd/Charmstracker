"""
Poshmark Scraper for CharmTracker
Fetches real-time listings and pricing data from Poshmark
"""

import logging
from typing import List, Dict
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class PoshmarkScraper:
    """Poshmark scraper for charm listings"""
    
    def __init__(self):
        self.base_url = "https://poshmark.com"
        self.search_url = f"{self.base_url}/search"
        
    async def search_charm(
        self, 
        charm_name: str, 
        limit: int = 20
    ) -> List[Dict]:
        """
        Search Poshmark for a specific charm
        Returns list of listings with prices and details
        """
        try:
            search_query = f"James Avery {charm_name} charm"
            params = {
                'query': search_query,
                'department': 'Jewelry',
                'price_min': '10',
                'price_max': '500',
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.search_url, 
                    params=params, 
                    headers=headers
                ) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_response(html, limit)
                    else:
                        logger.warning(f"Poshmark returned status {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error searching Poshmark for {charm_name}: {str(e)}")
            return []
    
    def _parse_response(self, html: str, limit: int) -> List[Dict]:
        """Parse Poshmark HTML response"""
        listings = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find listing cards
            items = soup.find_all('div', class_=re.compile(r'tile'))
            if not items:
                items = soup.find_all('a', class_=re.compile(r'tile__covershot'))
            
            for item in items[:limit]:
                try:
                    # Extract price
                    price_elem = item.find('span', class_=re.compile(r'price'))
                    if not price_elem:
                        price_elem = item.find('div', class_=re.compile(r'price'))
                    
                    if not price_elem:
                        continue
                    
                    price_text = price_elem.text.strip()
                    price_match = re.search(r'\$([\d,]+\.?\d*)', price_text)
                    if not price_match:
                        continue
                    
                    price = float(price_match.group(1).replace(',', ''))
                    
                    # Extract URL
                    url = ''
                    if item.name == 'a':
                        url = item.get('href', '')
                    else:
                        link = item.find('a')
                        url = link.get('href', '') if link else ''
                    
                    if url and not url.startswith('http'):
                        url = f"{self.base_url}{url}"
                    
                    # Extract title
                    title_elem = item.find('a', class_=re.compile(r'tile__title'))
                    if not title_elem:
                        title_elem = item.find('h2')
                    title = title_elem.text.strip() if title_elem else ''
                    
                    # Extract image
                    img_elem = item.find('img')
                    image_url = ''
                    if img_elem:
                        image_url = img_elem.get('src', img_elem.get('data-src', ''))
                    
                    # Extract seller
                    seller_elem = item.find('a', class_=re.compile(r'tile__creator'))
                    seller = seller_elem.text.strip() if seller_elem else ''
                    
                    # Extract condition
                    condition_elem = item.find('span', class_=re.compile(r'condition'))
                    condition = 'Pre-owned'
                    if condition_elem:
                        condition_text = condition_elem.text.strip()
                        if 'new' in condition_text.lower():
                            condition = 'New'
                    
                    listing = {
                        'platform': 'Poshmark',
                        'title': title,
                        'price': price,
                        'url': url,
                        'condition': condition,
                        'image_url': image_url,
                        'seller': seller,
                        'location': '',
                        'shipping': 7.97,  # Poshmark standard shipping
                        'scraped_at': datetime.utcnow()
                    }
                    
                    if listing['price'] > 0 and listing['url']:
                        listings.append(listing)
                        
                except Exception as e:
                    logger.debug(f"Error parsing Poshmark item: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing Poshmark response: {str(e)}")
            
        return listings


# Initialize scraper instance
poshmark_scraper = PoshmarkScraper()