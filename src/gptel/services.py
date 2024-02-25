import os

from openai import AsyncOpenAI


class TranscriptionClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    async def transcript(self, audio_path: str) -> str:
        audio_file = open(audio_path, "rb")
        transcription = await self.client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="text",
        )

        return transcription
