from aiohttp import web


async def handle_404(request):
    location = request.app.router['main'].url_for()
    raise web.HTTPFound(location)


def create_error_middleware(overrides):

    @web.middleware
    async def error_middleware(request, handler):
        try:
            response = await handler(request)
            override = overrides.get(response.status)
            if override:
                return await override(request)
            return response
        except web.HTTPException as ex:
            override = overrides.get(ex.status)
            if override:
                return await override(request)
            raise

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware({
        404: handle_404,
    })
    app.middlewares.append(error_middleware)
