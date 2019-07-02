""" Views and service functions for them"""
import datetime
import json
from typing import Any, Dict

from aiohttp import WSMsgType, web
import aiohttp_jinja2
import aiosqlite
import jinja2


def setup_views(app: Any) -> Any:
    """
    Add jinja2 support and url for static files
    :param app: Application
    :return:
    """
    aiohttp_jinja2.setup(
        app,
        loader=jinja2.FileSystemLoader(
            str("{}/templates".format(app.config["PROJECT_ROOT"]))
        ),
    )
    app["static_root_url"] = app.config["STATIC_ROOT"]
    return app


class Handlers:
    """
    Views handlers
    """

    @aiohttp_jinja2.template("index.html")
    async def index(self, request: web.Request) -> Dict:
        """
        Handler for index page
        :param request: incoming request
        :return:
        """
        now = datetime.datetime.utcnow()
        last_moment = now - datetime.timedelta(hours=12)
        last_moment = last_moment.isoformat()
        query = (f"SELECT * FROM main.testimony "
                    f"WHERE time >= {last_moment}"
                    f"ORDER BY time ASC")
        async with aiosqlite.connect(request.app.config["DB_PATH"]) as database:
            async with database.execute(query) as cursor:
                rows = await cursor.fetchall()

        return {"data": json.dumps(rows)}

    async def websocket(self, request: web.Request) -> web.WebSocketResponse:
        """
        Handler for websocket endpoint
        :param request: incoming request
        :return:
        """
        websocket_response = web.WebSocketResponse()
        await websocket_response.prepare(request)

        request.app.websockets.append(websocket_response)

        async for msg in websocket_response:
            if msg.type == WSMsgType.TEXT:
                if msg.data == "close":
                    await websocket_response.close()
                else:
                    for listener_socket in request.app.websockets:
                        await listener_socket.send_str(msg.data)
            elif msg.type == WSMsgType.ERROR:
                print("ws connection closed with exception %s" %
                      websocket_response.exception())
        request.app.websockets.remove(websocket_response)
        return websocket_response
