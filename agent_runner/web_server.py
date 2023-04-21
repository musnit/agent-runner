from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, Json
from .runner import run, AgentRequest, InvalidAgentError

server = FastAPI()


class Result(BaseModel):
    result: Optional[str]
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
    except InvalidAgentError as e:
        return {"error": ErrorMessage(message=str(e)).json()}
    except ValidationError as e:
        return {"error": e.json()}
    return {"result": result}
