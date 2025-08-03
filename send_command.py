#!/usr/bin/env python3
"""
Send commands to the browser daemon
"""

import json
import time
import os
import sys

def send_command(command_type, **args):
    """Send a command to the browser daemon"""
    command_file = "browser_command.json"
    result_file = "browser_result.json"
    
    # Remove old result file
    if os.path.exists(result_file):
        os.remove(result_file)
    
    # Create command
    command = {
        "type": command_type,
        "args": args
    }
    
    # Write command file
    with open(command_file, 'w') as f:
        json.dump(command, f)
    
    # Wait for result
    timeout = 30  # 30 seconds timeout
    start_time = time.time()
    
    while not os.path.exists(result_file):
        if time.time() - start_time > timeout:
            return {"status": "error", "message": "Command timeout"}
        time.sleep(0.1)
    
    # Read result
    with open(result_file, 'r') as f:
        result = json.load(f)
    
    return result

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 send_command.py <command> [args...]")
        print("Commands:")
        print("  navigate <url>")
        print("  click <selector>") 
        print("  fill <selector> <text>")
        print("  screenshot [filename]")
        print("  title")
        print("  js <script>")
        print("  new_tab")
        print("  list_tabs")
        print("  switch_tab [index]")
        print("  current_tab")
        print("  stop")
        return
    
    command = sys.argv[1]
    
    if command == "navigate" and len(sys.argv) > 2:
        result = send_command("navigate", url=sys.argv[2])
    elif command == "click" and len(sys.argv) > 2:
        result = send_command("click", selector=sys.argv[2])
    elif command == "fill" and len(sys.argv) > 3:
        result = send_command("fill", selector=sys.argv[2], text=" ".join(sys.argv[3:]))
    elif command == "screenshot":
        filename = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
        result = send_command("screenshot", filename=filename)
    elif command == "title":
        result = send_command("title")
    elif command == "js" and len(sys.argv) > 2:
        result = send_command("js", script=" ".join(sys.argv[2:]))
    elif command == "new_tab":
        # Enhanced new_tab with optional purpose and URL
        purpose = sys.argv[2] if len(sys.argv) > 2 else "general"
        url = sys.argv[3] if len(sys.argv) > 3 else None
        if url:
            result = send_command("new_tab", purpose=purpose, url=url)
        else:
            result = send_command("new_tab", purpose=purpose)
    elif command == "list_tabs":
        result = send_command("list_tabs")
    elif command == "switch_tab" and len(sys.argv) > 2:
        tab_index = int(sys.argv[2])
        result = send_command("switch_tab", index=tab_index)
    elif command == "current_tab":
        result = send_command("current_tab")
    elif command == "stop":
        result = send_command("stop")
    else:
        print("Invalid command or missing arguments")
        return
    
    print(f"Status: {result.get('status')}")
    print(f"Message: {result.get('message')}")
    if result.get('data'):
        print(f"Data: {result.get('data')}")

if __name__ == "__main__":
    main()
