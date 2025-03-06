from browser_use import Browser, BrowserConfig

async def setup_browser() -> Browser:
    config = BrowserConfig(
        headless=True,
        disable_security=True
    )
    return Browser(config=config)