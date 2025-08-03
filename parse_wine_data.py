#!/usr/bin/env python3
"""
Parse actual Mollydooker wine data from scraped page content
"""

import csv
import re

# Actual page content from the wine shop
page_content = """Skip to Content
MENU
CLOSE
SHOP WINES
CELLAR DOOR
MOLLYCLUB
EVENTS
AUS
USA
Log in
Cart
0
WINES FOR ALL
SHOP WINES
LEFTY WINES
FUN WINES
FAMILY WINES
LOVE WINES
VELVET GLOVE
LARGE FORMAT
EVENT TICKETS
LEFTY WINES
Quick View - The Violinist
2024
THE VIOLINIST
VERDELHO
$32
SOLD OUT
Quick View - The Scooter
2023
THE SCOOTER
MERLOT
$32
Quantity
ADD TO CART
Quick View - The Maitre D'
2022
THE MAITRE D'
CABERNET SAUVIGNON
$32
Quantity
ADD TO CART
Quick View - Two Left Feet
2022
TWO LEFT FEET
SHIRAZ / MERLOT / CABERNET
$32
Quantity
ADD TO CART
Quick View - The Boxer
2023
THE BOXER
SHIRAZ
$32
Quantity
ADD TO CART
Quick View - Miss Molly
2023
MISS MOLLY
SPARKLING SHIRAZ
$32
Quantity
ADD TO CART
Quick View - Winemaker Dozen
2023
WINEMAKER DOZEN
MIXED VARIETY
$550
Quantity
ADD TO CART
Quick View - 'Dooker Gift Card
'DOOKER GIFT CARD
$50-$1,000
Options
$50
$75
$100
$150
$200
$250
$500
$750
$1000
Recipient Email
Add gift message
ADD TO CART
FUN WINES
Quick View - Euphoria
2024
EUPHORIA
SPARKLING VERDELHO
$27
Quantity
ADD TO CART
Quick View - Summer of '69
2024
SUMMER OF '69
'EARLY PICK' VERDELHO
$27
Quantity
ADD TO CART
Quick View - Serenity
2024
SERENITY
MERLOT ROSÉ
$27
SOLD OUT
FAMILY WINES
Quick View - Gigglepot
2023
GIGGLEPOT
CABERNET SAUVIGNON
$65
Quantity
ADD TO CART
Quick View - Blue Eyed Boy
2022
BLUE EYED BOY
SHIRAZ
$65
Quantity
ADD TO CART
Quick View - The Family Collection
THE FAMILY COLLECTION
SHIRAZ & CABERNET SAUVIGNON
$500
Quantity
ADD TO CART
LOVE WINES
Quick View - Enchanted Path
2022
ENCHANTED PATH
SHIRAZ / CABERNET SAUVIGNON
$95
Quantity
ADD TO CART
Quick View - Carnival of Love
2022
CARNIVAL OF LOVE
SHIRAZ
$95
Quantity
ADD TO CART
VELVET GLOVE
Quick View - Velvet Glove
2022
VELVET GLOVE
SHIRAZ
$230

This product is only available to club members. Please log in to purchase.

LOGIN
LARGE FORMATS
Quick View - The Boxer 1.5L
2021
THE BOXER 1.5L
SHIRAZ
$90
SOLD OUT
Quick View - The Boxer 3L
2021
THE BOXER 3L
SHIRAZ
$235
Quantity
ADD TO CART
Quick View - Carnival 1.5L
2021
CARNIVAL 1.5L
SHIRAZ
$240
Quantity
ADD TO CART
Quick View - Carnival 3L
2021
CARNIVAL 3L
SHIRAZ
$655
Quantity
ADD TO CART
Quick View - Carnival 6L
2021
CARNIVAL 6L
SHIRAZ
$1549
Quantity
ADD TO CART"""

def parse_wines():
    """Parse wine data from the page content"""
    wines = []
    lines = page_content.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Look for wine entries that start with "Quick View - "
        if line.startswith('Quick View - ') and not line.endswith('Gift Card'):
            wine_name = line.replace('Quick View - ', '').strip()
            
            # Skip if it's an event ticket
            if 'FEST' in wine_name.upper() or 'EVENT' in wine_name.upper():
                i += 1
                continue
                
            wine = {
                'name': wine_name,
                'vintage': '',
                'full_name': '',
                'variety': '',
                'price': '',
                'status': 'Available',
                'category': '',
                'region': 'McLaren Vale, South Australia'
            }
            
            # Look ahead for wine details
            for j in range(i + 1, min(i + 10, len(lines))):
                next_line = lines[j].strip()
                
                # Check for vintage (4-digit year)
                if re.match(r'^\d{4}$', next_line):
                    wine['vintage'] = next_line
                
                # Check for full wine name (usually in ALL CAPS)
                elif next_line.isupper() and len(next_line) > 3 and not next_line.startswith('$'):
                    if not wine['full_name']:
                        wine['full_name'] = next_line
                    elif wine['full_name'] and not wine['variety']:
                        wine['variety'] = next_line
                
                # Check for price
                elif next_line.startswith('$') and re.match(r'^\$\d+', next_line):
                    wine['price'] = next_line
                
                # Check for sold out status
                elif next_line == 'SOLD OUT':
                    wine['status'] = 'SOLD OUT'
                    break
                
                # Check for add to cart (indicates end of wine info)
                elif next_line == 'ADD TO CART':
                    break
                    
                # Check for category sections
                elif next_line in ['LEFTY WINES', 'FUN WINES', 'FAMILY WINES', 'LOVE WINES', 'VELVET GLOVE', 'LARGE FORMAT']:
                    # Find the category for this wine by looking backwards
                    for k in range(i, max(0, i - 20), -1):
                        prev_line = lines[k].strip()
                        if prev_line in ['LEFTY WINES', 'FUN WINES', 'FAMILY WINES', 'LOVE WINES', 'VELVET GLOVE', 'LARGE FORMAT']:
                            wine['category'] = prev_line
                            break
            
            # Determine category if not found
            if not wine['category']:
                for k in range(max(0, i - 20), i):
                    prev_line = lines[k].strip()
                    if prev_line in ['LEFTY WINES', 'FUN WINES', 'FAMILY WINES', 'LOVE WINES', 'VELVET GLOVE', 'LARGE FORMAT']:
                        wine['category'] = prev_line
                        break
            
            # Only add if we have essential info
            if wine['name'] and (wine['price'] or wine['status'] == 'SOLD OUT'):
                wines.append(wine)
        
        i += 1
    
    return wines

def main():
    print('🍷 PARSING REAL MOLLYDOOKER WINE DATA')
    print('=' * 50)
    
    wines = parse_wines()
    
    print(f'✅ Extracted {len(wines)} real wines from the website')
    print()
    
    # Create CSV file
    csv_filename = 'mollydooker_real_scraped_wines.csv'
    
    with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'full_name', 'vintage', 'variety', 'price', 'status', 'category', 'region']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for i, wine in enumerate(wines):
            print(f"{i+1:2d}. {wine['name']} ({wine['vintage']}) - {wine['price']} - {wine['status']}")
            if wine['variety']:
                print(f"    Variety: {wine['variety']}")
            if wine['category']:
                print(f"    Category: {wine['category']}")
            print()
            
            writer.writerow(wine)
    
    print(f"✅ Real wine data saved to: {csv_filename}")
    print(f"📊 Total wines exported: {len(wines)}")
    
    # Summary by category
    categories = {}
    for wine in wines:
        cat = wine.get('category', 'Unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📈 WINES BY CATEGORY:")
    for category, count in categories.items():
        print(f"  {category}: {count} wines")

if __name__ == "__main__":
    main()
