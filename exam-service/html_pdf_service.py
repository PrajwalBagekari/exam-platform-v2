import asyncio

from playwright.async_api import (
    async_playwright
)


async def create_pdf(
    url: str,
    output_path: str,
):

    async with (
        async_playwright()
        as playwright
    ):

        browser = await (
            playwright.chromium.launch(
                headless=True
            )
        )

        page = await (
            browser.new_page()
        )

        await page.goto(
            url,
            wait_until="networkidle"
        )

        await page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
        )

        await browser.close()


def generate_html_pdf(
    url: str,
    output_path: str,
):
    asyncio.run(
        create_pdf(
            url,
            output_path,
        )
    )