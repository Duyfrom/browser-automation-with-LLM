#!/usr/bin/env python3
"""
Persistent Browser Automation
Keeps browser running and accepts commands via function calls
"""

import sys
import time
from browser_automation import BrowserAutomation

class PersistentBrowser:
    def __init__(self):
        self.automation = None
        self.start_browser()
        
    def start_browser(self):
        """Start browser session"""
        if not self.automation:
            self.automation = BrowserAutomation(headless=False)
            self.automation.start_browser()
            print("✅ Browser started successfully")
            return True
        print("⚠️ Browser already running")
        return False
    
    def navigate_to(self, url):
        """Navigate to URL"""
        if not self.automation:
            return "❌ Browser not started"
            
        try:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            result = self.automation.navigate_to(url)
            return f"✅ Navigated to {url}"
        except Exception as e:
            return f"❌ Error navigating: {str(e)}"
    
    def click_element(self, selector):
        """Click element by selector"""
        if not self.automation:
            return "❌ Browser not started"
            
        try:
            result = self.automation.click_element(selector)
            return f"✅ Clicked element: {selector}"
        except Exception as e:
            return f"❌ Error clicking: {str(e)}"
    
    def fill_form(self, selector, text):
        """Fill form field"""
        if not self.automation:
            return "❌ Browser not started"
            
        try:
            result = self.automation.fill_form(selector, text)
            return f"✅ Filled '{selector}' with '{text}'"
        except Exception as e:
            return f"❌ Error filling form: {str(e)}"
    
    def take_screenshot(self, filename='screenshot.png'):
        """Take screenshot"""
        if not self.automation:
            return "❌ Browser not started"
            
        try:
            result = self.automation.take_screenshot(filename)
            return f"✅ Screenshot saved as {filename}"
        except Exception as e:
            return f"❌ Error taking screenshot: {str(e)}"
    
    def get_title(self):
        """Get page title"""
        if not self.automation:
            return "❌ Browser not started"
            
        try:
            title = self.automation.page.title()
            return f"📋 Page title: {title}"
        except Exception as e:
            return f"❌ Error getting title: {str(e)}"
    
    def wait_for_element(self, selector):
        """Wait for element to appear"""
        if not self.automation:
            return "❌ Browser not started"
            
        try:
            result = self.automation.wait_for_element(selector)
            return f"✅ Waited for element: {selector}"
        except Exception as e:
            return f"❌ Error waiting: {str(e)}"
    
    def execute_javascript(self, script):
        """Execute JavaScript"""
        if not self.automation:
            return "❌ Browser not started"
            
        try:
            result = self.automation.execute_javascript(script)
            return f"✅ JavaScript executed: {result}"
        except Exception as e:
            return f"❌ Error executing JS: {str(e)}"
    
    def close_browser(self):
        """Close browser session"""
        if self.automation:
            try:
                self.automation.close_browser()
                self.automation = None
                return "✅ Browser closed"
            except Exception as e:
                return f"❌ Error closing browser: {str(e)}"
        return "⚠️ No browser to close"
    
    def is_running(self):
        """Check if browser is running"""
        return self.automation is not None

# Global browser instance
browser = None

def get_browser():
    """Get or create browser instance"""
    global browser
    if browser is None:
        browser = PersistentBrowser()
    return browser

if __name__ == "__main__":
    # Start browser and keep it running
    browser = PersistentBrowser()
    
    print("🌐 Browser is now running!")
    print("Use the browser object to control it programmatically")
    print("Press Ctrl+C to exit")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n" + browser.close_browser())
        print("👋 Goodbye!")
