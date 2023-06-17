from __future__ import annotations

import multiprocessing
import socket

from typing import Any

from waitress import create_server

from ..parse import parse_application, parse_bind
from ..multiprocess import multiprocess

spawn = multiprocessing.get_context("spawn")


def singleprocess(application: Any, bind: socket.socket) -> None:
    server = create_server(application, sockets=[bind])
    server.run()


def wsgi(bind_address: str, application: str, workers_num: int | None) -> None:
    callback = parse_application(application)
    bind_socket = parse_bind(bind_address)

    if workers_num is None:
        singleprocess(callback, bind_socket)
    else:

        def create_process():
            process = spawn.Process(target=singleprocess, args=(callback, bind_socket))
            return process

        multiprocess(workers_num, create_process)
