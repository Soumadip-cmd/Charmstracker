"""
eBay API Integration for CharmTracker
Fetches real-time listings and pricing data
"""

import os
import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class EbayScraper:
    """eBay scraper using Finding API and web scraping"""
    
    def __init__(self):
        self.app_id = os.getenv('EBAY_APP_ID', '')  # Set in .env
        self.base_url = "https://svcs.ebay.com/services/search/FindingService/v1"
        self.search_url = "https://www.ebay.com/sch/i.html"
        
    async def search_charm(
        self, 
        charm_name: str, 
        limit: int = 20
    ) -> List[Dict]:
        """
        Search eBay for a specific charm
        Returns list of listings with prices and details
        """
        try:
            # If we have API key, use official API
            if self.app_id:
                return await self._search_with_api(charm_name, limit)
            else:
                # Fallback to web scraping
                return await self._search_with_scraping(charm_name, limit)
                
        except Exception as e:
            logger.error(f"Error searching eBay for {charm_name}: {str(e)}")
            return []
    
    async def _search_with_api(
        self, 
        charm_name: str, 
        limit: int = 20
    ) -> List[Dict]:
        """Search using eBay Finding API"""
        try:
            params = {
                'OPERATION-NAME': 'findItemsAdvanced',
                'SERVICE-VERSION': '1.0.0',
                'SECURITY-APPNAME': self.app_id,
                'RESPONSE-DATA-FORMAT': 'JSON',
                'REST-PAYLOAD': '',
                'keywords': f'James Avery {charm_name} charm',
                'paginationInput.entriesPerPage': limit,
                'sortOrder': 'EndTimeSoonest',
                'itemFilter(0).name': 'Condition',
                'itemFilter(0).value': 'New|Used',
                'itemFilter(1).name': 'ListingType',
                'itemFilter(1).value': 'FixedPrice|Auction',
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(self.base_url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._parse_api_response(data)
                    else:
                        logger.warning(f"eBay API returned status {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error with eBay API: {str(e)}")
            return []
    
    async def _search_with_scraping(
        self, 
        charm_name: str, 
        limit: int = 20
    ) -> List[Dict]:
        """Fallback web scraping method"""
        try:
            search_query = f"James Avery {charm_name} charm"
            params = {
                '_nkw': search_query,
                '_sacat': '0',
                'LH_Sold': '1',  # Sold listings
                'LH_Complete': '1',  # Completed listings
                '_udlo': '10',  # Min price $10
                '_udhi': '500',  # Max price $500
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.search_url, 
                    params=params, 
                    headers=headers
                ) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_html_response(html, limit)
                    else:
                        logger.warning(f"eBay scraping returned status {response.status}")
                        return []
                        
        except Exception as e:
            logger.error(f"Error scraping eBay: {str(e)}")
            return []
    
    def _parse_api_response(self, data: Dict) -> List[Dict]:
        """Parse eBay API JSON response"""
        listings = []
        try:
            search_result = data.get('findItemsAdvancedResponse', [{}])[0]
            items = search_result.get('searchResult', [{}])[0].get('item', [])
            
            for item in items:
                try:
                    listing = {
                        'platform': 'eBay',
                        'title': item.get('title', [''])[0],
                        'price': float(item.get('sellingStatus', [{}])[0]
                                     .get('currentPrice', [{}])[0]
                                     .get('__value__', 0)),
                        'url': item.get('viewItemURL', [''])[0],
                        'condition': item.get('condition', [{}])[0]
                                         .get('conditionDisplayName', ['Used'])[0],
                        'image_url': item.get('galleryURL', [''])[0],
                        'seller': item.get('sellerInfo', [{}])[0]
                                     .get('sellerUserName', [''])[0],
                        'location': item.get('location', [''])[0],
                        'shipping': float(item.get('shippingInfo', [{}])[0]
                                        .get('shippingServiceCost', [{}])[0]
                                        .get('__value__', 0)),
                        'end_time': item.get('listingInfo', [{}])[0]
                                       .get('endTime', [''])[0],
                        'scraped_at': datetime.utcnow()
                    }
                    
                    if listing['price'] > 0:  # Valid price
                        listings.append(listing)
                        
                except Exception as e:
                    logger.debug(f"Error parsing item: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing API response: {str(e)}")
            
        return listings
    
    def _parse_html_response(self, html: str, limit: int) -> List[Dict]:
        """Parse eBay HTML response"""
        listings = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find_all('li', class_='s-item', limit=limit)
            
            for item in items:
                try:
                    # Skip promoted/ad listings
                    if item.find('span', class_='PROMOTED'):
                        continue
                    
                    # Extract price
                    price_elem = item.find('span', class_='s-item__price')
                    if not price_elem:
                        continue
                        
                    price_text = price_elem.text.strip()
                    price_match = re.search(r'\$([\d,]+\.?\d*)', price_text)
                    if not price_match:
                        continue
                    
                    price = float(price_match.group(1).replace(',', ''))
                    
                    # Extract URL and title
                    link_elem = item.find('a', class_='s-item__link')
                    url = link_elem.get('href', '') if link_elem else ''
                    title = item.find('h3', class_='s-item__title')
                    title_text = title.text.strip() if title else ''
                    
                    # Extract condition
                    condition_elem = item.find('span', class_='SECONDARY_INFO')
                    condition = condition_elem.text.strip() if condition_elem else 'Used'
                    
                    # Extract shipping
                    shipping_elem = item.find('span', class_='s-item__shipping')
                    shipping = 0.0
                    if shipping_elem:
                        shipping_text = shipping_elem.text.strip()
                        shipping_match = re.search(r'\$([\d,]+\.?\d*)', shipping_text)
                        if shipping_match:
                            shipping = float(shipping_match.group(1).replace(',', ''))
                    
                    # Extract image
                    img_elem = item.find('img', class_='s-item__image-img')
                    image_url = img_elem.get('src', '') if img_elem else ''
                    
                    listing = {
                        'platform': 'eBay',
                        'title': title_text,
                        'price': price,
                        'url': url,
                        'condition': condition,
                        'image_url': image_url,
                        'seller': '',
                        'location': '',
                        'shipping': shipping,
                        'end_time': '',
                        'scraped_at': datetime.utcnow()
                    }
                    
                    if listing['price'] > 0 and listing['url']:
                        listings.append(listing)
                        
                except Exception as e:
                    logger.debug(f"Error parsing HTML item: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing HTML response: {str(e)}")
            
        return listings
    
    async def get_sold_items(
        self, 
        charm_name: str, 
        days: int = 90
    ) -> List[Dict]:
        """Get sold items for price history"""
        try:
            search_query = f"James Avery {charm_name} charm"
            params = {
                '_nkw': search_query,
                '_sacat': '0',
                'LH_Sold': '1',
                'LH_Complete': '1',
                '_udlo': '10',
                '_udhi': '500',
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.search_url, 
                    params=params, 
                    headers=headers
                ) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_sold_items(html, days)
                    return []
                    
        except Exception as e:
            logger.error(f"Error getting sold items: {str(e)}")
            return []
    
    def _parse_sold_items(self, html: str, days: int) -> List[Dict]:
        """Parse sold items from HTML"""
        sold_items = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            items = soup.find_all('li', class_='s-item', limit=50)
            
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            for item in items:
                try:
                    # Extract price
                    price_elem = item.find('span', class_='s-item__price')
                    if not price_elem:
                        continue
                        
                    price_text = price_elem.text.strip()
                    price_match = re.search(r'\$([\d,]+\.?\d*)', price_text)
                    if not price_match:
                        continue
                    
                    price = float(price_match.group(1).replace(',', ''))
                    
                    # Extract date (approximate from "Sold" text)
                    date_elem = item.find('span', class_='POSITIVE')
                    sale_date = datetime.utcnow()  # Default to now
                    
                    if date_elem and 'Sold' in date_elem.text:
                        # Try to extract date from text
                        date_text = date_elem.text.strip()
                        if 'hour' in date_text or 'minute' in date_text:
                            sale_date = datetime.utcnow()
                        elif 'day' in date_text:
                            days_ago = re.search(r'(\d+)', date_text)
                            if days_ago:
                                sale_date = datetime.utcnow() - timedelta(
                                    days=int(days_ago.group(1))
                                )
                    
                    if sale_date >= cutoff_date:
                        sold_items.append({
                            'date': sale_date,
                            'price': price,
                            'source': 'eBay'
                        })
                        
                except Exception as e:
                    logger.debug(f"Error parsing sold item: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing sold items: {str(e)}")
            
        return sold_items


# Initialize scraper instance
ebay_scraper = EbayScraper()