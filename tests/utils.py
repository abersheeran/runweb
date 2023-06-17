import os
import random
import signal
import subprocess
import time
from contextlib import contextmanager
from typing import Generator


@contextmanager
def run_command(command: str) -> Generator[str, None, None]:
    for _ in range(3):
        port = random.randint(20000, 60000)
        process = subprocess.Popen(
            command + f" -b 127.0.0.1:{port}",
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            creationflags=0 if os.name != "nt" else subprocess.CREATE_NEW_PROCESS_GROUP,
        )
        time.sleep(1)
        if process.poll() is None:
            break
        stdout, stderr = process.communicate()
        print(stdout.decode())
        print(stderr.decode())

    yield f"http://127.0.0.1:{port}"

    os.kill(process.pid, signal.SIGINT if os.name != "nt" else signal.CTRL_C_EVENT)
