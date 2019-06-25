"""
Routing for our application
"""
from typing import Any

from views import Handlers


def setup_routes(app: Any) -> None:
    """
    Setting up routes for our application
    :param app:
    :return:
    """
    handler = Handlers()
    app.router.add_get("/", handler.index)
    app.router.add_get("/ws", handler.websocket)
    app.router.add_static(
        "/static", path=app.config["STATIC_ROOT"], name="static")
