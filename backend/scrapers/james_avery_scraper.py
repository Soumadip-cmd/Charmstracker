"""
James Avery Website Scraper for CharmTracker
Fetches official product details, images, and retired status
"""

import logging
from typing import Dict, Optional, List
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import re

logger = logging.getLogger(__name__)


class JamesAveryScraper:
    """James Avery official website scraper"""
    
    def __init__(self):
        self.base_url = "https://www.jamesavery.com"
        self.search_url = f"{self.base_url}/search"
        
    async def get_charm_details(
        self, 
        charm_name: str
    ) -> Optional[Dict]:
        """
        Get official charm details from James Avery website
        Returns charm info including images, description, material, and status
        """
        try:
            # First, search for the charm
            search_results = await self._search_charm(charm_name)
            if not search_results:
                logger.info(f"No results found for {charm_name} on James Avery")
                return None
            
            # Get the first matching result
            product_url = search_results[0].get('url')
            if not product_url:
                return None
            
            # Fetch detailed product page
            product_details = await self._get_product_page(product_url)
            
            return product_details
            
        except Exception as e:
            logger.error(f"Error getting James Avery details for {charm_name}: {str(e)}")
            return None
    
    async def _search_charm(self, charm_name: str) -> List[Dict]:
        """Search James Avery website"""
        try:
            params = {
                'q': charm_name,
                'lang': 'default',
            }
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.search_url, 
                    params=params, 
                    headers=headers
                ) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_search_results(html)
                    return []
                    
        except Exception as e:
            logger.error(f"Error searching James Avery: {str(e)}")
            return []
    
    def _parse_search_results(self, html: str) -> List[Dict]:
        """Parse search results page"""
        results = []
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Find product tiles
            products = soup.find_all('div', class_=re.compile(r'product-tile'))
            
            for product in products:
                try:
                    # Extract URL
                    link = product.find('a', class_=re.compile(r'product-tile__link'))
                    if not link:
                        link = product.find('a', href=re.compile(r'/products/'))
                    
                    url = ''
                    if link:
                        url = link.get('href', '')
                        if url and not url.startswith('http'):
                            url = f"{self.base_url}{url}"
                    
                    # Extract title
                    title_elem = product.find('h3', class_=re.compile(r'product-tile__name'))
                    if not title_elem:
                        title_elem = product.find('a', class_=re.compile(r'product-tile__link'))
                    
                    title = title_elem.text.strip() if title_elem else ''
                    
                    # Extract image
                    img_elem = product.find('img')
                    image = ''
                    if img_elem:
                        image = img_elem.get('src', img_elem.get('data-src', ''))
                        if image and not image.startswith('http'):
                            image = f"{self.base_url}{image}"
                    
                    if url and title:
                        results.append({
                            'url': url,
                            'title': title,
                            'image': image
                        })
                        
                except Exception as e:
                    logger.debug(f"Error parsing search result: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error parsing search results: {str(e)}")
            
        return results
    
    async def _get_product_page(self, url: str) -> Optional[Dict]:
        """Fetch and parse product detail page"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers) as response:
                    if response.status == 200:
                        html = await response.text()
                        return self._parse_product_page(html, url)
                    return None
                    
        except Exception as e:
            logger.error(f"Error fetching product page: {str(e)}")
            return None
    
    def _parse_product_page(self, html: str, url: str) -> Optional[Dict]:
        """Parse product detail page"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Extract product name
            name_elem = soup.find('h1', class_=re.compile(r'product-name'))
            if not name_elem:
                name_elem = soup.find('h1')
            name = name_elem.text.strip() if name_elem else ''
            
            # Extract description
            desc_elem = soup.find('div', class_=re.compile(r'product-description'))
            if not desc_elem:
                desc_elem = soup.find('div', {'itemprop': 'description'})
            description = desc_elem.text.strip() if desc_elem else ''
            
            # Extract material
            material = 'Silver'  # Default
            material_elem = soup.find('span', class_=re.compile(r'material'))
            if material_elem:
                material_text = material_elem.text.lower()
                if 'gold' in material_text:
                    material = 'Gold'
            elif 'gold' in name.lower() or 'gold' in description.lower():
                material = 'Gold'
            
            # Check if retired
            is_retired = False
            status = 'Active'
            
            # Look for "retired" or "discontinued" text
            if 'retired' in html.lower() or 'discontinued' in html.lower():
                is_retired = True
                status = 'Retired'
            
            # Check for "out of stock" or "unavailable"
            availability_elem = soup.find('button', class_=re.compile(r'add-to-cart'))
            if availability_elem:
                button_text = availability_elem.text.lower()
                if 'unavailable' in button_text or 'out of stock' in button_text:
                    # Could be temporarily out of stock or retired
                    # Check elsewhere for confirmation
                    pass
            else:
                # No add to cart button might mean retired
                is_retired = True
                status = 'Retired'
            
            # Extract price
            price = None
            price_elem = soup.find('span', class_=re.compile(r'price-sales'))
            if not price_elem:
                price_elem = soup.find('span', {'itemprop': 'price'})
            
            if price_elem:
                price_text = price_elem.text.strip()
                price_match = re.search(r'\$([\d,]+\.?\d*)', price_text)
                if price_match:
                    price = float(price_match.group(1).replace(',', ''))
            
            # Extract images
            images = []
            
            # Try to find image gallery
            gallery = soup.find('div', class_=re.compile(r'product-carousel'))
            if not gallery:
                gallery = soup.find('div', class_=re.compile(r'product-images'))
            
            if gallery:
                img_elements = gallery.find_all('img')
                for img in img_elements:
                    img_url = img.get('src', img.get('data-src', ''))
                    if img_url and 'placeholder' not in img_url.lower():
                        if not img_url.startswith('http'):
                            img_url = f"{self.base_url}{img_url}"
                        images.append(img_url)
            
            # If no gallery, try main product image
            if not images:
                main_img = soup.find('img', class_=re.compile(r'product-image'))
                if not main_img:
                    main_img = soup.find('img', {'itemprop': 'image'})
                
                if main_img:
                    img_url = main_img.get('src', main_img.get('data-src', ''))
                    if img_url:
                        if not img_url.startswith('http'):
                            img_url = f"{self.base_url}{img_url}"
                        images.append(img_url)
            
            # Return structured data
            product_data = {
                'name': name,
                'description': description or f"Individual {name} charm from James Avery.",
                'material': material,
                'status': status,
                'is_retired': is_retired,
                'official_price': price,
                'images': images,
                'official_url': url,
                'scraped_at': datetime.utcnow()
            }
            
            return product_data if name else None
            
        except Exception as e:
            logger.error(f"Error parsing product page: {str(e)}")
            return None
    
    async def check_if_retired(self, charm_name: str) -> bool:
        """Quick check if a charm is retired"""
        try:
            details = await self.get_charm_details(charm_name)
            if details:
                return details.get('is_retired', False)
            return False
        except Exception as e:
            logger.error(f"Error checking retired status: {str(e)}")
            return False


# Initialize scraper instance
james_avery_scraper = JamesAveryScraper()