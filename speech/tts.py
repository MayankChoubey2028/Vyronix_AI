import asyncio
import edge_tts


class TextToSpeech:

    def __init__(self):

        self.voice = "en-US-AriaNeural"

    async def speak(self, text, output_file="response.mp3"):

        communicate = edge_tts.Communicate(
            text=text,
            voice=self.voice
        )

        await communicate.save(output_file)

        return output_file