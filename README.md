# RunWeb

Run web server with one command.

## Installation

```bash
$ pip install runweb
```

If you need auto reload, install with `reload` extra.

```bash
$ pip install "runweb[reload]"
```

## Usage

### `waitress`

Install with `waitress` extra.

```bash
$ pip install "runweb[waitress]"
```

Then run command.

```bash
$ runweb -a app:wsgi
```

If you need a multi-process waitress service, just run the following command:

```bash
$ runweb -a app:wsgi -w 4
```

### `uvicorn`

Install with `uvicorn` extra.

```bash
$ pip install "runweb[uvicorn]"
```

Then run command.

```bash
$ runweb -a app:asgi
```

If you need a multi-process uvicorn service, just run the following command:

```bash
$ runweb -a app:asgi -w 4
```
