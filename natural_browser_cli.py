#!/usr/bin/env python3
"""
Natural Language Browser Automation CLI
Accepts commands via command line arguments or stdin
"""

import sys
import json
import argparse
from browser_automation import BrowserAutomation

class NaturalBrowserCLI:
    def __init__(self):
        self.automation = None
        
    def start_browser(self):
        """Start browser session"""
        if not self.automation:
            self.automation = BrowserAutomation(headless=False)
            self.automation.start_browser()
            return "✅ Browser started successfully"
        return "⚠️ Browser already running"
    
    def execute_command(self, command_type, **kwargs):
        """Execute a browser command"""
        if not self.automation:
            return "❌ Browser not started. Start browser first."
            
        try:
            if command_type == "navigate":
                url = kwargs.get('url')
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                result = self.automation.navigate_to(url)
                return f"✅ Navigated to {url}"
                
            elif command_type == "click":
                selector = kwargs.get('selector')
                result = self.automation.click_element(selector)
                return f"✅ Clicked element: {selector}"
                
            elif command_type == "fill":
                selector = kwargs.get('selector')
                text = kwargs.get('text')
                result = self.automation.fill_form(selector, text)
                return f"✅ Filled '{selector}' with '{text}'"
                
            elif command_type == "screenshot":
                filename = kwargs.get('filename', 'screenshot.png')
                result = self.automation.take_screenshot(filename)
                return f"✅ Screenshot saved as {filename}"
                
            elif command_type == "get_title":
                title = self.automation.page.title()
                return f"📋 Page title: {title}"
                
            elif command_type == "get_content":
                content = self.automation.get_page_content()
                return f"📄 Page content retrieved"
                
            elif command_type == "wait":
                selector = kwargs.get('selector')
                result = self.automation.wait_for_element(selector)
                return f"✅ Waited for element: {selector}"
                
            elif command_type == "execute_js":
                script = kwargs.get('script')
                result = self.automation.execute_javascript(script)
                return f"✅ JavaScript executed: {result}"
                
            else:
                return f"❌ Unknown command type: {command_type}"
                
        except Exception as e:
            return f"❌ Error executing command: {str(e)}"
    
    def close_browser(self):
        """Close browser session"""
        if self.automation:
            self.automation.close_browser()
            self.automation = None
            return "✅ Browser closed"
        return "⚠️ No browser to close"

def main():
    parser = argparse.ArgumentParser(description='Natural Language Browser Automation')
    parser.add_argument('--start', action='store_true', help='Start browser')
    parser.add_argument('--navigate', type=str, help='Navigate to URL')
    parser.add_argument('--click', type=str, help='Click element by selector')
    parser.add_argument('--fill', nargs=2, metavar=('SELECTOR', 'TEXT'), help='Fill form field')
    parser.add_argument('--screenshot', type=str, nargs='?', const='screenshot.png', help='Take screenshot')
    parser.add_argument('--title', action='store_true', help='Get page title')
    parser.add_argument('--close', action='store_true', help='Close browser')
    parser.add_argument('--wait', type=str, help='Wait for element')
    parser.add_argument('--js', type=str, help='Execute JavaScript')
    
    args = parser.parse_args()
    
    cli = NaturalBrowserCLI()
    
    # Execute commands based on arguments
    if args.start:
        print(cli.start_browser())
        
    if args.navigate:
        print(cli.execute_command('navigate', url=args.navigate))
        
    if args.click:
        print(cli.execute_command('click', selector=args.click))
        
    if args.fill:
        print(cli.execute_command('fill', selector=args.fill[0], text=args.fill[1]))
        
    if args.screenshot:
        print(cli.execute_command('screenshot', filename=args.screenshot))
        
    if args.title:
        print(cli.execute_command('get_title'))
        
    if args.wait:
        print(cli.execute_command('wait', selector=args.wait))
        
    if args.js:
        print(cli.execute_command('execute_js', script=args.js))
        
    if args.close:
        print(cli.close_browser())

if __name__ == "__main__":
    cli = NaturalBrowserCLI()
    while True:
        try:
            command = input("Enter your command: ")
            if command.lower() == "exit":
                print(cli.close_browser())
                break
            elif command.lower().startswith("go to "):
                url = command[6:].strip()
                print(cli.execute_command('navigate', url=url))
            elif command.lower().startswith("search for "):
                query = command[11:].strip()
                print(cli.execute_command('fill', selector='input[name=\"q\"]', text=query))
                print(cli.execute_command('click', selector='input[type=\"submit\"]'))
            else:
                print(f"❌ Unknown command: {command}")

        except KeyboardInterrupt:
            print(cli.close_browser())
            break
