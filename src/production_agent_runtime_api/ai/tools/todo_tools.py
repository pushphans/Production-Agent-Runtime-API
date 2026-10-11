from production_agent_runtime_api.core.db import session_factory
from production_agent_runtime_api.schemas.todo_schemas import CreateTodoRequestModel
from uuid import UUID
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from production_agent_runtime_api.services import todo_service





@dataclass
class UserContext:
    user_id : UUID




@tool
async def create_todo(
    title : str,
    description : str | None,
    runtime : ToolRuntime[UserContext]
):
    """Creates new todo for an authenticated user"""

    try:
        user_id = runtime.context.user_id

        data = CreateTodoRequestModel(
            title=title,
            description=description,
            is_completed=False
        )


        async with session_factory() as tool_db:

            todo = await todo_service.create_todo(data=data, db=tool_db, user_id=user_id)

            return {
                "status" : "success",
                "todo_id" : str(todo.id),
                "title" : todo.title
            }

    except ValueError as ve:
        return {
            "status" : "error",
            "message" : str(ve),
            "retryable" : False
        }

    except Exception as e:
        return {
            "status" : "error",
            "message" : "Unable to create todo due to internal error",
            "retryable" : False
        }
