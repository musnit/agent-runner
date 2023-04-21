from typing import Optional, Any
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, Json
from .runner import run, AgentRequest, InvalidAgentError

server = FastAPI()


class Result(BaseModel):
    result: Optional[Any]
    error: Json


class ErrorMessage(BaseModel):
    message: str


@server.get("/ping", response_model=Result, response_model_exclude_none=True)
async def ping():
    return {"result": "pong"}


@server.post("/run_agent", response_model=Result, response_model_exclude_none=True)
async def run_agent(request: AgentRequest):
    try:
        result = run(request)
    except ValidationError as e:
        return {"error": e.json()}
    except (InvalidAgentError, ValueError) as e:
        return {"error": ErrorMessage(message=str(e)).json()}
    return {"result": result}
