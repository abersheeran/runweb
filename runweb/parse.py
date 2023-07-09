import importlib
import ipaddress
import os
import socket
from functools import reduce
from typing import Any

import click


def parse_bind(value: str) -> socket.socket:
    if value.startswith("unix:"):
        path = value[5:]
        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(path)

        uds_perms = 0o666
        os.chmod(path, uds_perms)
        return sock

    if ":" not in value:
        raise click.BadParameter("Bind must be of the form: HOST:PORT")

    host, port = value.rsplit(":", 1)

    try:
        port = int(port)
    except ValueError:
        raise click.BadParameter("Bind port must be an integer")

    if not 0 < port < 65536:
        raise click.BadParameter("Bind port must be between 0 and 65536")

    address = ipaddress.ip_address(host)
    sock = socket.socket(
        socket.AF_INET if address.version == 4 else socket.AF_INET6, socket.SOCK_STREAM
    )
    if os.name != "nt":
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    else:  # In windows, SO_REUSEPORT is not available
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((str(address), port))
    return sock


def parse_application(value: str) -> Any:
    module_str, _, attrs_str = value.partition(":")
    if not module_str or not attrs_str:
        message = (
            'Import string "{import_str}" must be in format "<module>:<attribute>".'
        )
        raise click.BadParameter(message.format(import_str=value))

    module = importlib.import_module(module_str)
    instance = reduce(getattr, attrs_str.split("."), module)
    return instance
