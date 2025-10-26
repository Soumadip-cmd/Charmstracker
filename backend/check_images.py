"""
Image Debug Script for CharmTracker
Checks what images are in database and tests if they load
Run with: python check_images.py
"""

import asyncio
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import aiohttp

load_dotenv()

async def check_images():
    print("=" * 60)
    print("CharmTracker - Image Debug Tool")
    print("=" * 60)
    print()
    
    # Connect to database
    mongo_url = os.getenv('MONGO_URL', 'mongodb://localhost:27017')
    db_name = os.getenv('DB_NAME', 'charmtracker_production')
    
    print(f"📡 Connecting to {db_name}...")
    client = AsyncIOMotorClient(mongo_url)
    db = client[db_name]
    
    # Get all charms
    charms = await db.charms.find({}).to_list(length=100)
    
    if not charms:
        print("❌ No charms found in database!")
        print("\n💡 Run: python dynamic_seed.py")
        client.close()
        return
    
    print(f"✅ Found {len(charms)} charms\n")
    
    # Check images for each charm
    print("🔍 Checking images...\n")
    
    issues_found = []
    
    for i, charm in enumerate(charms[:5], 1):  # Check first 5 charms
        print(f"[{i}/5] {charm['name']}")
        print(f"    Images: {len(charm.get('images', []))}")
        
        if not charm.get('images'):
            print("    ❌ No images in database!")
            issues_found.append(f"{charm['name']}: No images")
            continue
        
        # Show first image URL
        first_image = charm['images'][0]
        print(f"    URL: {first_image[:60]}...")
        
        # Check if it's a placeholder
        if 'placehold' in first_image:
            print("    ⚠️  Using placeholder image")
            issues_found.append(f"{charm['name']}: Placeholder images")
        elif 'jamesavery.com' in first_image:
            print("    ✅ Real James Avery image")
        elif 'ebay.com' in first_image or 'etsy.com' in first_image:
            print("    ✅ Marketplace image")
        else:
            print("    ⚠️  Unknown image source")
        
        # Try to fetch image
        try:
            async with aiohttp.ClientSession() as session:
                async with session.head(first_image, timeout=aiohttp.ClientTimeout(total=5)) as response:
                    if response.status == 200:
                        print("    ✅ Image is accessible")
                    else:
                        print(f"    ❌ Image returned status {response.status}")
                        issues_found.append(f"{charm['name']}: Image not accessible (status {response.status})")
        except Exception as e:
            print(f"    ❌ Could not fetch image: {str(e)[:50]}")
            issues_found.append(f"{charm['name']}: Could not fetch image")
        
        print()
    
    # Summary
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    
    if not issues_found:
        print("✅ All images look good!")
    else:
        print(f"⚠️  Found {len(issues_found)} issues:\n")
        for issue in issues_found:
            print(f"   • {issue}")
    
    print()
    
    # Recommendations
    if issues_found:
        print("💡 Recommendations:")
        print()
        
        has_placeholders = any('Placeholder' in i for i in issues_found)
        has_access_issues = any('not accessible' in i or 'Could not fetch' in i for i in issues_found)
        
        if has_placeholders:
            print("1. Placeholder images found - this is normal initially")
            print("   Run scraper to get real images:")
            print("   → PowerShell: Invoke-WebRequest -Uri 'http://localhost:8000/api/scraper/update-all' -Method POST")
            print("   → Or visit: http://localhost:8000/docs\n")
        
        if has_access_issues:
            print("2. Some images cannot be accessed")
            print("   This might be:")
            print("   • Firewall blocking placeholder.co")
            print("   • No internet connection")
            print("   • Images blocked by browser\n")
            print("   Try using real images from scrapers instead\n")
    
    else:
        print("💡 Your images are working!")
        print("   If they're not showing in browser:")
        print("   • Hard refresh: Ctrl + Shift + R")
        print("   • Check browser console (F12) for errors")
        print("   • Try different browser")
    
    print()
    client.close()

if __name__ == "__main__":
    try:
        asyncio.run(check_images())
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()