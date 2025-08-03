# Browser Automation with LLM Integration

A comprehensive browser automation framework that enables natural language control of web browsers using Playwright. This project provides AI agents with the ability to control browsers, extract content, manage multiple tabs, and perform complex web automation tasks through natural language commands.

## 🚀 Features

- **Natural Language Control**: Command browsers using natural language through AI integration
- **Multi-tab Management**: Handle multiple browser tabs with persistent sessions
- **Real-time Web Scraping**: Extract and parse web content with intelligent data processing
- **Persistent Browser Sessions**: Maintain browser state across commands with IPC communication
- **Full Browser Control**: Navigate, click, fill forms, take screenshots, and execute JavaScript
- **Cross-Platform Support**: Works on macOS, Linux, and Windows
- **Docker Support**: Containerized deployment for easy scaling
- **CSV Export**: Export scraped data to structured formats

## 📋 Requirements

- **Python 3.9+**
- **Node.js** (for Playwright browser binaries)
- **Docker** (optional, for containerized deployment)

## 🛠️ Setup Options

### Option 1: Virtual Environment (Recommended)

```bash
# Clone the repository
git clone https://github.com/Duyfrom/browser-automation-with-LLM.git
cd browser-automation-with-LLM

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install browser binaries
python3 -m playwright install
```

### Option 2: Docker (Containerized)

```bash
# Clone the repository
git clone https://github.com/Duyfrom/browser-automation-with-LLM.git
cd browser-automation-with-LLM

# Build the Docker image
docker build -t browser-automation .

# Run container with volume mounting for screenshots
docker run --rm -v $(pwd)/screenshots:/app/screenshots browser-automation
```

## 🎮 Usage Methods

### 1. Browser Daemon with Natural Language Control (Recommended)

```bash
# Start the persistent browser daemon
source venv/bin/activate
python browser_daemon.py
```

In another terminal, send natural language commands:
```bash
# Send commands to the running daemon
python send_command.py "open a new tab and go to google.com"
python send_command.py "search for 'python web scraping'"
python send_command.py "take a screenshot"
python send_command.py "list all tabs"
python send_command.py "switch to tab 1"
```

**Available Natural Language Commands:**
- "open new tab [with URL]"
- "switch to tab [number]"
- "close current tab"
- "go to [URL]"
- "click on [element description]"
- "fill [field] with [text]"
- "take screenshot [filename]"
- "scroll down/up"
- "get page content"
- "list all tabs"
- "close browser"

### 2. Interactive CLI

```bash
# Start the basic CLI interface
source venv/bin/activate
python cli.py
```

**CLI Commands:**
```
start                    - Start browser session
goto <url>              - Navigate to URL  
title                   - Get page title
content                 - Get page content (text, links, images)
click <selector>        - Click element by CSS selector
fill <selector> <text>  - Fill form field
wait <selector>         - Wait for element to appear
text <selector>         - Get text from element
screenshot [filename]   - Take screenshot
js <script>            - Execute JavaScript
close                  - Close browser
help                   - Show help
quit                   - Exit CLI
```

### 2. Direct Python Usage

```python
from browser_automation import BrowserAutomation

# Create automation instance
automation = BrowserAutomation(headless=False)  # Set True for headless

try:
    # Start browser
    automation.start_browser()
    
    # Navigate and interact
    automation.navigate_to("https://example.com")
    automation.take_screenshot("example.png")
    content = automation.get_page_content()
    
    # Form interaction
    automation.fill_form('input[name="search"]', "query")
    automation.click_element('button[type="submit"]')
    
finally:
    automation.close_browser()
```

### 3. Docker Usage

```bash
# Run demo
docker run --rm browser-automation

# Run with volume for screenshots
docker run --rm -v $(pwd)/screenshots:/app/screenshots browser-automation
```

## 🎯 Common Use Cases for Claude

### Web Scraping
```python
automation.navigate_to("https://news.ycombinator.com")
content = automation.get_page_content()
print(f"Found {len(content['links'])} links")
```

### Form Automation
```python
automation.navigate_to("https://forms.example.com")
automation.fill_form('#name', 'Claude AI')
automation.fill_form('#email', 'claude@example.com')
automation.click_element('#submit')
```

### Screenshot & Analysis
```python
automation.navigate_to("https://website.com")
automation.take_screenshot("analysis.png")
content = automation.get_page_content()
# Analyze content and provide insights
```

### JavaScript Execution
```python
result = automation.execute_javascript("""
    return {
        title: document.title,
        links: Array.from(document.links).length,
        images: Array.from(document.images).length
    }
""")
```

## 🔧 Configuration

### Browser Settings
- **Headless Mode**: Set `headless=True` for background operation
- **Browser Choice**: Use `chromium`, `firefox`, or `webkit`
- **Viewport Size**: Configurable in BrowserAutomation class
- **User Agent**: Customizable for different device simulation

### Screenshot Options
- **Full Page**: `full_page=True` captures entire page
- **Element Only**: Use `element.screenshot()` for specific elements
- **Format**: PNG, JPEG support

## 🛡️ Security Notes

- Always validate URLs before navigation
- Be mindful of rate limiting on target sites
- Respect robots.txt and site terms of service
- Use appropriate delays between actions

## 🐛 Troubleshooting

### Common Issues

1. **Browser won't start**: Check if display is available in headless mode
2. **Elements not found**: Wait for page load with `wait_for_element()`
3. **Screenshots fail**: Ensure write permissions in target directory
4. **Docker issues**: Make sure Docker daemon is running

### Debug Mode
```python
automation = BrowserAutomation(headless=False)  # Visual debugging
```

## 📁 File Structure

```
browser-automation-with-LLM/
├── .gitignore               # Git ignore patterns
├── README.md                # This documentation
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container setup
├── browser_daemon.py        # Persistent browser session manager
├── send_command.py          # Command helper for IPC communication
├── browser_automation.py    # Core automation class
├── cli.py                   # Basic CLI interface
├── natural_browser_cli.py   # Natural language interface
├── persistent_browser.py    # Browser persistence utilities
├── wine_scraper.py          # Example web scraping implementation
├── parse_wine_data.py       # Data parsing utilities
└── main.py                 # Entry point
```

## 🎉 Success!

Your browser automation setup is complete and tested! Claude can now:
- ✅ Control browsers programmatically
- ✅ Extract and analyze web content  
- ✅ Take screenshots for visual analysis
- ✅ Fill forms and interact with pages
- ✅ Execute custom JavaScript
- ✅ Run in both GUI and headless modes
- ✅ Work via CLI, Python, or Docker

**Ready for Claude to browse the web! 🤖🌐**
