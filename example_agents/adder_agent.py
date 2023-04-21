from pydantic import BaseModel, validator
from agent_runner.agent import Agent
from typing import List


class AdderAgent(Agent):
    class Input(BaseModel):
        input: List[int]

        @validator("input")
        def input_must_be_length_2(cls, value):
            if len(value) is not 2:
                raise ValueError("must be exactly 2 items in input list")
            return value

    def run(self, input: Input):
        return input.input[0] + input.input[1]
