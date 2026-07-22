from faster_whisper import WhisperModel


class SpeechToText:

    def __init__(self):

        self.model = WhisperModel(
            "base",
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio_path):

        segments, info = self.model.transcribe(audio_path)

        text = ""

        for segment in segments:
            text += segment.text + " "

        return text.strip()