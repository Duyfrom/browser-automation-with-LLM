#!/usr/bin/env python3
"""
Browser Automation Script for Claude
Provides comprehensive browser control capabilities
"""

import json
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import base64

class BrowserAutomation:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.browser = None
        self.page = None
    
    def start_browser(self):
        """Initialize browser session"""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        print("✅ Browser started successfully")
    
    def close_browser(self):
        """Close browser session"""
        if self.browser:
            self.context.close()
        if self.playwright:
            self.playwright.stop()
        print("✅ Browser closed")
    
    def navigate_to(self, url):
        """Navigate to a URL"""
        try:
            self.page.goto(url, wait_until="networkidle")
            print(f"✅ Navigated to: {url}")
            return {"success": True, "url": url, "title": self.page.title()}
        except Exception as e:
            print(f"❌ Failed to navigate to {url}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_page_content(self):
        """Extract page content"""
        try:
            content = self.page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            # Extract text content
            text = soup.get_text(strip=True)
            
            # Extract links
            links = [{"text": a.get_text(strip=True), "href": a.get("href")} 
                    for a in soup.find_all("a", href=True)]
            
            # Extract images
            images = [{"alt": img.get("alt", ""), "src": img.get("src")} 
                     for img in soup.find_all("img")]
            
            return {
                "title": self.page.title(),
                "url": self.page.url,
                "text": text[:5000],  # First 5000 chars
                "links": links[:20],  # First 20 links
                "images": images[:10]  # First 10 images
            }
        except Exception as e:
            print(f"❌ Failed to extract content: {str(e)}")
            return {"error": str(e)}
    
    def take_screenshot(self, filename="screenshot.png"):
        """Take a screenshot of the current page"""
        try:
            self.page.screenshot(path=filename, full_page=True)
            print(f"✅ Screenshot saved as: {filename}")
            return {"success": True, "filename": filename}
        except Exception as e:
            print(f"❌ Failed to take screenshot: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def click_element(self, selector):
        """Click an element by CSS selector"""
        try:
            self.page.click(selector)
            print(f"✅ Clicked element: {selector}")
            return {"success": True, "selector": selector}
        except Exception as e:
            print(f"❌ Failed to click {selector}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def fill_form(self, selector, text):
        """Fill a form field"""
        try:
            self.page.fill(selector, text)
            print(f"✅ Filled field {selector} with text")
            return {"success": True, "selector": selector}
        except Exception as e:
            print(f"❌ Failed to fill {selector}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def wait_for_element(self, selector, timeout=30000):
        """Wait for an element to appear"""
        try:
            self.page.wait_for_selector(selector, timeout=timeout)
            print(f"✅ Element found: {selector}")
            return {"success": True, "selector": selector}
        except Exception as e:
            print(f"❌ Element not found {selector}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def execute_javascript(self, script):
        """Execute JavaScript on the page"""
        try:
            result = self.page.evaluate(script)
            print(f"✅ JavaScript executed successfully")
            return {"success": True, "result": result}
        except Exception as e:
            print(f"❌ JavaScript execution failed: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def get_element_text(self, selector):
        """Get text content of an element"""
        try:
            text = self.page.locator(selector).text_content()
            print(f"✅ Got text from {selector}: {text[:100]}...")
            return {"success": True, "text": text}
        except Exception as e:
            print(f"❌ Failed to get text from {selector}: {str(e)}")
            return {"success": False, "error": str(e)}

def demo_automation():
    """Demonstration of browser automation capabilities"""
    print("🚀 Starting Browser Automation Demo")
    
    # Create automation instance
    automation = BrowserAutomation(headless=True)
    
    try:
        # Start browser
        automation.start_browser()
        
        # Navigate to example site
        result = automation.navigate_to("https://example.com")
        print(f"Navigation result: {result}")
        
        # Take screenshot
        screenshot_result = automation.take_screenshot("/app/example_screenshot.png")
        print(f"Screenshot result: {screenshot_result}")
        
        # Get page content
        content = automation.get_page_content()
        print(f"Page title: {content.get('title')}")
        print(f"Page text preview: {content.get('text', '')[:200]}...")
        
        # Navigate to a more interactive site
        automation.navigate_to("https://httpbin.org/forms/post")
        
        # Fill a form
        automation.fill_form('input[name="custname"]', "Claude AI")
        automation.fill_form('input[name="custtel"]', "555-0123")
        
        # Take another screenshot
        automation.take_screenshot("/app/form_screenshot.png")
        
        print("✅ Demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")
    
    finally:
        # Always close browser
        automation.close_browser()

if __name__ == "__main__":
    demo_automation()
