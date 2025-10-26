"""
Improved Seed Script for CharmTracker
Creates comprehensive charm database with proper placeholder images
Run with: python improved_seed.py
"""

import asyncio
import sys
from datetime import datetime, timedelta, timezone
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv
import random

load_dotenv()

# Comprehensive list of James Avery charms
COMPREHENSIVE_CHARMS = [
    # Religious & Spiritual
    {"name": "Cross Charm", "description": "Sterling silver cross charm with detailed design. Classic religious symbol.", "material": "Silver", "status": "Active"},
    {"name": "Angel Wings Charm", "description": "Detailed angel wing charm in sterling silver. Symbol of protection.", "material": "Silver", "status": "Retired"},
    {"name": "Praying Hands Charm", "description": "Delicate praying hands charm. Symbol of faith and devotion.", "material": "Silver", "status": "Active"},
    {"name": "Guardian Angel Charm", "description": "Protective guardian angel charm with wings spread.", "material": "Silver", "status": "Active"},
    {"name": "Miraculous Medal Charm", "description": "Traditional miraculous medal design in sterling silver.", "material": "Silver", "status": "Active"},
    
    # Hearts & Love
    {"name": "Heart Charm", "description": "Classic sterling silver heart charm. Perfect for expressing love.", "material": "Silver", "status": "Active"},
    {"name": "Double Heart Charm", "description": "Two intertwined hearts representing eternal love.", "material": "Silver", "status": "Active"},
    {"name": "Open Heart Charm", "description": "Open heart design symbolizing openness and love.", "material": "Silver", "status": "Active"},
    {"name": "Sweetheart Charm", "description": "Romantic sweetheart charm with intricate details.", "material": "Silver", "status": "Retired"},
    
    # Nature & Animals
    {"name": "Butterfly Charm", "description": "Delicate butterfly charm with intricate wing details.", "material": "Silver", "status": "Active"},
    {"name": "Dragonfly Charm", "description": "Delicate dragonfly charm with detailed wings.", "material": "Silver", "status": "Active"},
    {"name": "Dog Paw Charm", "description": "Adorable dog paw print charm. Great for pet lovers.", "material": "Silver", "status": "Active"},
    {"name": "Cat Charm", "description": "Playful cat charm with detailed features.", "material": "Silver", "status": "Active"},
    {"name": "Horse Charm", "description": "Majestic horse charm with flowing mane.", "material": "Silver", "status": "Active"},
    {"name": "Bird Charm", "description": "Delicate bird charm in flight.", "material": "Silver", "status": "Active"},
    {"name": "Hummingbird Charm", "description": "Tiny hummingbird charm with detailed feathers.", "material": "Silver", "status": "Active"},
    {"name": "Owl Charm", "description": "Wise owl charm with intricate details.", "material": "Silver", "status": "Active"},
    {"name": "Dolphin Charm", "description": "Playful dolphin charm with detailed design.", "material": "Silver", "status": "Active"},
    {"name": "Sea Turtle Charm", "description": "Detailed sea turtle charm. Symbol of longevity.", "material": "Silver", "status": "Active"},
    {"name": "Ladybug Charm", "description": "Lucky ladybug charm with spots.", "material": "Silver", "status": "Active"},
    {"name": "Bee Charm", "description": "Industrious bee charm with wings.", "material": "Silver", "status": "Active"},
    {"name": "Tree of Life Charm", "description": "Intricate tree of life design. Symbol of growth and connection.", "material": "Silver", "status": "Active"},
    {"name": "Rose Charm", "description": "Beautiful rose charm with detailed petals.", "material": "Silver", "status": "Retired"},
    {"name": "Flower Charm", "description": "Delicate flower charm with petals.", "material": "Silver", "status": "Active"},
    {"name": "Sunflower Charm", "description": "Bright sunflower charm with seeds and petals.", "material": "Silver", "status": "Active"},
    
    # Ocean & Beach
    {"name": "Seashell Charm", "description": "Beach-inspired seashell charm. Perfect for ocean lovers.", "material": "Silver", "status": "Active"},
    {"name": "Starfish Charm", "description": "Detailed starfish charm from the sea.", "material": "Silver", "status": "Active"},
    {"name": "Sand Dollar Charm", "description": "Delicate sand dollar charm with pattern.", "material": "Silver", "status": "Active"},
    {"name": "Anchor Charm", "description": "Nautical anchor charm. Symbol of hope and stability.", "material": "Silver", "status": "Active"},
    {"name": "Ship's Wheel Charm", "description": "Nautical ship's wheel charm.", "material": "Silver", "status": "Active"},
    
    # Celestial
    {"name": "Star Charm", "description": "Classic five-point star charm in sterling silver.", "material": "Silver", "status": "Active"},
    {"name": "Moon and Stars Charm", "description": "Celestial moon and stars charm. Perfect for dreamers.", "material": "Silver", "status": "Active"},
    {"name": "Crescent Moon Charm", "description": "Delicate crescent moon charm.", "material": "Silver", "status": "Active"},
    {"name": "Sun Charm", "description": "Radiant sun charm with rays.", "material": "Silver", "status": "Active"},
    
    # Symbols & Icons
    {"name": "Peace Sign Charm", "description": "Classic peace symbol charm. Timeless design.", "material": "Silver", "status": "Active"},
    {"name": "Infinity Symbol Charm", "description": "Elegant infinity symbol in sterling silver.", "material": "Silver", "status": "Active"},
    {"name": "Yin Yang Charm", "description": "Balance symbol yin yang charm.", "material": "Silver", "status": "Active"},
    {"name": "Key Charm", "description": "Vintage key charm with intricate design.", "material": "Silver", "status": "Active"},
    {"name": "Lock and Key Charm", "description": "Matching lock and key set.", "material": "Silver", "status": "Active"},
    {"name": "Crown Charm", "description": "Royal crown charm with jeweled details.", "material": "Silver", "status": "Retired"},
    
    # Lucky Charms
    {"name": "Horseshoe Charm", "description": "Lucky horseshoe charm with detailed design.", "material": "Silver", "status": "Retired"},
    {"name": "Four Leaf Clover Charm", "description": "Lucky four leaf clover charm in sterling silver.", "material": "Silver", "status": "Active"},
    {"name": "Wishbone Charm", "description": "Lucky wishbone charm.", "material": "Silver", "status": "Active"},
    {"name": "Elephant Charm", "description": "Lucky elephant charm with trunk up.", "material": "Silver", "status": "Active"},
    
    # Celtic & Cultural
    {"name": "Celtic Knot Charm", "description": "Traditional Celtic knot design in sterling silver.", "material": "Silver", "status": "Retired"},
    {"name": "Trinity Knot Charm", "description": "Irish trinity knot charm.", "material": "Silver", "status": "Active"},
    {"name": "Claddagh Charm", "description": "Irish Claddagh ring design charm.", "material": "Silver", "status": "Active"},
    
    # Music & Arts
    {"name": "Musical Note Charm", "description": "Music note charm. Perfect for music lovers.", "material": "Silver", "status": "Active"},
    {"name": "Treble Clef Charm", "description": "Treble clef music symbol charm.", "material": "Silver", "status": "Active"},
    {"name": "Guitar Charm", "description": "Detailed guitar charm for musicians.", "material": "Silver", "status": "Active"},
    {"name": "Piano Charm", "description": "Miniature piano charm with keys.", "material": "Silver", "status": "Retired"},
    {"name": "Dance Shoes Charm", "description": "Ballet or dance shoes charm.", "material": "Silver", "status": "Active"},
    
    # Travel & Adventure
    {"name": "Compass Charm", "description": "Working compass charm. Symbol of guidance and direction.", "material": "Silver", "status": "Active"},
    {"name": "Globe Charm", "description": "World globe charm for travelers.", "material": "Silver", "status": "Active"},
    {"name": "Airplane Charm", "description": "Airplane charm for travel lovers.", "material": "Silver", "status": "Active"},
    {"name": "Passport Charm", "description": "Miniature passport charm.", "material": "Silver", "status": "Active"},
    {"name": "Suitcase Charm", "description": "Vintage suitcase charm for adventurers.", "material": "Silver", "status": "Active"},
    
    # Sports & Hobbies
    {"name": "Baseball Charm", "description": "Baseball charm with stitching detail.", "material": "Silver", "status": "Active"},
    {"name": "Football Charm", "description": "Football charm for sports fans.", "material": "Silver", "status": "Active"},
    {"name": "Soccer Ball Charm", "description": "Soccer ball charm with pentagon pattern.", "material": "Silver", "status": "Active"},
    {"name": "Tennis Racket Charm", "description": "Tennis racket charm for players.", "material": "Silver", "status": "Active"},
    {"name": "Golf Bag Charm", "description": "Golf bag charm with clubs.", "material": "Silver", "status": "Retired"},
    
    # Food & Drink
    {"name": "Coffee Cup Charm", "description": "Steaming coffee cup charm.", "material": "Silver", "status": "Active"},
    {"name": "Wine Glass Charm", "description": "Elegant wine glass charm.", "material": "Silver", "status": "Active"},
    {"name": "Cupcake Charm", "description": "Sweet cupcake charm with frosting.", "material": "Silver", "status": "Active"},
    {"name": "Apple Charm", "description": "Detailed apple charm.", "material": "Silver", "status": "Active"},
    
    # Celebrations
    {"name": "Birthday Cake Charm", "description": "Birthday cake charm with candles.", "material": "Silver", "status": "Active"},
    {"name": "Champagne Bottle Charm", "description": "Celebration champagne bottle.", "material": "Silver", "status": "Active"},
    {"name": "Graduation Cap Charm", "description": "Graduation cap charm for grads.", "material": "Silver", "status": "Active"},
    {"name": "Wedding Bells Charm", "description": "Wedding bells charm for brides.", "material": "Silver", "status": "Active"},
    
    # Everyday Objects
    {"name": "Book Charm", "description": "Open book charm for readers.", "material": "Silver", "status": "Active"},
    {"name": "Camera Charm", "description": "Vintage camera charm for photographers.", "material": "Silver", "status": "Active"},
    {"name": "Bicycle Charm", "description": "Detailed bicycle charm.", "material": "Silver", "status": "Active"},
    {"name": "Umbrella Charm", "description": "Open umbrella charm.", "material": "Silver", "status": "Active"},
    {"name": "Mailbox Charm", "description": "Vintage mailbox charm.", "material": "Silver", "status": "Retired"},
    
    # Texas & Western
    {"name": "Texas Charm", "description": "Texas state charm with star.", "material": "Silver", "status": "Active"},
    {"name": "Cowboy Boot Charm", "description": "Western cowboy boot charm.", "material": "Silver", "status": "Active"},
    {"name": "Cowboy Hat Charm", "description": "Western cowboy hat charm.", "material": "Silver", "status": "Active"},
    {"name": "Longhorn Charm", "description": "Texas longhorn charm.", "material": "Silver", "status": "Active"},
    
    # Seasonal
    {"name": "Snowflake Charm", "description": "Delicate snowflake charm.", "material": "Silver", "status": "Active"},
    {"name": "Pumpkin Charm", "description": "Halloween pumpkin charm.", "material": "Silver", "status": "Active"},
    {"name": "Christmas Tree Charm", "description": "Festive Christmas tree charm.", "material": "Silver", "status": "Active"},
]


def generate_proper_placeholder_image(charm_name):
    """
    Generate a meaningful placeholder URL based on charm category
    Uses a better strategy than random images
    """
    name_lower = charm_name.lower()
    
    # Map charm names to appropriate placeholder categories
    if any(word in name_lower for word in ['cross', 'angel', 'pray', 'guardian', 'medal']):
        category = "faith"
    elif any(word in name_lower for word in ['heart', 'love', 'sweetheart']):
        category = "love"
    elif any(word in name_lower for word in ['butterfly', 'bird', 'owl', 'bee', 'dragonfly']):
        category = "nature"
    elif any(word in name_lower for word in ['dog', 'cat', 'horse', 'dolphin', 'elephant']):
        category = "animals"
    elif any(word in name_lower for word in ['shell', 'anchor', 'star', 'turtle', 'dolphin']):
        category = "ocean"
    elif any(word in name_lower for word in ['star', 'moon', 'sun', 'celestial']):
        category = "celestial"
    elif any(word in name_lower for word in ['flower', 'rose', 'tree', 'sunflower']):
        category = "botanical"
    elif any(word in name_lower for word in ['music', 'guitar', 'piano', 'note']):
        category = "music"
    else:
        category = "jewelry"
    
    # Use a charm-specific identifier
    charm_id = charm_name.replace(' ', '-').lower()
    
    # Return a generic jewelry placeholder that won't confuse users
    # This should be replaced by real images from scrapers
    return f"https://via.placeholder.com/400x400/silver/white?text={charm_name.replace(' ', '+')}"


def generate_placeholder_images(charm_name):
    """
    Generate 4 placeholder image URLs
    These are meant to be replaced by scrapers with real James Avery images
    """
    base_url = generate_proper_placeholder_image(charm_name)
    
    # Generate slight variations
    images = []
    colors = ["C0C0C0", "D3D3D3", "E8E8E8", "F5F5F5"]  # Silver shades
    
    for i, color in enumerate(colors):
        encoded_name = charm_name.replace(' ', '+')
        url = f"https://via.placeholder.com/400x400/{color}/666666?text={encoded_name}"
        images.append(url)
    
    return images


def generate_price_history(avg_price, days=90):
    """Generate realistic price history"""
    history = []
    current_date = datetime.now(timezone.utc) - timedelta(days=days)
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
    """Generate sample marketplace listings"""
    platforms = ['eBay', 'Etsy', 'Poshmark', 'Mercari']
    conditions = ['New', 'Like New', 'Pre-owned', 'Good']
    
    listings = []
    for _ in range(random.randint(5, 15)):
        platform = random.choice(platforms)
        price = avg_price * random.uniform(0.8, 1.3)
        
        listings.append({
            'platform': platform,
            'title': f"{charm_name} - James Avery Sterling Silver",
            'price': round(price, 2),
            'url': f"https://www.example.com/{platform.lower()}/listing/{random.randint(1000, 9999)}",
            'condition': random.choice(conditions),
            'image_url': '',
            'seller': f"seller{random.randint(100, 999)}",
            'shipping': round(random.uniform(0, 8), 2),
            'scraped_at': datetime.now(timezone.utc)
        })
    
    return listings


async def seed_database():
    """Seed the database with comprehensive charm data"""
    
    print("=" * 80)
    print("CharmTracker - Comprehensive Seed Script")
    print("=" * 80)
    print()
    
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        print("❌ Error: MONGO_URL not found in environment variables")
        print("Please create a .env file with MONGO_URL")
        return
    
    print("📡 Connecting to database...")
    client = AsyncIOMotorClient(mongo_url)
    db_name = os.environ.get('DB_NAME', 'charmtracker_production')
    db = client[db_name]
    print(f"✅ Connected to database: {db_name}")
    print()
    
    print("🗑️  Clearing existing charms...")
    await db.charms.delete_many({})
    print("✅ Database cleared")
    print()
    
    print(f"🌱 Seeding {len(COMPREHENSIVE_CHARMS)} charms...")
    print("   (Placeholders will be replaced by scrapers with real images)")
    print()
    
    inserted_count = 0
    
    for i, charm_data in enumerate(COMPREHENSIVE_CHARMS, 1):
        charm_id = f"charm_{charm_data['name'].lower().replace(' ', '_').replace('/', '_')}"
        
        # Generate pricing data
        base_price = random.uniform(25, 80)
        avg_price = round(base_price, 2)
        price_history = generate_price_history(avg_price)
        listings = generate_sample_listings(charm_data['name'], avg_price)
        
        # Calculate price changes
        price_7d_ago = price_history[-7]['price'] if len(price_history) >= 7 else avg_price
        price_30d_ago = price_history[-30]['price'] if len(price_history) >= 30 else avg_price
        price_90d_ago = price_history[0]['price'] if len(price_history) >= 90 else avg_price
        
        price_change_7d = round(((avg_price - price_7d_ago) / price_7d_ago) * 100, 1)
        price_change_30d = round(((avg_price - price_30d_ago) / price_30d_ago) * 100, 1)
        price_change_90d = round(((avg_price - price_90d_ago) / price_90d_ago) * 100, 1)
        
        # Generate placeholder images
        placeholder_images = generate_placeholder_images(charm_data['name'])
        
        # Create charm document
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
            'images': placeholder_images,
            'listings': listings,
            'price_history': price_history,
            'related_charm_ids': [],
            'last_updated': datetime.now(timezone.utc),
            'created_at': datetime.now(timezone.utc),
            'needs_image_update': True,
            'needs_scraper_update': True
        }
        
        await db.charms.insert_one(charm)
        inserted_count += 1
        
        if i % 10 == 0:
            print(f"[{i}/{len(COMPREHENSIVE_CHARMS)}] Seeded {i} charms...")
    
    print(f"\n✅ Seeded all {inserted_count} charms")
    print()
    
    print("🔗 Adding related charm relationships...")
    all_charms = await db.charms.find({}).to_list(length=2000)
    
    for charm in all_charms:
        other_charms = [c for c in all_charms if c['id'] != charm['id']]
        related_count = min(random.randint(3, 6), len(other_charms))
        related = random.sample(other_charms, k=related_count)
        related_ids = [c['id'] for c in related]
        
        await db.charms.update_one(
            {'id': charm['id']},
            {'$set': {'related_charm_ids': related_ids}}
        )
    
    print("✅ Related charm relationships added")
    print()
    
    # Summary
    print("=" * 80)
    print("📊 Seeding Summary")
    print("=" * 80)
    print(f"✅ Successfully seeded: {inserted_count} charms")
    print(f"📦 Total in database: {await db.charms.count_documents({})}")
    print()
    
    # Show sample
    sample = await db.charms.find_one({})
    if sample:
        print(f"🔍 Sample charm: {sample['name']}")
        print(f"   Price: ${sample['avg_price']}")
        print(f"   Status: {sample['status']}")
        print(f"   Images: {len(sample['images'])} (placeholder)")
        print(f"   Listings: {len(sample['listings'])}")
    
    print()
    print("=" * 80)
    print("✅ Database seeding complete!")
    print("=" * 80)
    print()
    print("💡 Next steps:")
    print("   1. Start backend: python server.py")
    print("   2. Start frontend: cd frontend && npm start")
    print("   3. Visit: http://localhost:3000")
    print()
    print("🔄 To get REAL James Avery images:")
    print("   • Visit: http://localhost:8000/docs")
    print("   • Find: POST /api/scraper/update-all")
    print("   • Click: Try it out → Execute")
    print()
    print("   Or use PowerShell:")
    print('   Invoke-WebRequest -Uri "http://localhost:8000/api/scraper/update-all" -Method POST')
    print()
    print(f"   The scrapers will replace placeholder images with real ones from:")
    print("   - James Avery official website")
    print("   - eBay marketplace")
    print("   - Etsy marketplace")
    print("   - Poshmark marketplace")
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