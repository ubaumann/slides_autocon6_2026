from typing import Any

from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse, RedirectResponse

from .models import ErrorModel, ErspanSession

app = FastAPI(
    title="ERSPAN API",
    version="1.0.0",
    description="Simple example of an API for AutoCon6",
)

sessions: dict[str, ErspanSession] = {}


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse("./redoc")


@app.get("/erspan-sessions")
def list_sessions() -> list[ErspanSession]:
    return list(sessions.values())


@app.post("/erspan-sessions", status_code=201, response_model=ErspanSession, responses={409: {"model": ErrorModel}})
def create_session(session: ErspanSession) -> ErspanSession | JSONResponse:
    if session.name in sessions:
        return JSONResponse(
            status_code=409,
            content={
                "title": "Session already exists",
                "status": 409,
                "detail": f"Sesson {session.name} already exists",
            },
        )

    sessions[session.name] = session
    return session


@app.get("/erspan-sessions/{name}", response_model=ErspanSession, responses={404: {"model": ErrorModel}})
def get_session(name: str) -> ErspanSession | JSONResponse:
    if name not in sessions:
        return JSONResponse(
            status_code=404,
            content={
                "title": "Session not found",
                "status": 404,
                "detail": f"Sesson {name} not found",
            },
        )

    return sessions[name]


@app.put(
    "/erspan-sessions/{name}",
    response_model=ErspanSession,
    responses={404: {"model": ErrorModel}, 409: {"model": ErrorModel}},
)
def update_session(name: str, session: ErspanSession) -> ErspanSession | JSONResponse:
    if name not in sessions:
        return JSONResponse(
            status_code=404,
            content={
                "title": "Session not found",
                "status": 404,
                "detail": f"Sesson {name} not found",
            },
        )

    if session.name != name:
        return JSONResponse(
            status_code=409,
            content={
                "title": "Session name mismatch",
                "status": 409,
                "detail": f"Sesson {session.name} does not match {name}",
            },
        )

    sessions[name] = session
    return session


@app.delete(
    "/erspan-sessions/{name}", status_code=204, responses={404: {"model": ErrorModel}}
)
def delete_session(name: str) -> Response:
    if name not in sessions:
        return JSONResponse(
            status_code=404,
            content={
                "title": "Session not found",
                "status": 404,
                "detail": f"Sesson {name} not found",
            },
        )

    del sessions[name]
    return Response(status_code=204)


@app.get("/schemas/erspan-session.json")
def get_erspan_schema() -> dict[str, Any]:
    return ErspanSession.model_json_schema()
