import multiprocessing
from typing import Union

import click
from waitress import create_server

from ..logging import logger
from ..multiprocess import multiprocess
from ..parse import parse_application, parse_bind

spawn = multiprocessing.get_context("spawn")


def singleprocess(application: str, bind_address: str) -> None:
    server = create_server(
        parse_application(application),
        sockets=[parse_bind(bind_address)],
    )
    server.run()


def wsgi(bind_address: str, application: str, workers_num: Union[int, None]) -> None:
    parse_bind(bind_address).close()

    logger.info(
        "Binding to {}".format(
            click.style(bind_address, fg="green", bold=True),
        )
    )

    if workers_num is None:
        singleprocess(application, bind_address)
    else:
        multiprocess(
            workers_num,
            lambda: spawn.Process(
                target=singleprocess, args=(application, bind_address)
            ),
        )
