from rag.pipeline import search_rag

from memory.chat_memory import ChatMemory

from vision.scene_memory import SceneMemory


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