#!/usr/bin/env python3
"""
Browser Daemon - Keeps browser session alive
Accepts commands via command files and returns results
"""

import os
import time
import json
import signal
import sys
from browser_automation import BrowserAutomation

class BrowserDaemon:
    def __init__(self):
        self.automation = None
        self.command_file = "browser_command.json"
        self.result_file = "browser_result.json"
        self.running = True
        self.pages = []  # List to store all open pages/tabs
        self.current_page_index = 0  # Index of currently active page
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start browser
        self.start_browser()
        
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print(f"\nReceived signal {signum}, shutting down...")
        self.running = False
        if self.automation:
            self.automation.close_browser()
        sys.exit(0)
        
    def start_browser(self):
        """Start browser session"""
        try:
            self.automation = BrowserAutomation(headless=False)
            self.automation.start_browser()
            # Add the initial page to our pages list
            self.pages.append({
                'page': self.automation.page,
                'title': 'New Tab',
                'url': 'about:blank',
                'index': 0
            })
            print("✅ Browser daemon started successfully")
            self.write_result({"status": "started", "message": "Browser daemon ready"})
        except Exception as e:
            print(f"❌ Failed to start browser: {e}")
            self.write_result({"status": "error", "message": str(e)})
            
    def write_result(self, result):
        """Write result to file"""
        try:
            with open(self.result_file, 'w') as f:
                json.dump(result, f)
        except Exception as e:
            print(f"Error writing result: {e}")
            
    def execute_command(self, command_data):
        """Execute a browser command"""
        if not self.automation:
            return {"status": "error", "message": "Browser not started"}
            
        try:
            command_type = command_data.get('type')
            args = command_data.get('args', {})
            
            if command_type == "navigate":
                url = args.get('url')
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                result = self.automation.navigate_to(url)
                return {"status": "success", "message": f"Navigated to {url}", "data": result}
                
            elif command_type == "click":
                selector = args.get('selector')
                result = self.automation.click_element(selector)
                return {"status": "success", "message": f"Clicked {selector}", "data": result}
                
            elif command_type == "fill":
                selector = args.get('selector')
                text = args.get('text')
                result = self.automation.fill_form(selector, text)
                return {"status": "success", "message": f"Filled {selector} with '{text}'", "data": result}
                
            elif command_type == "screenshot":
                filename = args.get('filename', 'screenshot.png')
                result = self.automation.take_screenshot(filename)
                return {"status": "success", "message": f"Screenshot saved as {filename}", "data": result}
                
            elif command_type == "title":
                title = self.automation.page.title()
                return {"status": "success", "message": f"Page title: {title}", "data": title}
                
            elif command_type == "wait":
                selector = args.get('selector')
                result = self.automation.wait_for_element(selector)
                return {"status": "success", "message": f"Waited for {selector}", "data": result}
                
            elif command_type == "js":
                script = args.get('script')
                result = self.automation.execute_javascript(script)
                return {"status": "success", "message": "JavaScript executed", "data": result}
                
            elif command_type == "new_tab":
                # Create a new page/tab with optional URL and purpose within the same browser context
                new_page = self.automation.context.new_page()
                tab_info = {
                    'page': new_page,
                    'title': 'New Tab',
                    'url': 'about:blank',
                    'index': len(self.pages),
                    'purpose': args.get('purpose', 'general')  # e.g., 'search', 'shopping', 'video'
                }
                self.pages.append(tab_info)
                self.current_page_index = len(self.pages) - 1
                self.automation.page = new_page  # Switch to the new page
                
                # If URL is provided, navigate to it
                if args.get('url'):
                    url = args.get('url')
                    if not url.startswith(('http://', 'https://')):
                        url = 'https://' + url
                    new_page.goto(url)
                    tab_info['url'] = url
                    tab_info['title'] = new_page.title()
                
                return {
                    "status": "success", 
                    "message": f"New tab opened (Tab {tab_info['index'] + 1})",
                    "data": {
                        "tab_index": tab_info['index'],
                        "purpose": tab_info['purpose'],
                        "url": tab_info['url']
                    }
                }
                
            elif command_type == "switch_tab":
                # Switch to a specific tab by index
                tab_index = args.get('index', 0)
                if 0 <= tab_index < len(self.pages):
                    self.current_page_index = tab_index
                    self.automation.page = self.pages[tab_index]['page']
                    current_tab = self.pages[tab_index]
                    # Bring the tab to front
                    self.automation.page.bring_to_front()
                    return {
                        "status": "success",
                        "message": f"Switched to Tab {tab_index + 1}",
                        "data": {
                            "tab_index": tab_index,
                            "title": current_tab['title'],
                            "url": current_tab['url'],
                            "purpose": current_tab.get('purpose', 'general')
                        }
                    }
                else:
                    return {"status": "error", "message": f"Tab index {tab_index} not found"}
                    
            elif command_type == "list_tabs":
                # List all open tabs
                tabs_info = []
                for i, tab in enumerate(self.pages):
                    try:
                        # Update tab info
                        tab['title'] = tab['page'].title()
                        tab['url'] = tab['page'].url
                        tabs_info.append({
                            "index": i,
                            "title": tab['title'],
                            "url": tab['url'],
                            "purpose": tab.get('purpose', 'general'),
                            "active": i == self.current_page_index
                        })
                    except:
                        tabs_info.append({
                            "index": i,
                            "title": "Closed Tab",
                            "url": "about:blank",
                            "purpose": tab.get('purpose', 'general'),
                            "active": False
                        })
                        
                return {
                    "status": "success",
                    "message": f"Found {len(tabs_info)} tabs",
                    "data": {
                        "tabs": tabs_info,
                        "current_tab": self.current_page_index
                    }
                }
                
            elif command_type == "current_tab":
                # Get information about current tab
                if self.pages:
                    current_tab = self.pages[self.current_page_index]
                    try:
                        current_tab['title'] = current_tab['page'].title()
                        current_tab['url'] = current_tab['page'].url
                    except:
                        pass
                    return {
                        "status": "success",
                        "message": "Current tab info",
                        "data": {
                            "tab_index": self.current_page_index,
                            "title": current_tab['title'],
                            "url": current_tab['url'],
                            "purpose": current_tab.get('purpose', 'general')
                        }
                    }
                else:
                    return {"status": "error", "message": "No tabs available"}
                
            elif command_type == "stop":
                self.running = False
                return {"status": "success", "message": "Stopping daemon"}
                
            else:
                return {"status": "error", "message": f"Unknown command: {command_type}"}
                
        except Exception as e:
            return {"status": "error", "message": str(e)}
            
    def run(self):
        """Main daemon loop"""
        print("🤖 Browser daemon running... (Ctrl+C to stop)")
        
        while self.running:
            try:
                # Check for command file
                if os.path.exists(self.command_file):
                    with open(self.command_file, 'r') as f:
                        command_data = json.load(f)
                    
                    # Execute command
                    result = self.execute_command(command_data)
                    
                    # Write result
                    self.write_result(result)
                    
                    # Remove command file
                    os.remove(self.command_file)
                    
                    print(f"✅ Executed: {command_data.get('type')} - {result.get('message')}")
                    
                    # Check if we should stop
                    if command_data.get('type') == 'stop':
                        break
                        
                time.sleep(0.1)  # Small delay to prevent high CPU usage
                
            except Exception as e:
                print(f"❌ Error in daemon loop: {e}")
                time.sleep(1)
                
        # Cleanup
        if self.automation:
            self.automation.close_browser()
        print("👋 Browser daemon stopped")

if __name__ == "__main__":
    daemon = BrowserDaemon()
    daemon.run()
