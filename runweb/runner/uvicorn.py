import multiprocessing

from typing import Any, Union

from uvicorn import Server, Config

from ..parse import parse_application, parse_bind
from ..multiprocess import multiprocess

spawn = multiprocessing.get_context("spawn")


def singleprocess(application: Any, bind_address: str) -> None:
    config = Config(application)
    server = Server(config)
    server.run([parse_bind(bind_address)])


def asgi(bind_address: str, application: str, workers_num: Union[int, None]) -> None:
    callback = parse_application(application)
    parse_bind(bind_address).close()

    if workers_num is None:
        singleprocess(callback, bind_address)
    else:
        multiprocess(
            workers_num,
            lambda: spawn.Process(target=singleprocess, args=(callback, bind_address)),
        )
