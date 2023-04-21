from pydantic import BaseModel, validator


class Agent:
    class Input(BaseModel):
        pass

    def run(self):
        pass
