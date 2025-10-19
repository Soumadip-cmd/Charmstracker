"""
Seed script to populate CharmTracker database with sample data
Run with: python seed_data.py
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random
import os
from dotenv import load_dotenv
from pathlib import Path

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Sample charm data
CHARM_NAMES = [
    "Heart Lock Charm",
    "Birthstone Dangle",
    "Texas State Charm",
    "Cross with Stones",
    "Angel Wings Charm",
    "Peacock Detailed Charm",
    "Dolphin Charm",
    "Tree of Life",
    "Infinity Symbol",
    "Compass Rose",
    "Horseshoe Lucky Charm",
    "Musical Note",
    "Butterfly Garden",
    "Starfish Beach",
    "Celtic Knot",
    "Dragonfly Wings",
    "Moon and Stars",
    "Rose Flower",
    "Anchor Maritime",
    "Four Leaf Clover",
]

DESCRIPTIONS = [
    "Individual charm perfect for adding to your bracelet collection.",
    "Single decorative charm with intricate detailing, sold separately.",
    "Standalone charm piece designed to attach to bracelets or necklaces.",
    "Individual collectible charm with classic design and quality craftsmanship.",
    "Single charm featuring unique design, ideal for charm bracelets.",
    "Collectible individual charm with timeless appeal and fine detailing.",
    "Standalone decorative charm piece with symbolic meaning.",
    "Individual charm with artisan-quality craftsmanship and elegant design.",
]

MATERIALS = ["Silver", "Gold"]
STATUSES = ["Active", "Retired"]

# Image URLs from vision expert agent
CHARM_IMAGES = [
    "https://images.unsplash.com/photo-1749672197593-5682fde3702f",
    "https://images.unsplash.com/photo-1749672327818-2bf0797689dd",
    "https://images.unsplash.com/photo-1749672327814-f5eadb278229",
    "https://images.unsplash.com/photo-1758911995794-3eabd996bd3d",
    "https://images.unsplash.com/photo-1731531534571-91c2a59148d3",
    "https://images.unsplash.com/photo-1713004539634-a6694a83f3d9",
    "https://images.pexels.com/photos/8640988/pexels-photo-8640988.jpeg",
    "https://images.pexels.com/photos/25283498/pexels-photo-25283498.jpeg",
]


def generate_price_history(base_price: float, days: int = 90) -> list:
    """Generate realistic price history"""
    history = []
    current_date = datetime.utcnow() - timedelta(days=days)
    current_price = base_price * random.uniform(0.8, 0.95)
    
    for _ in range(days):
        # Add some variation to price
        price_change = random.uniform(-0.05, 0.05)
        current_price = current_price * (1 + price_change)
        current_price = max(current_price, base_price * 0.7)  # Don't go too low
        
        history.append({
            "date": current_date,
            "price": round(current_price, 2),
            "source": random.choice(["eBay", "Poshmark", "Etsy", "JamesAvery"])
        })
        
        current_date += timedelta(days=1)
    
    return history


def generate_listings(base_price: float, count: int = 5) -> list:
    """Generate sample listings"""
    platforms = ["eBay", "Poshmark", "Etsy", "JamesAvery"]
    conditions = ["New", "Like New", "Good", "Acceptable"]
    
    listings = []
    for _ in range(count):
        platform = random.choice(platforms)
        price = base_price * random.uniform(0.9, 1.2)
        
        listings.append({
            "platform": platform,
            "price": round(price, 2),
            "url": f"https://{platform.lower()}.com/item/{random.randint(10000, 99999)}",
            "condition": random.choice(conditions),
            "seller": f"seller_{random.randint(100, 999)}",
            "scraped_at": datetime.utcnow()
        })
    
    return listings


async def seed_database():
    """Populate database with sample charm data"""
    try:
        # Connect to MongoDB
        mongo_url = os.environ['MONGO_URL']
        client = AsyncIOMotorClient(mongo_url)
        db = client[os.environ['DB_NAME']]
        
        # Clear existing charms
        await db.charms.delete_many({})
        print("Cleared existing charms")
        
        # Generate and insert sample charms
        charms = []
        for i, name in enumerate(CHARM_NAMES):
            # Generate charm data
            material = random.choice(MATERIALS)
            status = random.choice(STATUSES)
            is_retired = status == "Retired"
            base_price = round(random.uniform(25.0, 150.0), 2)
            
            # Generate price history
            price_history = generate_price_history(base_price, days=90)
            
            # Calculate price changes
            recent_7d = price_history[-7:]
            recent_30d = price_history[-30:]
            
            price_change_7d = round(
                ((price_history[-1]["price"] - recent_7d[0]["price"]) / recent_7d[0]["price"]) * 100,
                1
            )
            price_change_30d = round(
                ((price_history[-1]["price"] - recent_30d[0]["price"]) / recent_30d[0]["price"]) * 100,
                1
            )
            price_change_90d = round(
                ((price_history[-1]["price"] - price_history[0]["price"]) / price_history[0]["price"]) * 100,
                1
            )
            
            # Generate listings
            listings = generate_listings(base_price, count=random.randint(3, 7))
            
            charm = {
                "id": f"charm_{i+1:03d}",
                "name": name,
                "description": random.choice(DESCRIPTIONS),
                "material": material,
                "status": status,
                "is_retired": is_retired,
                "avg_price": base_price,
                "price_history": price_history,
                "price_change_7d": price_change_7d,
                "price_change_30d": price_change_30d,
                "price_change_90d": price_change_90d,
                "popularity": random.randint(50, 100),
                "images": random.sample(CHARM_IMAGES, k=random.randint(2, 4)),
                "listings": listings,
                "related_charm_ids": [],
                "last_updated": datetime.utcnow(),
                "created_at": datetime.utcnow() - timedelta(days=random.randint(30, 365))
            }
            
            charms.append(charm)
        
        # Add related charm IDs
        for i, charm in enumerate(charms):
            # Add 2-4 related charms
            related_count = random.randint(2, 4)
            related_indices = random.sample(
                [j for j in range(len(charms)) if j != i],
                k=min(related_count, len(charms) - 1)
            )
            charm["related_charm_ids"] = [charms[j]["id"] for j in related_indices]
        
        # Insert all charms
        result = await db.charms.insert_many(charms)
        print(f"✅ Successfully seeded {len(result.inserted_ids)} charms")
        
        # Print summary statistics
        total = len(charms)
        active = sum(1 for c in charms if c["status"] == "Active")
        retired = sum(1 for c in charms if c["status"] == "Retired")
        avg_price = sum(c["avg_price"] for c in charms) / total
        
        print(f"\n📊 Database Summary:")
        print(f"   Total Charms: {total}")
        print(f"   Active: {active}")
        print(f"   Retired: {retired}")
        print(f"   Average Price: ${avg_price:.2f}")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        raise


if __name__ == "__main__":
    print("🌱 Starting database seed...")
    asyncio.run(seed_database())
    print("\n✅ Seed complete!")
