#!/usr/bin/env python3
"""
Interactive CLI for Browser Automation
Allows Claude to control browsers with simple commands
"""

import sys
import json
from browser_automation import BrowserAutomation

def print_help():
    """Print available commands"""
    help_text = """
🤖 Browser Automation CLI Commands:

Basic Navigation:
  start                    - Start browser session
  goto <url>              - Navigate to URL
  title                   - Get page title
  content                 - Get page content (text, links, images)
  close                   - Close browser

Interaction:
  click <selector>        - Click element by CSS selector
  fill <selector> <text>  - Fill form field
  wait <selector>         - Wait for element to appear
  text <selector>         - Get text from element

Utilities:
  screenshot [filename]   - Take screenshot (default: screenshot.png)
  js <script>            - Execute JavaScript
  help                   - Show this help
  quit                   - Exit CLI

Examples:
  goto https://google.com
  fill input[name="q"] "Claude AI"
  click input[type="submit"]
  screenshot google_search.png
"""
    print(help_text)

def main():
    """Main CLI loop"""
    print("🚀 Browser Automation CLI Started")
    print("Type 'help' for commands or 'quit' to exit")
    
    automation = None
    
    try:
        while True:
            try:
                command = input("\n🤖 > ").strip()
                
                if not command:
                    continue
                
                parts = command.split()
                cmd = parts[0].lower()
                
                if cmd == 'quit' or cmd == 'exit':
                    break
                elif cmd == 'help':
                    print_help()
                elif cmd == 'start':
                    if automation:
                        print("⚠️  Browser already started")
                    else:
                        automation = BrowserAutomation(headless=False)
                        automation.start_browser()
                elif cmd == 'close':
                    if automation:
                        automation.close_browser()
                        automation = None
                    else:
                        print("⚠️  No browser session to close")
                elif cmd == 'goto':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    if len(parts) < 2:
                        print("❌ Usage: goto <url>")
                        continue
                    url = parts[1]
                    result = automation.navigate_to(url)
                    print(f"📄 {result}")
                elif cmd == 'title':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    try:
                        title = automation.page.title()
                        print(f"📋 Title: {title}")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                elif cmd == 'content':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    content = automation.get_page_content()
                    print(f"📄 Content: {json.dumps(content, indent=2)}")
                elif cmd == 'click':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    if len(parts) < 2:
                        print("❌ Usage: click <selector>")
                        continue
                    selector = parts[1]
                    result = automation.click_element(selector)
                    print(f"👆 {result}")
                elif cmd == 'fill':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    if len(parts) < 3:
                        print("❌ Usage: fill <selector> <text>")
                        continue
                    selector = parts[1]
                    text = ' '.join(parts[2:])
                    result = automation.fill_form(selector, text)
                    print(f"✏️  {result}")
                elif cmd == 'wait':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    if len(parts) < 2:
                        print("❌ Usage: wait <selector>")
                        continue
                    selector = parts[1]
                    result = automation.wait_for_element(selector)
                    print(f"⏰ {result}")
                elif cmd == 'text':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    if len(parts) < 2:
                        print("❌ Usage: text <selector>")
                        continue
                    selector = parts[1]
                    result = automation.get_element_text(selector)
                    print(f"📝 {result}")
                elif cmd == 'screenshot':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    filename = parts[1] if len(parts) > 1 else "screenshot.png"
                    result = automation.take_screenshot(filename)
                    print(f"📸 {result}")
                elif cmd == 'js':
                    if not automation:
                        print("❌ Start browser first with 'start'")
                        continue
                    if len(parts) < 2:
                        print("❌ Usage: js <javascript_code>")
                        continue
                    script = ' '.join(parts[1:])
                    result = automation.execute_javascript(script)
                    print(f"🔧 {result}")
                else:
                    print(f"❌ Unknown command: {cmd}")
                    print("Type 'help' for available commands")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    finally:
        if automation:
            automation.close_browser()

if __name__ == "__main__":
    main()
