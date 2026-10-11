from production_agent_runtime_api.ai.tools.todo_tools import UserContext
from langchain.messages import SystemMessage, HumanMessage
from production_agent_runtime_api.ai.core.agent_state import AgentState
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from production_agent_runtime_api.core.config import settings
from langgraph.prebuilt import ToolNode, tools_condition
from production_agent_runtime_api.ai.tools.todo_tools import create_todo

llm = init_chat_model(model="qwen/qwen3.8-27b", model_provider="groq", api_key = settings.GROQ_API_KEY)

tools = [create_todo]

llm_with_tools = llm.bind_tools(tools=tools)




# Nodes
async def react_node(state : AgentState) -> dict:

    messages = state["messages"]

    system_prompt = SystemMessage(content=f"""
    You are a Todo assistant.
    Use create_todo when the user asks to create a todo.
    Never claim success if a tool reports an error.
    Do not retry failed create operations automatically.
    """)

    response = await llm_with_tools.ainvoke([system_prompt] + messages)

    return {
        "messages" : [response]
    }


tool_node = ToolNode(tools=tools)






# State graph
graph = StateGraph(state_schema=AgentState, context_schema=UserContext)

graph.add_node("react_node", react_node)
graph.add_node("tool_node", tool_node)

graph.add_edge(START, "react_node")
graph.add_conditional_edges(
    "react_node",
    tools_condition,
    {
        "tools" : "tool_node",
        "__end__" : END
    }
)
graph.add_edge("tool_node", "react_node")



workflow = graph.compile()
