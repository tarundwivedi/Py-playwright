import pytest
from playwright.sync_api import Page, expect,Playwright, sync_playwright
from pytest_playwright_snapshot.plugin import assert_snapshot


def test_main():
    with sync_playwright() as p:
        iphone_12 = p.devices['iPhone 12']
        browser = p.webkit.launch(headless=False)
        context = browser.new_context(
            **iphone_12,
        )
        # browser = p.chromium.launch(headless=False, slow_mo=1000)
        page = browser.new_page()
        context = browser.new_context()

        # Start tracing before creating / navigating a page.
        context.tracing.start(screenshots=True, snapshots=True, sources=True)

        page.goto('https://creativecloud.adobe.com/')
        # page.on("request", log_request)
        print(page.title())
        # test_myapp(page,assert_snapshot)
        page.locator('h1.welcome-title-v3').text_content()
        page.locator('span.welcome-desc-v3').text_content()
        page.locator('div.welcome-cta button:has-text("Sign in")').is_visible()
        page.locator('button:has-text("View all plans")').is_visible()
        page.locator("div.scroll-carousel button", has_text="Download").is_visible()
        page.locator("div.scroll-carousel button", has_text="Sign in").is_visible()
        page.locator("div.scroll-carousel button", has_text="Get help").is_visible()
        page.locator("div.scroll-carousel button", has_text="Get started").is_visible()
        page.locator("div.info-desc.cc div", has_text="Adobe Express").is_visible()
        page.locator("div.info-desc.cc div", has_text="Quickly and easily make standout content from thousands of beautiful templates.").is_visible()
        page.screenshot(path="screenshot.png", full_page=True)
        page.locator("div.info-desc.cc button", has_text="Start for free").click()
        page.once("load", lambda: print("page loaded!"))
        page.wait_for_timeout(1000)
        context.tracing.stop(path="trace.zip")
        browser.close()


if __name__ == '__main__':
    test_main()

def log_request(intercepted_request):
        print("a request was made:", intercepted_request.url)

@pytest.fixture
def test_myapp(page, assert_snapshot):
    assert_snapshot(page.screenshot(), "screenshot.png")

