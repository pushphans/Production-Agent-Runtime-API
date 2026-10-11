from production_agent_runtime_api.schemas.todo_schemas import UpdateTodoResponseModel
from production_agent_runtime_api.models.todo_model import TodoModel
from production_agent_runtime_api.schemas.todo_schemas import CreateTodoResponseModel
from production_agent_runtime_api.schemas.todo_schemas import UpdateTodoRequestSchema
from fastapi.openapi.utils import status_code_ranges
from uuid import UUID
from fastapi import status
from fastapi import HTTPException
from production_agent_runtime_api.schemas.todo_schemas import CreateTodoRequestModel
from production_agent_runtime_api.core.security import get_user
from production_agent_runtime_api.models.user_model import UserModel
from production_agent_runtime_api.core.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
from production_agent_runtime_api.services import todo_service



todo_router = APIRouter(prefix="/todos", tags = ["TODO"])


@todo_router.post("/todo")
async def create_todo(
    data : CreateTodoRequestModel,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_user),
):

    try:
        result = await todo_service.create_todo(data=data, user_id=user.id, db=db)
        return CreateTodoResponseModel(
            id= result.id,
            title=result.title,
            description=result.description,
            is_completed=result.is_completed,
            created_at=result.created_at,
            updated_at=result.updated_at
        )

    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )



@todo_router.get("/todo")
async def list_todos(
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_user),
    page : int = 1,
    page_size : int = 10,
    is_completed : bool | None = None,
    search_term : str | None = None
):
    try:
        result : TodoModel = await todo_service.list_todos(db=db, user_id=user.id, page=page, page_size=page_size, search_term=search_term, is_completed=is_completed)
        return result

    except LookupError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        )

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )
@todo_router.get("/todo/{todo_id}")
async def get_todo(
    todo_id : UUID,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_user)
):
    try:
        result = await todo_service.get_todo(user_id=user.id, db=db, todo_id=todo_id)

        return CreateTodoResponseModel(
            id= result.id,
            title=result.title,
            description=result.description,
            is_completed=result.is_completed,
            created_at=result.created_at,
            updated_at=result.updated_at
        )

    except LookupError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        )

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )

@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_id : UUID,
    data : UpdateTodoRequestSchema,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_user)
):

    try:
        result = await todo_service.update_todo(todo_id=todo_id, db=db, user_id=user.id, data=data)
        return UpdateTodoResponseModel(
            id= result.id,
            title=result.title,
            description=result.description,
            is_completed=result.is_completed,
            created_at=result.created_at,
            updated_at=result.updated_at
        )

    except LookupError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        )

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )


@todo_router.delete("/todo/{todo_id}")
async def delete_todo(
    todo_id : UUID,
    db : AsyncSession = Depends(get_db),
    user : UserModel = Depends(get_user),
):
    try:
        await todo_service.delete_todo(db=db, user_id=user.id, todo_id=todo_id)

        return {
            "message" : "Todo deleted successfully"
        }

    except LookupError:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Todo not found"
        )

    except Exception:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = "Internal server error"
        )
