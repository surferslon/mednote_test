import motor.motor_asyncio
import aiohttp
from datetime import datetime, timedelta
from aiohttp import web
from middlewares import setup_middlewares


DB_URL = 'mongodb://mongo:27017'
PAGE_NAME = 'yandex'
PAGE_URL = 'https://yandex.ru'
INTERVAL = 7


async def main(request):
    cached_page = await col.find_one({'page_name': PAGE_NAME})
    if (not cached_page) or (datetime.now() - cached_page['date']) > timedelta(days=INTERVAL):
        async with aiohttp.ClientSession() as session:
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


db = motor.motor_asyncio.AsyncIOMotorClient(DB_URL).main_database
col = db.cached_pages
app = web.Application()
setup_middlewares(app)
app.add_routes([
    web.get('/', main, name='main')
])
web.run_app(app)
