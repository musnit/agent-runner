from pydantic import BaseModel, Json
from typing import Any, Optional
from .config import agent_config


class InvalidAgentError(Exception):
    pass


class AgentRequest(BaseModel):
    name: str
    input: Optional[Any]


class AgentResponse(BaseModel):
    result: Json


def run(request: AgentRequest) -> AgentResponse:
    agent_type = agent_config.get(request.name)
    if not agent_type:
        raise InvalidAgentError("Invalid agent name")
    agent = agent_type()
    input = agent.Input(input=request.input)
    result = agent.run(input)
    return result
