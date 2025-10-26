"""
Dynamic Seed Script for CharmTracker
Creates charms with placeholder images that can be replaced with real scraped images
Run with: python dynamic_seed.py
"""

import asyncio
import sys
from datetime import datetime, timedelta
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

# Sample charm data (no hardcoded images!)
SAMPLE_CHARMS = [
    {
        "name": "Cross Charm",
        "description": "Sterling silver cross charm with detailed design. Classic religious symbol.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Heart Charm",
        "description": "Classic sterling silver heart charm. Perfect for expressing love.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Angel Wings Charm",
        "description": "Detailed angel wing charm in sterling silver. Symbol of protection.",
        "material": "Silver",
        "status": "Retired",
    },
    {
        "name": "Butterfly Charm",
        "description": "Delicate butterfly charm with intricate wing details.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Seashell Charm",
        "description": "Beach-inspired seashell charm. Perfect for ocean lovers.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Dog Paw Charm",
        "description": "Adorable dog paw print charm. Great for pet lovers.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Star Charm",
        "description": "Classic five-point star charm in sterling silver.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Rose Charm",
        "description": "Beautiful rose charm with detailed petals.",
        "material": "Silver",
        "status": "Retired",
    },
    {
        "name": "Anchor Charm",
        "description": "Nautical anchor charm. Symbol of hope and stability.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Peace Sign Charm",
        "description": "Classic peace symbol charm. Timeless design.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Tree of Life Charm",
        "description": "Intricate tree of life design. Symbol of growth and connection.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Infinity Symbol Charm",
        "description": "Elegant infinity symbol in sterling silver.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Horseshoe Charm",
        "description": "Lucky horseshoe charm with detailed design.",
        "material": "Silver",
        "status": "Retired",
    },
    {
        "name": "Four Leaf Clover Charm",
        "description": "Lucky four leaf clover charm in sterling silver.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Moon and Stars Charm",
        "description": "Celestial moon and stars charm. Perfect for dreamers.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Dragonfly Charm",
        "description": "Delicate dragonfly charm with detailed wings.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Celtic Knot Charm",
        "description": "Traditional Celtic knot design in sterling silver.",
        "material": "Silver",
        "status": "Retired",
    },
    {
        "name": "Musical Note Charm",
        "description": "Music note charm. Perfect for music lovers.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Compass Charm",
        "description": "Working compass charm. Symbol of guidance and direction.",
        "material": "Silver",
        "status": "Active",
    },
    {
        "name": "Dolphin Charm",
        "description": "Playful dolphin charm with detailed design.",
        "material": "Silver",
        "status": "Active",
    },
]


def generate_placeholder_images(charm_name):
    """
    Generate placeholder image URLs that can be replaced by scrapers
    Uses a generic placeholder service that shows the charm name
    """
    # Use placeholder.com with charm name
    # These will be replaced when scrapers find real images
    base_url = "https://placehold.co/400x400"
    
    # Create 4 placeholder images with different backgrounds
    colors = ["CCCCCC", "DDDDDD", "EEEEEE", "F0F0F0"]
    images = []
    
    for i, color in enumerate(colors):
        # URL format: https://placehold.co/400x400/CCCCCC/333333?text=Charm+Name
        encoded_name = charm_name.replace(' ', '+')
        url = f"{base_url}/{color}/333333?text={encoded_name}"
        images.append(url)
    
    return images


def generate_price_history(avg_price, days=90):
    """Generate realistic price history"""
    history = []
    current_date = datetime.utcnow() - timedelta(days=days)
    current_price = avg_price * random.uniform(0.85, 0.95)
    
    for _ in range(days):
        price_change = random.uniform(-0.03, 0.03)
        current_price = current_price * (1 + price_change)
        current_price = max(current_price, avg_price * 0.7)
        
        history.append({
            'date': current_date,
            'price': round(current_price, 2),
            'source': 'aggregated',
            'listing_count': random.randint(5, 20)
        })
        
        current_date += timedelta(days=1)
    
    return history


def generate_sample_listings(charm_name, avg_price):
    """
    Generate sample marketplace listings with placeholder data
    These will be replaced when scrapers run
    """
    platforms = ['eBay', 'Etsy', 'Poshmark', 'Mercari']
    conditions = ['New', 'Like New', 'Pre-owned', 'Good']
    
    listings = []
    for _ in range(random.randint(5, 15)):
        platform = random.choice(platforms)
        price = avg_price * random.uniform(0.8, 1.3)
        
        listings.append({
            'platform': platform,
            'title': f"{charm_name} - James Avery",
            'price': round(price, 2),
            'url': f"https://www.example.com/{platform.lower()}/listing",
            'condition': random.choice(conditions),
            'image_url': '',  # Will be filled by scrapers
            'seller': f"seller{random.randint(100, 999)}",
            'shipping': round(random.uniform(0, 8), 2),
            'scraped_at': datetime.utcnow()
        })
    
    return listings


async def seed_database():
    """Seed the database with charms using placeholder images"""
    
    print("=" * 60)
    print("CharmTracker - Dynamic Seed Script")
    print("=" * 60)
    print()
    
    # Connect to MongoDB
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        print("❌ Error: MONGO_URL not found in environment variables")
        print("Make sure you have a .env file with MONGO_URL set")
        return
    
    print("📡 Connecting to database...")
    client = AsyncIOMotorClient(mongo_url)
    db_name = os.environ.get('DB_NAME', 'charmtracker')
    db = client[db_name]
    print(f"✅ Connected to database: {db_name}")
    print()
    
    # Clear existing charms
    print("🗑️  Clearing existing charms...")
    await db.charms.delete_many({})
    print("✅ Database cleared")
    print()
    
    # Seed charms
    print(f"🌱 Seeding {len(SAMPLE_CHARMS)} charms with placeholder images...")
    print("   (Scrapers will replace with real images when they run)")
    print()
    
    inserted_count = 0
    
    for i, charm_data in enumerate(SAMPLE_CHARMS, 1):
        charm_id = f"charm_{charm_data['name'].lower().replace(' ', '_')}"
        
        # Generate random price and data
        avg_price = round(random.uniform(25, 80), 2)
        price_history = generate_price_history(avg_price)
        listings = generate_sample_listings(charm_data['name'], avg_price)
        
        # Calculate price changes
        price_7d_ago = price_history[-7]['price'] if len(price_history) >= 7 else avg_price
        price_30d_ago = price_history[-30]['price'] if len(price_history) >= 30 else avg_price
        price_90d_ago = price_history[0]['price'] if len(price_history) >= 90 else avg_price
        
        price_change_7d = round(((avg_price - price_7d_ago) / price_7d_ago) * 100, 1)
        price_change_30d = round(((avg_price - price_30d_ago) / price_30d_ago) * 100, 1)
        price_change_90d = round(((avg_price - price_90d_ago) / price_90d_ago) * 100, 1)
        
        # Generate placeholder images (will be replaced by scrapers)
        placeholder_images = generate_placeholder_images(charm_data['name'])
        
        # Create full charm document
        charm = {
            'id': charm_id,
            'name': charm_data['name'],
            'description': charm_data['description'],
            'material': charm_data['material'],
            'status': charm_data['status'],
            'is_retired': charm_data['status'] == 'Retired',
            'avg_price': avg_price,
            'price_change_7d': price_change_7d,
            'price_change_30d': price_change_30d,
            'price_change_90d': price_change_90d,
            'popularity': random.randint(60, 98),
            'images': placeholder_images,  # Placeholder images
            'listings': listings,
            'price_history': price_history,
            'related_charm_ids': [],
            'last_updated': datetime.utcnow(),
            'created_at': datetime.utcnow(),
            # Flag to indicate images need updating from scrapers
            'needs_image_update': True
        }
        
        # Insert into database
        await db.charms.insert_one(charm)
        inserted_count += 1
        
        print(f"[{i}/{len(SAMPLE_CHARMS)}] ✅ Seeded: {charm_data['name']} (${avg_price})")
    
    print()
    print("🔗 Adding related charm relationships...")
    
    # Add related charm IDs
    all_charms = await db.charms.find({}).to_list(length=1000)
    
    for charm in all_charms:
        other_charms = [c for c in all_charms if c['id'] != charm['id']]
        related_count = min(random.randint(2, 4), len(other_charms))
        related = random.sample(other_charms, k=related_count)
        related_ids = [c['id'] for c in related]
        
        await db.charms.update_one(
            {'id': charm['id']},
            {'$set': {'related_charm_ids': related_ids}}
        )
    
    print("✅ Related charm relationships added")
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Seeding Summary")
    print("=" * 60)
    print(f"✅ Successfully seeded: {inserted_count} charms")
    print(f"📦 Total in database: {await db.charms.count_documents({})}")
    print()
    
    # Show sample
    sample = await db.charms.find_one({})
    if sample:
        print(f"📝 Sample charm: {sample['name']}")
        print(f"   Price: ${sample['avg_price']}")
        print(f"   Status: {sample['status']}")
        print(f"   Images: {len(sample['images'])} (placeholder)")
        print(f"   Listings: {len(sample['listings'])}")
    
    print()
    print("=" * 60)
    print("✅ Database seeding complete!")
    print("=" * 60)
    print()
    print("💡 Next steps:")
    print("   1. Start backend: python server.py")
    print("   2. Start frontend: cd frontend && npm start")
    print("   3. Visit: http://localhost:3000")
    print()
    print("🔄 To get REAL images and data:")
    print("   The scrapers will automatically run and update:")
    print("   - Real images from James Avery website")
    print("   - Live listings from eBay, Etsy, Poshmark")
    print("   - Current market prices")
    print()
    print("   Or trigger manual update:")
    print("   curl -X POST http://localhost:8000/api/scraper/update-all")
    print()
    print("   The scrapers run automatically every 6 hours!")
    print()
    
    client.close()


if __name__ == "__main__":
    try:
        asyncio.run(seed_database())
    except KeyboardInterrupt:
        print("\n⚠️  Seeding interrupted by user")
    except Exception as e:
        print(f"\n❌ Seeding failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)