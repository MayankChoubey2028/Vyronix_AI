from collections import deque


class ChatMemory:
    """
    Stores recent conversations between the user and the assistant.
    """

    def __init__(self, max_history=10):

        self.history = deque(maxlen=max_history)


    def add_message(self, role: str, message: str):
        """
        Add a message to memory.

        role -> "user" or "assistant"
        """

        self.history.append({
            "role": role,
            "message": message
        })


    def get_history(self):
        """
        Return all stored messages.
        """

        return list(self.history)


    def get_context(self):
        """
        Convert history into a single string for the LLM.
        """

        conversation = ""

        for item in self.history:

            conversation += (
                f"{item['role'].capitalize()}: "
                f"{item['message']}\n"
            )

        return conversation.strip()


    def clear(self):
        """
        Clear chat history.
        """

        self.history.clear()


    def size(self):
        """
        Number of stored messages.
        """

        return len(self.history)