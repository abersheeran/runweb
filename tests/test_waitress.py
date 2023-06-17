import httpx

from .utils import run_command


def test_single_process():
    with run_command("runweb -s waitress -a app:wsgi") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"


def test_multi_process():
    with run_command("runweb -s waitress -a app:wsgi -w 2") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"


def test_reload():
    with run_command("runweb -s waitress -a app:wsgi --reload") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"


def test_reload_multi_process():
    with run_command("runweb -s waitress -a app:wsgi --reload -w 2") as url:
        response = httpx.get(url)
        assert response.status_code == 200
        assert response.text == "Hello World!"
