import multiprocessing
import socket

from typing import Any, Union

from uvicorn import Server, Config

from ..parse import parse_application, parse_bind
from ..multiprocess import multiprocess

spawn = multiprocessing.get_context("spawn")


def singleprocess(application: Any, bind: socket.socket) -> None:
    config = Config(application)
    server = Server(config)
    server.run([bind])


def asgi(bind_address: str, application: str, workers_num: Union[int, None]) -> None:
    callback = parse_application(application)
    bind_socket = parse_bind(bind_address)

    if workers_num is None:
        singleprocess(callback, bind_socket)
    else:

        def create_process():
            process = spawn.Process(target=singleprocess, args=(callback, bind_socket))
            return process

        multiprocess(workers_num, create_process)
