from agent.tools import (
    rag_tool,
    history_tool,
    scene_tool
)


def execute_tools(question, db):

    context = rag_tool(question, db)

    history = history_tool()

    scene = scene_tool()

    return {
        "context": context,
        "history": history,
        "scene": scene
    }