from .celery import celery
from .runner import run, AgentRequest


@celery.task
def add(x, y):
    return x + y


@celery.task
def execute_agent(name, input):
    result = run(AgentRequest(name=name, input=input))
    return result
