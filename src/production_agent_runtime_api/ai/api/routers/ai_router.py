from production_agent_runtime_api.ai.tools.todo_tools import UserContext
from production_agent_runtime_api.ai.workflows.todo_agent import workflow
from langchain.messages import HumanMessage
from production_agent_runtime_api.ai.core.agent_state import AgentState
from production_agent_runtime_api.core.security import get_user
from fastapi import Depends
from production_agent_runtime_api.models.user_model import UserModel
from production_agent_runtime_api.ai.schemas.chat_schemas import ChatRequestSchema
from fastapi import APIRouter, HTTPException


ai_router = APIRouter(prefix="/ai", tags=["AI"])



@ai_router.post("/chat")
async def chat_with_agent(
    request : ChatRequestSchema,
    user : UserModel = Depends(get_user)
):
    try:
        initial_state : AgentState = {
        "messages" : [HumanMessage(content=request.message)]
    }

        final_state : AgentState = await workflow.ainvoke(initial_state, context=UserContext(user_id=user.id))

        return final_state["messages"][-1].content

    except:
        raise HTTPException(
            status_code=500,
            detail="AI agent failed to process your request"
        )
