from sqlalchemy import select
from production_agent_runtime_api.models.todo_model import TodoModel
from production_agent_runtime_api.schemas.todo_schemas import UpdateTodoRequestSchema
from production_agent_runtime_api.schemas.todo_schemas import CreateTodoRequestModel
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession



async def create_todo(
    db : AsyncSession,
    user_id : UUID,
    data : CreateTodoRequestModel
) -> TodoModel:
    try:
        todo = TodoModel(
        title = data.title,
        description = data.description,
        is_completed = data.is_completed,
        user_id = user_id
    )

        db.add(todo)
        await db.commit()
        await db.refresh(todo)

        return todo

    except Exception:
        await db.rollback()
        raise


async def list_todos(
    db : AsyncSession,
    user_id : UUID,
    page : int = 1,
    page_size : int = 10,
    is_completed : bool | None = None,
    search_term : str | None = None
) -> list[TodoModel]:

    query = (
        select(TodoModel)
        .where(TodoModel.user_id == user_id)
    )

    if search_term is not None:
        query = query.where(TodoModel.title.ilike(f"%{search_term}%"))

    if is_completed is not None:
        query = query.where(TodoModel.is_completed == is_completed)


    offset = (page -1) * page_size

    query = query.offset(offset).limit(page_size)

    result = await db.execute(query)

    todos = result.scalars().all()

    return todos



async def get_todo(
    todo_id : UUID,
    db : AsyncSession,
    user_id : UUID
) -> TodoModel:


    query = (
        select(TodoModel)
        .where(TodoModel.user_id == user_id, TodoModel.id == todo_id)
    )

    result = await db.execute(query)

    todo = result.scalar_one_or_none()

    if todo is None:
        raise LookupError("No todo found")

    return todo



async def update_todo(
    db : AsyncSession,
    user_id : UUID,
    todo_id : UUID,
    data : UpdateTodoRequestSchema
) -> TodoModel:

    try:
        query = (
        select(TodoModel)
        .where(TodoModel.user_id == user_id, TodoModel.id == todo_id)
    )

        result = await db.execute(query)

        todo = result.scalar_one_or_none()

        if todo is None:
            raise LookupError("Todo not found")

        todo.title = data.title
        todo.description = data.description
        todo.is_completed = data.is_completed

        await db.commit()
        await db.refresh(todo)

        return todo

    except Exception:
        await db.rollback()
        raise

async def delete_todo(
    db : AsyncSession,
    user_id : UUID,
    todo_id : UUID
) -> bool:
    try:
        query = (
        select(TodoModel)
        .where(TodoModel.user_id == user_id, TodoModel.id == todo_id)
    )

        result = await db.execute(query)

        todo = result.scalar_one_or_none()

        if todo is None:
            raise LookupError("Todo not found")

        await db.delete(todo)
        await db.commit()

        return True


    except Exception:
        await db.rollback()
        raise
