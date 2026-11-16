# FastAPI Server (generated)

Generating FastAPI from OpenAPI spec using [datamodel-code-generator](https://datamodel-code-generator.koxudaxi.dev/fastapi-server/).

All settings are in `pyproject.toml`.

## Generate FastAPI server

```
uv run datamodel-codegen
```

## Run the server

```
uv run fastapi dev --entrypoint app.server.main:app
```

## NotImplementedError

When generating the application and service, DMCG does not know the business logic (in our case just an in-memory dictionary) and adds `NotImplementedError` in the code.