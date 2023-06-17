import multiprocessing
import os
import signal
import threading
from multiprocessing.context import SpawnProcess
from typing import Callable

import click

multiprocessing.allow_connection_pickling()


def multiprocess(workers_num: int, create_process: Callable[[], SpawnProcess]) -> None:
    should_exit = threading.Event()

    click.echo(
        "Started parent process [{}]".format(
            click.style(str(os.getpid()), fg="cyan", bold=True)
        )
    )

    for sig in (
        signal.SIGINT,  # Sent by Ctrl+C.
        signal.SIGTERM,  # Sent by `kill <pid>`.
    ):
        signal.signal(sig, lambda sig, frame: should_exit.set())

    processes: list[SpawnProcess] = []
    for _ in range(workers_num):
        process = create_process()
        processes.append(process)
        process.start()
        click.echo(
            "Started child process [{}]".format(
                click.style(str(process.pid), fg="cyan", bold=True)
            )
        )

    while not should_exit.wait(0.5):
        for idx, process in enumerate(tuple(processes)):
            if process.is_alive():
                continue

            click.echo(
                "Child process [{}] died unexpectedly".format(
                    click.style(str(process.pid), fg="cyan", bold=True)
                )
            )
            del processes[idx]
            process = create_process()
            processes.append(process)
            process.start()
            click.echo(
                "Started child process [{}]".format(
                    click.style(str(process.pid), fg="cyan", bold=True)
                )
            )

    click.echo(
        "Stopping parent process [{}]".format(
            click.style(str(os.getpid()), fg="cyan", bold=True)
        )
    )

    for process in processes:
        if process.pid is None:
            continue

        if os.name == "nt":
            # Windows doesn't support SIGTERM.
            os.kill(process.pid, signal.CTRL_BREAK_EVENT)
        else:
            os.kill(process.pid, signal.SIGTERM)

    for process in processes:
        click.echo(
            "Waiting for child process [{}] to terminate".format(
                click.style(str(process.pid), fg="cyan", bold=True)
            )
        )
        process.join()
