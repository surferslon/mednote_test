import motor.motor_asyncio
import aiohttp
from datetime import datetime, timedelta
from aiohttp import web
from middlewares import setup_middlewares


async def main(request):
    cached_page = await col.find_one({'page_name': PAGE_NAME})
    if (datetime.now() - cached_page['date']) > timedelta(seconds=10):
        async with session.get(PAGE_URL) as resp:
            response_text = await resp.text()
            cached_item = {'page_name': PAGE_NAME, 'date': datetime.now(), 'content': response_text}
            if cached_page:
                await col.update_one({'page_name': PAGE_NAME}, {'$set': cached_item})
            else:
                await col.insert_one(cached_item)
        raise web.HTTPFound(PAGE_URL)
    else:
        return web.Response(text=cached_page['content'], content_type='text/html')


PAGE_NAME = 'yandex'
PAGE_URL = 'https://yandex.ru'

db = motor.motor_asyncio.AsyncIOMotorClient().main_database
col = db.cached_pages

session = aiohttp.ClientSession()
app = web.Application()
setup_middlewares(app)
app.add_routes([
    web.get('/', main, name='main')
])

web.run_app(app)
