import httpx

from .utils import run_command


def test_single_process():
    with run_command("runweb -s uvicorn -a app:asgi") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"


def test_multi_process():
    with run_command("runweb -s uvicorn -a app:asgi -w 2") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"


def test_reload():
    with run_command("runweb -s uvicorn -a app:asgi --reload") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"


def test_reload_multi_process():
    with run_command("runweb -s uvicorn -a app:asgi --reload -w 2") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"
