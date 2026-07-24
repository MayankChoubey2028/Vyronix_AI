from rag.pipeline import search_rag

from memory.chat_memory import ChatMemory

from vision.scene_memory import SceneMemory


# Singletons shared across the whole agent - imported by name elsewhere
# (agent.py imports add_to_history, main.py imports scene_memory)
chat_memory = ChatMemory()

scene_memory = SceneMemory()


def rag_tool(question, db):

    docs = search_rag(question, db)

    return "\n".join(
        doc.page_content for doc in docs
    )


def history_tool():

    return chat_memory.get_context()


def scene_tool():

    scene = scene_memory.get_scene()

    return str(scene)


def add_to_history(question, answer):
    """
    Call this after every answered question so future turns
    have real conversation context instead of an empty history.
    """

    chat_memory.add_message("user", question)
    chat_memory.add_message("assistant", answer)