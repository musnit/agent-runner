from .adder_agent import AdderAgent
from pydantic import BaseModel
from typing import Any, Optional


class InvalidAgentError(Exception):
    pass


class AgentRequest(BaseModel):
    name: str
    input: Optional[Any]


agents = {"adder": AdderAgent}


def run(request: AgentRequest):
    agent_type = agents.get(request.name)
    if not agent_type:
        raise InvalidAgentError("Invalid agent name")
    agent = agent_type()
    input = agent.Input(input=request.input)
    result = agent.run(input)
    return result
