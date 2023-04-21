import uvicorn


def main():
    uvicorn.run(
        "agent_runner.web_server:server", host="127.0.0.1", port=8000, reload=True
    )
