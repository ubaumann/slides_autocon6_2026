# Demo 03 - NETCONF Deploy

NETCONF deploy demo using Nornir async + Pydantic models.

## Run

```bash
uv run python main.py
```

## What it does

Configures ERSPAN monitor session via NETCONF on Cisco NX-OS:
- Generate XML from Pydantic model
- Lock candidate datastore
- Edit config
- Validate
- Commit with confirm (120s timeout)
- Unlock

## Stack

- **Nornir async**: Public alpha, async task execution
- **nornir-scrapli**: Custom branch `dga/feat-v2-async-m8ppp` for latest features
- **pydantify**: Generated model from YANG (`model/span.py`)
- **pydantify-common**: XML generation via `model_dump_xml()`

## Model notes

Base class manually replaced `BaseModel` → `XMLPydantifyModel` in generated code.
