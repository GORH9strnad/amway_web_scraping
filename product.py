import asyncio
from playwright.async_api import async_playwright
import re

class Product:

    def __init__(self, url):
        self.url = url
    
    @property
    async def img_url(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(self.url)

            img_element = await page.query_selector('.image-gallery__img')
            img_url = await img_element.get_attribute('src')

            await browser.close()

            return img_url

    @property
    async def cost(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(self.url)

            cost_element = await page.query_selector('.product-info__main-price-num')
            cost = await cost_element.text_content()

            await browser.close()

            return re.search(r'\d+(?:\s*\d+)?(?:,\d+)?(?:\.\d+)?', cost).group().replace(",", ".")

    @property
    async def product_number(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(self.url)

            product_number_element = await page.query_selector('.product-info__order-title')
            product_number = await product_number_element.text_content()

            await browser.close()

            return re.search(r'\d+', product_number).group()

    @property
    async def amount(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(self.url)

            amount_element = await page.query_selector('.product-info__size-title')

            if amount_element:
                amount = await amount_element.text_content()
                amount = amount[10:]
            else:
                amount = ""

            await browser.close()

            return amount

    @property
    async def texts(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page()
            await page.goto(self.url)

            text_elements = await page.query_selector_all('.tabbody')
            header_elements = await page.query_selector_all('.tabhead__label-main')

            texts = {}

            for i in range(len(text_elements)):
                header_text = await header_elements[i].inner_text()
                text_content = await text_elements[i].inner_text()
                texts[header_text] = text_content

            await browser.close()

            return texts