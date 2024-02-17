import asyncio
from pyppeteer import launch
import json
from flask import escape

async def scrape_americanas(url):
    # Configurando o navegador em modo headless
    browser = await launch(headless=True, args=['--no-sandbox'])
    page = await browser.newPage()
    await page.goto(url)

    # Aguardar até que os elementos do produto estejam presentes
    await page.waitForSelector('.product-title__Title-sc-1hlrxcw-0')
    await page.waitForSelector('.priceSales')

    # Extrair informações do produto
    product_title = await page.querySelectorEval('.product-title__Title-sc-1hlrxcw-0', 'element => element.textContent')
    product_price = await page.querySelectorEval('.priceSales', 'element => element.textContent')

    await browser.close()

    # Organizar as informações em um dicionário
    data = {
        "product": {
            "title": product_title.strip(),
            "price": product_price.strip()
        }
    }

    return data

def scrape_function(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json and 'url' in request_json:
        url = request_json['url']
    elif request_args and 'url' in request_args:
        url = request_args['url']
    else:
        return 'URL is required', 400

    result = asyncio.get_event_loop().run_until_complete(scrape_americanas(url))
    return json.dumps(result, indent=4), 200, {'Content-Type': 'application/json'}
