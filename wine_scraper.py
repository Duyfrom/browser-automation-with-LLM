#!/usr/bin/env python3
"""
Wine Catalog Scraper for Mollydooker Wines
Extracts comprehensive wine data and exports to CSV
"""

import csv
import json
import time
from send_command import send_command

def scrape_wine_catalog():
    print('🍷 COMPREHENSIVE WINE CATALOG SCRAPER')
    print('=' * 50)
    
    # First, analyze the page structure
    page_analysis = send_command('js', script='''
    const pageInfo = {
        title: document.title,
        url: window.location.href,
        bodyHTML: document.body.innerHTML.substring(0, 2000),
        allText: document.body.innerText.substring(0, 1000),
        productContainers: [],
        wineKeywords: []
    };
    
    // Look for product containers
    const containerSelectors = [
        '.product', '.wine', '.bottle', '.collection-item', 
        '.grid-item', '[data-product]', '.card', '.item'
    ];
    
    containerSelectors.forEach(selector => {
        const elements = document.querySelectorAll(selector);
        if (elements.length > 0) {
            pageInfo.productContainers.push({
                selector: selector,
                count: elements.length,
                sample: elements[0] ? elements[0].outerHTML.substring(0, 200) : ''
            });
        }
    });
    
    // Look for wine-related keywords in text
    const keywords = ['shiraz', 'cabernet', 'merlot', 'chardonnay', 'riesling', 'pinot', 'vintage', 'bottle', 'wine'];
    keywords.forEach(keyword => {
        if (pageInfo.allText.toLowerCase().includes(keyword)) {
            pageInfo.wineKeywords.push(keyword);
        }
    });
    
    JSON.stringify(pageInfo);
    ''')
    
    if page_analysis.get('status') == 'success':
        try:
            analysis = json.loads(page_analysis['data']['result'])
            print(f"📄 Page: {analysis['title']}")
            print(f"🌐 URL: {analysis['url']}")
            print(f"🔍 Wine keywords found: {', '.join(analysis['wineKeywords'])}")
            print(f"📦 Product containers found: {len(analysis['productContainers'])}")
            
            for container in analysis['productContainers']:
                print(f"  - {container['selector']}: {container['count']} items")
                
        except json.JSONDecodeError:
            print("Could not parse page analysis")
    
    # Now try multiple scraping strategies
    wines_found = []
    
    # Strategy 1: Look for actual wine products
    wine_scrape = send_command('js', script='''
    const wines = [];
    
    // Multiple strategies to find wines
    const strategies = [
        // Strategy 1: Look for wine product pages or links
        () => {
            const wineLinks = Array.from(document.querySelectorAll('a')).filter(link => {
                const href = link.href.toLowerCase();
                const text = link.textContent.toLowerCase();
                return (href.includes('/wine') || href.includes('/product') || 
                       text.includes('shiraz') || text.includes('cabernet') || 
                       text.includes('chardonnay') || text.includes('merlot') ||
                       text.includes('vintage') || text.includes('bottle')) &&
                       !href.includes('#') && href !== window.location.href;
            });
            
            return wineLinks.slice(0, 20).map(link => ({
                name: link.textContent.trim(),
                url: link.href,
                type: 'link_based'
            }));
        },
        
        // Strategy 2: Look for price elements (wines usually have prices)
        () => {
            const priceElements = Array.from(document.querySelectorAll('*')).filter(el => {
                const text = el.textContent;
                return text && (text.includes('$') || text.includes('AUD') || 
                               text.match(/\\d+\\.\\d{2}/)) && text.length < 50;
            });
            
            return priceElements.slice(0, 10).map(el => {
                const parent = el.closest('.product, .item, .card, article, .wine') || el.parentElement;
                const nameEl = parent.querySelector('h1, h2, h3, h4, .title, .name') || parent;
                return {
                    name: nameEl.textContent.trim(),
                    price: el.textContent.trim(),
                    type: 'price_based'
                };
            });
        },
        
        // Strategy 3: Look in specific wine-related text content
        () => {
            const textContent = document.body.innerText;
            const wineMatches = textContent.match(/[A-Z][a-z]+ (Shiraz|Cabernet|Merlot|Chardonnay|Pinot|Riesling)[^\\n]*/gi) || [];
            
            return wineMatches.slice(0, 15).map(match => ({
                name: match.trim(),
                type: 'text_based'
            }));
        }
    ];
    
    // Execute all strategies
    let allWines = [];
    strategies.forEach((strategy, index) => {
        try {
            const results = strategy();
            allWines = allWines.concat(results.map(wine => ({...wine, strategy: index + 1})));
        } catch (e) {
            console.log('Strategy ' + (index + 1) + ' failed:', e);
        }
    });
    
    // Clean and deduplicate
    const uniqueWines = [];
    const seen = new Set();
    
    allWines.forEach(wine => {
        if (wine.name && wine.name.length > 3 && wine.name.length < 200) {
            const cleanName = wine.name.replace(/\\s+/g, ' ').trim();
            if (!seen.has(cleanName.toLowerCase())) {
                seen.add(cleanName.toLowerCase());
                uniqueWines.push({
                    name: cleanName,
                    price: wine.price || '',
                    url: wine.url || '',
                    description: '',
                    vintage: cleanName.match(/\\b(19|20)\\d{2}\\b/)?.[0] || '',
                    variety: (['shiraz', 'cabernet', 'merlot', 'chardonnay', 'pinot', 'riesling']
                             .find(v => cleanName.toLowerCase().includes(v)) || ''),
                    region: 'McLaren Vale, South Australia',
                    type: wine.type,
                    strategy: wine.strategy
                });
            }
        }
    });
    
    JSON.stringify(uniqueWines);
    ''')
    
    if wine_scrape.get('status') == 'success':
        try:
            wines_data = json.loads(wine_scrape['data']['result'])
            wines_found = wines_data
            print(f"🍇 Found {len(wines_found)} potential wines")
            
        except json.JSONDecodeError:
            print("Could not parse wine data")
    
    # If we have wines, create CSV
    if wines_found:
        csv_filename = 'mollydooker_wines_comprehensive.csv'
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'price', 'description', 'vintage', 'variety', 'region', 'url', 'extraction_method', 'strategy_used']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for wine in wines_found:
                writer.writerow({
                    'name': wine.get('name', ''),
                    'price': wine.get('price', ''),
                    'description': wine.get('description', ''),
                    'vintage': wine.get('vintage', ''),
                    'variety': wine.get('variety', '').title(),
                    'region': wine.get('region', ''),
                    'url': wine.get('url', ''),
                    'extraction_method': wine.get('type', ''),
                    'strategy_used': wine.get('strategy', '')
                })
        
        print(f"✅ Successfully created {csv_filename}")
        print(f"📊 Exported {len(wines_found)} wine entries")
        print()
        print("📋 Sample wines found:")
        for i, wine in enumerate(wines_found[:8]):
            print(f"  {i+1}. {wine['name']}")
            if wine.get('variety'):
                print(f"     Variety: {wine['variety'].title()}")
            if wine.get('price'):
                print(f"     Price: {wine['price']}")
            print(f"     Method: {wine.get('type', 'unknown')}")
            print()
            
        return True
    else:
        print("❌ No wines found")
        return False

if __name__ == "__main__":
    success = scrape_wine_catalog()
    if success:
        print("🎉 Wine catalog scraping completed successfully!")
    else:
        print("💔 Wine catalog scraping failed")
