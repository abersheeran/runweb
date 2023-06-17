from typing import Union

import click

from .parse import parse_application


SERVERS = {"wsgi": {}, "asgi": {}}

try:
    from .runner.waitress import wsgi as wsgi_waitress
except ImportError:
    pass
else:
    SERVERS["wsgi"]["waitress"] = wsgi_waitress

try:
    from .runner.uvicorn import asgi as asgi_uvicorn
except ImportError:
    pass
else:
    SERVERS["asgi"]["uvicorn"] = asgi_uvicorn


@click.group(invoke_without_command=True)
@click.option(
    "-s",
    "--server",
    "server_name",
    type=click.Choice(list(s for v in SERVERS.values() for s in v.keys())),
    default=None,
    help="The server to use to serve the application.",
)
@click.option(
    "-i",
    "--interface",
    type=click.Choice(list(SERVERS.keys())),
    default=None,
    help="The interface to use to serve the application.",
)
@click.option(
    "-a",
    "--application",
    help="`module:attribute` or `package.module:attribute`",
)
@click.option(
    "-b",
    "--bind",
    "bind_address",
    default="127.0.0.1:8000",
    show_default=True,
    help="A string of the form: HOST:PORT, unix:PATH",
)
@click.option(
    "--reload/--no-reload",
    "autoreload",
    default=False,
    show_default=True,
    help="Reload the application on python module changes",
)
@click.option(
    "-w",
    "--workers",
    "workers_num",
    default=None,
    type=int,
    show_default=True,
    help="Number of worker processes for handling requests",
)
@click.pass_context
def cli(
    ctx: click.Context,
    server_name: Union[str, None],
    interface: Union[str, None],
    application: str,
    bind_address: str,
    autoreload: bool,
    workers_num: Union[int, None],
) -> None:
    if ctx.invoked_subcommand is not None:
        return

    if application is None:
        raise click.UsageError("Missing option '--application' / '-a'.")

    if interface is None:
        try:
            co = parse_application(application)(None, None, None)
            interface = "asgi"
        except TypeError:
            interface = "wsgi"
        else:
            # close the coroutine, disable the warning
            co.close()

    if server_name is None:
        servers = SERVERS.get(interface)
        if servers:
            server_name = next(iter(servers))
        else:
            raise click.UsageError(
                f"No server found for interface `{interface}`. "
                "Try installing a server for this interface."
            )

    try:
        server = SERVERS[interface][server_name]
    except KeyError:
        raise click.UsageError(
            f"No server found for interface `{interface}` and server `{server_name}`. "
        )

    if autoreload:
        try:
            import hupper
        except ImportError:
            raise click.UsageError(
                "Autoreload requires the `hupper` package to be installed."
            )

        # start_reloader will only return in a monitored subprocess
        reloader = hupper.start_reloader(
            f"{server.__module__}.{server.__qualname__}",
            shutdown_interval=3,  # type: ignore
            worker_kwargs={
                "bind_address": bind_address,
                "application": application,
                "workers_num": workers_num,
            },
        )
        # monitor an extra file
        reloader.watch_files([".env"])
        return

    server(bind_address=bind_address, application=application, workers_num=workers_num)


try:
    from trogon import tui
except ImportError:
    pass
else:
    cli = tui()(cli)
