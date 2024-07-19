from flask import Flask, send_file, request
from product import Product
import os
from image_processor import ImageProcessor
import io

app = Flask(__name__)

image_processor = ImageProcessor()

def get_img_names():
  filenames = []
  for filename in os.listdir("product_images"):
    filenames.append(filename)
  return filenames

img_names = get_img_names()

@app.route('/get-product', methods=['GET', 'POST'])
async def get_product():
    url = request.form['url']
    product = Product(url)

    img_transparent = image_processor.remove_backround(await product.img_url)
    cost = await product.cost
    product_number = await product.product_number
    amount = await product.amount
    texts = await product.texts
    img_transparent.save(f"product_images/{product_number}.png", format="PNG")
    img_names = get_img_names()
    return {
        "transparent_img_url" : f"http://127.0.0.1:5000/{product_number}.png",
        "cost" : cost,
        "product_number" : product_number,
        "amount" : amount,
        "texts" : texts
        }

@app.route(f"/<img_name>", methods=['GET'])
def get_img(img_name):
    image_path = f"product_images/{img_name}"
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
    except FileNotFoundError:
        return "Image not found", 404

    return send_file(io.BytesIO(image_data), mimetype="image/png", as_attachment=False)

if __name__ == '__main__':
    app.run(debug=True)
