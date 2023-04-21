from example_agents.adder_agent import AdderAgent
from celery.schedules import crontab

agent_config = {"adder": AdderAgent}

task_config = {
    "run-adder-agent-every-5-seconds": {
        "task": "agent_runner.tasks.execute_agent",
        "schedule": 5.0,
        "args": (
            "adder",
            (16, 16),
        ),
    },
    "add-every-minute": {
        "task": "agent_runner.tasks.add",
        "schedule": crontab(minute="*/1"),
        "args": (2, 5),
    },
}
