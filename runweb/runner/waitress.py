import multiprocessing

from typing import Any, Union

from waitress import create_server

from ..parse import parse_application, parse_bind
from ..multiprocess import multiprocess

spawn = multiprocessing.get_context("spawn")


def singleprocess(application: Any, bind_address: str) -> None:
    server = create_server(application, sockets=[parse_bind(bind_address)])
    server.run()


def wsgi(bind_address: str, application: str, workers_num: Union[int, None]) -> None:
    callback = parse_application(application)
    parse_bind(bind_address).close()

    if workers_num is None:
        singleprocess(callback, bind_address)
    else:
        multiprocess(
            workers_num,
            lambda: spawn.Process(target=singleprocess, args=(callback, bind_address)),
        )
