from production_agent_runtime_api.ai.api.routers.ai_router import ai_router
from production_agent_runtime_api.api.routers.todo_router import todo_router
from production_agent_runtime_api.api.routers.auth_router import auth_router
from fastapi import FastAPI


app = FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)

app.include_router(ai_router)


@app.get("/")
def root():
    return {
        "status" : "running"
    }