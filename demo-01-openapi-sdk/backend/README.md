# FastAPI Server (home made)

## Run the backend

``` bash
uv run fastapi dev
```

-   Swagger UI: http://127.0.0.1:8000/docs
-   ReDoc: http://127.0.0.1:8000/redoc
-   OpenAPI spec: http://127.0.0.1:8000/openapi.json

## OpenAPI

Display the OpenAPI specification:

``` bash
curl -s http://127.0.0.1:8000/openapi.json | jq
```

Save the specification as a formatted `openapi.json` file:

``` bash
curl -s http://127.0.0.1:8000/openapi.json | jq > openapi.json
```

## Development

The project uses [uv](https://docs.astral.sh/uv/) to manage Python
dependencies and [Ruff](https://docs.astral.sh/ruff/) to format Python
files.
