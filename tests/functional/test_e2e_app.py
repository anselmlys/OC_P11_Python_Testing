from playwright.sync_api import sync_playwright

from tests.utils import flask_server


def test_e2e_login_and_summary(tmp_path):
    # Start Flask server with JSON temporary files
    server_process = flask_server.start_server_with_temp_data(tmp_path)

    try:
        # Launch Playwright
        with sync_playwright() as p:
            # Start browser and open new page
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            # Go to index page
            page.goto(f'{flask_server.BASE_URL}/')

            # Tries to login
            page.fill('input[name="email"]', 'test@club.com')
            page.click('button:has-text("Enter")')

            # Check that welcome.html is displayed has expected
            assert page.locator('text=Points available:').is_visible()

            # Close browser
            browser.close()
    
    finally:
        # Ensures that the server is shut down whether the test fails or not
        flask_server.stop_server(server_process)


def test_e2e_booking_success(tmp_path):
    server_process = flask_server.start_server_with_temp_data(tmp_path)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(f'{flask_server.BASE_URL}/')
            page.fill('input[name="email"]', 'test@club.com')
            page.click('button:has-text("Enter")')

            page.click('a:has-text("Book Places")')
            assert page.locator('text=How many places?').is_visible()

            page.fill('input[name="places"]', '5')
            page.click('button[type="submit"]')
            assert page.locator('text=Great-booking complete!').is_visible()

            browser.close()

    finally:
        flask_server.stop_server(server_process)


def test_e2e_booking_not_enough_points(tmp_path):
    server_process = flask_server.start_server_with_temp_data(tmp_path)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(f'{flask_server.BASE_URL}/')
            page.fill('input[name="email"]', 'test@club.com')
            page.click('button:has-text("Enter")')

            page.click('a:has-text("Book Places")')
            assert page.locator('text=How many places?').is_visible()

            page.fill('input[name="places"]', '11')
            page.click('button[type="submit"]')

            assert page.locator('text=You do not have enough points.').is_visible()
            assert page.locator('text=How many places?').is_visible()

            browser.close()
    
    finally:
        flask_server.stop_server(server_process)


def test_e2e_view_club_points(tmp_path):
    server_process = flask_server.start_server_with_temp_data(tmp_path)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(f'{flask_server.BASE_URL}/')
            page.click('a:has-text("here")')
            assert page.locator('text=Available points')

            browser.close()
    
    finally:
        flask_server.stop_server(server_process)
