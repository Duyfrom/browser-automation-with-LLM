# Browser Automation for Claude AI

This project provides Claude AI with the ability to control browsers on macOS, see content, make edits, browse the web, and extract content just like a normal user.

## 🚀 Features

- **Full Browser Control**: Navigate, click, fill forms, take screenshots
- **Content Extraction**: Get page text, links, images, and metadata  
- **JavaScript Execution**: Run custom JavaScript on pages
- **Multiple Interfaces**: CLI, Docker, and direct Python usage
- **Cross-Browser Support**: Chromium, Firefox, and WebKit via Playwright
- **Headless & GUI Modes**: Run with or without visible browser window

## 📋 Requirements

- **macOS** (tested on your system)
- **Python 3.9+** ✅ (you have 3.9.6)
- **Docker** ✅ (already installed)

## 🛠️ Setup Options

### Option 1: Virtual Environment (Recommended)

```bash
cd /Users/khuongduypham/browser-automation

# Activate virtual environment
source venv/bin/activate

# Install dependencies (already done)
# pip install playwright selenium beautifulsoup4 requests

# Install browser binaries (already done)
# playwright install
```

### Option 2: Docker (Containerized)

```bash
cd /Users/khuongduypham/browser-automation

# Build image (already built)
# docker build -t browser-automation .

# Run container
docker run --rm -v $(pwd)/screenshots:/app/screenshots browser-automation
```

## 🎮 Usage Methods

### 1. Interactive CLI (Best for Claude)

```bash
# Start the interactive CLI
source venv/bin/activate
python cli.py
```

**Available Commands:**
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

**Example Session:**
```
🤖 > start
🤖 > goto https://google.com
🤖 > fill input[name="q"] "Claude AI browser automation"
🤖 > click input[type="submit"]
🤖 > screenshot google_results.png
🤖 > content
🤖 > quit
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
browser-automation/
├── browser_automation.py  # Main automation class
├── cli.py                # Interactive CLI interface  
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container setup
├── README.md           # This file
└── venv/              # Virtual environment
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
