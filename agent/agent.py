from groq import Groq

from dotenv import load_dotenv

import os

from .graph import execute_tools

from .prompts import build_prompt

from .tools import add_to_history


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def ask(question, db):

    data = execute_tools(question, db)

    prompt = build_prompt(
        question=question,
        history=data["history"],
        scene=data["scene"],
        context=data["context"]
    )

    response = client.chat.completions.create(

        model="llama-3.3-70b-versatile",

        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ]
    )

    answer = response.choices[0].message.content

    # Record this turn so the next question has real chat history
    add_to_history(question, answer)

    return answer