import os
import asyncio
import pandas as pd
from playwright.async_api import async_playwright
from sqlalchemy import create_engine

# Environment Variables
DB_URL = os.getenv("DB_URL")
LOGIN_URL = os.getenv("LOGIN_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
EXPORT_URL = os.getenv("EXPORT_URL")

# Database Connection
engine = create_engine(DB_URL)

async def login_and_export():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Login
        await page.goto(LOGIN_URL)
        await page.fill("input[name='username']", USERNAME)
        await page.fill("input[name='password']", PASSWORD)
        await page.click("button[type='submit']")
        await page.wait_for_load_state("networkidle")

        # Navigate to Export URL
        await page.goto(EXPORT_URL)
        await page.wait_for_load_state("networkidle")

        table = await page.inner_html("table")
        data = []

        # Example scraping logic (Adjust to your portal structure)
        rows = await page.query_selector_all("table tr")
        headers = [th.inner_text().strip() for th in await rows[0].query_selector_all("th")]
        for row in rows[1:]:
            cols = [await td.inner_text() for td in await row.query_selector_all("td")]
            if cols:
                data.append(cols)

        # Save to DataFrame and Database
        df = pd.DataFrame(data, columns=headers)
        df.to_sql("payment_history", con=engine, if_exists="replace", index=False)
        print("Data imported successfully")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(login_and_export())
