from product import Product
import asyncio
from image_processor import ImageProcessor

async def main():
    product = Product("https://www.amway.cz/Bal%C3%AD%C4%8Dek-pro-nejmen%C5%A1%C3%AD-Plus-Nutrilite%E2%84%A2-/p/308133")
    img = await product.img_url
    cost = await product.cost
    product_number = await product.product_number
    amount = await product.amount
    texts = await product.texts

    image_processor = ImageProcessor()
    transparent_img = image_processor.remove_backround(await product.img_url)

    print(img)
    print(cost)
    print(product_number)
    print(amount)
    print(texts)

asyncio.run(main())