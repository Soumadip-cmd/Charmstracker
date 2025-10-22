"""
Seed initial charms database from James Avery catalog
Run this to populate your database with charms
"""

import asyncio
import os
import sys
import logging

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import from local modules
try:
    from database import get_database
except ImportError:
    # Try alternative import
    from backend.database import get_database

try:
    from scrapers.james_avery_scraper import JamesAveryScraper
except ImportError:
    # Scraper might not exist yet, that's okay
    JamesAveryScraper = None

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def seed_initial_charms():
    """Populate database with James Avery catalog"""
    try:
        logger.info("🔄 Connecting to database...")
        db = await get_database()
        
        # Use sample charms since scraper might not be ready
        logger.info("💡 Inserting sample charms for testing...")
        charms = get_sample_charms()
        
        logger.info(f"📦 Found {len(charms)} charms to insert")
        
        inserted_count = 0
        updated_count = 0
        
        for charm in charms:
            result = await db.charms.update_one(
                {"name": charm["name"]},
                {"$set": charm},
                upsert=True
            )
            if result.upserted_id:
                inserted_count += 1
            elif result.modified_count > 0:
                updated_count += 1
        
        logger.info(f"✅ Database seeded successfully!")
        logger.info(f"   New charms: {inserted_count}")
        logger.info(f"   Updated charms: {updated_count}")
        
        # Verify
        total_charms = await db.charms.count_documents({})
        logger.info(f"📊 Total charms in database: {total_charms}")
        
        # Show sample of charms
        sample = await db.charms.find_one({})
        if sample:
            logger.info(f"📝 Sample charm: {sample.get('name', 'Unknown')}")
        
    except Exception as e:
        logger.error(f"❌ Error seeding database: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def get_sample_charms():
    """Get sample charms for testing"""
    from datetime import datetime
    
    return [
        {
            "name": "Cross Charm",
            "description": "Sterling silver cross charm with detailed design",
            "category": "Religious",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 28.50,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 28.50,
                    "min": 22.00,
                    "max": 35.00,
                    "count": 10
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/83000-0002-0.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/cross-charm",
            "lastUpdated": datetime.utcnow(),
            "popularity": 85,
            "tags": ["religious", "classic", "popular"]
        },
        {
            "name": "Heart Charm",
            "description": "Classic sterling silver heart charm",
            "category": "Love",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 35.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 35.00,
                    "min": 28.00,
                    "max": 42.00,
                    "count": 15
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/heart-charm.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/heart-charm",
            "lastUpdated": datetime.utcnow(),
            "popularity": 92,
            "tags": ["love", "valentine", "popular"]
        },
        {
            "name": "Angel Wing Charm",
            "description": "Detailed angel wing in sterling silver",
            "category": "Religious",
            "material": "Sterling Silver",
            "retired": True,
            "averagePrice": 42.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 42.00,
                    "min": 35.00,
                    "max": 50.00,
                    "count": 8
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/angel-wing.jpg",
            "jamesAveryUrl": None,
            "lastUpdated": datetime.utcnow(),
            "popularity": 78,
            "tags": ["religious", "retired", "collectible"]
        },
        {
            "name": "Butterfly Charm",
            "description": "Delicate butterfly charm with intricate details",
            "category": "Nature",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 31.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 31.00,
                    "min": 25.00,
                    "max": 38.00,
                    "count": 12
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/butterfly-charm.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/butterfly",
            "lastUpdated": datetime.utcnow(),
            "popularity": 88,
            "tags": ["nature", "butterfly", "spring"]
        },
        {
            "name": "Seashell Charm",
            "description": "Beach-inspired seashell charm",
            "category": "Nature",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 27.50,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 27.50,
                    "min": 22.00,
                    "max": 33.00,
                    "count": 9
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/seashell-charm.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/seashell",
            "lastUpdated": datetime.utcnow(),
            "popularity": 75,
            "tags": ["beach", "summer", "nature"]
        },
        {
            "name": "Dog Paw Charm",
            "description": "Adorable dog paw print charm",
            "category": "Animals",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 33.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 33.00,
                    "min": 28.00,
                    "max": 40.00,
                    "count": 14
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/dog-paw-charm.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/dog-paw",
            "lastUpdated": datetime.utcnow(),
            "popularity": 90,
            "tags": ["pets", "dog", "animals"]
        },
        {
            "name": "Star Charm",
            "description": "Classic five-point star charm",
            "category": "Symbols",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 29.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 29.00,
                    "min": 24.00,
                    "max": 35.00,
                    "count": 11
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/star-charm.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/star",
            "lastUpdated": datetime.utcnow(),
            "popularity": 82,
            "tags": ["star", "celestial", "classic"]
        },
        {
            "name": "Vintage Rose Charm",
            "description": "Retired rose charm with vintage design",
            "category": "Nature",
            "material": "Sterling Silver",
            "retired": True,
            "averagePrice": 45.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 45.00,
                    "min": 38.00,
                    "max": 55.00,
                    "count": 6
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/rose-charm.jpg",
            "jamesAveryUrl": None,
            "lastUpdated": datetime.utcnow(),
            "popularity": 95,
            "tags": ["rose", "retired", "vintage", "rare"]
        },
        {
            "name": "Anchor Charm",
            "description": "Nautical anchor charm",
            "category": "Nautical",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 30.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 30.00,
                    "min": 25.00,
                    "max": 36.00,
                    "count": 10
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/anchor-charm.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/anchor",
            "lastUpdated": datetime.utcnow(),
            "popularity": 80,
            "tags": ["nautical", "anchor", "beach"]
        },
        {
            "name": "Peace Sign Charm",
            "description": "Classic peace symbol charm",
            "category": "Symbols",
            "material": "Sterling Silver",
            "retired": False,
            "averagePrice": 26.00,
            "priceHistory": [
                {
                    "date": datetime.utcnow().isoformat(),
                    "average": 26.00,
                    "min": 20.00,
                    "max": 32.00,
                    "count": 8
                }
            ],
            "imageUrl": "https://www.jamesavery.com/medias/peace-sign-charm.jpg",
            "jamesAveryUrl": "https://www.jamesavery.com/products/peace-sign",
            "lastUpdated": datetime.utcnow(),
            "popularity": 77,
            "tags": ["peace", "symbol", "classic"]
        }
    ]


if __name__ == "__main__":
    print("=" * 60)
    print("CharmTracker - Database Seed Script")
    print("=" * 60)
    print()
    
    asyncio.run(seed_initial_charms())
    
    print()
    print("=" * 60)
    print("✅ Seeding complete! You can now start your backend server.")
    print("=" * 60)