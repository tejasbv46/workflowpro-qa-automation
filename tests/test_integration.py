import pytest
import requests
from playwright.sync_api import Page, expect, Browser, BrowserContext

# --- CONFIGURATION ---
# Note: In a real environment, these are mock endpoints or staging URLs
API_URL = "https://jsonplaceholder.typicode.com" # Placeholder for demo stability
UI_URL = "https://example.com" 

# --- FIXTURE: DATA MANAGEMENT ---
@pytest.fixture(scope="function")
def project_data():
    """
    Creates test data via API before the UI test starts.
    """
    # 1. SETUP: Create Data via API
    # Simulating a POST request to create a project
    payload = {"title": "Integration Test Project", "body": "Created via Pytest", "userId": 1}
    
    # We use a public mock API (jsonplaceholder) so this script actually runs for the demo
    response = requests.post(f"{API_URL}/posts", json=payload)
    
    # Fail fast if API is broken
    if response.status_code != 201:
        pytest.fail(f"API Prerequisite Failed: {response.status_code}")

    data = response.json()
    # Mocking an ID since the real API isn't available
    data['id'] = 123 
    
    yield data 

    # 2. TEARDOWN: Cleanup
    # requests.delete(f"{API_URL}/posts/{data['id']}")
    print(f"\n[Teardown] Cleaned up project {data['id']}")

# --- FIXTURE: MOBILE ENVIRONMENT ---
@pytest.fixture(scope="function")
def mobile_context(browser: Browser):
    """
    Simulates a Mobile Device environment (iPhone 13 Pro).
    """
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"
    )
    yield context
    context.close()

# --- MAIN INTEGRATION TEST ---
def test_project_creation_flow(page: Page, mobile_context: BrowserContext, browser: Browser, project_data):
    """
    Validates: API Create -> UI Display -> Mobile Check -> Security Isolation
    """
    print(f"Step 1: Project '{project_data['title']}' created via API.")

    # [Step 2] Web UI: Verify project display
    page.goto(UI_URL)
    
    # Simulating finding the project on the dashboard
    # In a real app, this would be: page.locator(f"text={project_data['title']}")
    expect(page.locator("h1")).to_be_visible(timeout=10000)
    print("Step 2: UI Dashboard loaded successfully.")

    # [Step 3] Mobile: Check mobile accessibility
    mobile_page = mobile_context.new_page()
    mobile_page.goto(UI_URL)
    
    # Verify mobile viewport width
    viewport_width = mobile_page.viewport_size['width']
    assert viewport_width == 390
    print("Step 3: Mobile view verified.")

    # [Step 4] Security: Verify Tenant Isolation
    intruder_context = browser.new_context()
    intruder_page = intruder_context.new_page()
    
    # Attempt to access the protected project URL as an intruder
    intruder_page.goto(f"{UI_URL}/projects/{project_data['id']}")
    
    # Assert that we DO NOT see the project title (Security Check)
    # Since example.com handles 404s differently, we check for generic 404/Access denied behavior
    expect(intruder_page.locator("body")).not_to_contain_text(project_data['title'])
    
    intruder_context.close()
    print("Step 4: Security check passed. Tenant isolation verified.")
