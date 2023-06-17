import importlib
import os
import socket
import ipaddress
from functools import reduce
from typing import Any

import click


def parse_bind(value) -> socket.socket:
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
    sock.bind((str(address), port))
    return sock


def parse_application(value) -> Any:
    module_str, _, attrs_str = value.partition(":")
    if not module_str or not attrs_str:
        message = (
            'Import string "{import_str}" must be in format "<module>:<attribute>".'
        )
        raise click.BadParameter(message.format(import_str=value))

    try:
        module = importlib.import_module(module_str)
    except ImportError as exc:
        if exc.name != module_str:
            raise exc from None
        message = 'Could not import module "{module_str}".'
        raise click.BadParameter(message.format(module_str=module_str))

    try:
        instance = reduce(getattr, attrs_str.split("."), module)
    except AttributeError:
        message = 'Attribute "{attrs_str}" not found in module "{module_str}".'
        raise click.BadParameter(
            message.format(attrs_str=attrs_str, module_str=module_str)
        )

    return instance
