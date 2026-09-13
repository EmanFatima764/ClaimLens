from groq import Groq

from config import Config


class STTService:
    """
    Converts audio (a mic recording from st.audio_input, or a file from
    st.file_uploader) into text using Groq's hosted Whisper model.
    """

    MAX_FILE_SIZE_MB = 25  # Groq's per-file limit

    def __init__(self):
        if not Config.GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY is not configured.")
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.model = Config.WHISPER_MODEL

    def transcribe_audio(self, audio_source) -> str:
        if audio_source is None:
            raise ValueError("No audio source provided.")

        try:
            audio_bytes = audio_source.getvalue()
        except AttributeError:
            audio_bytes = audio_source.read()

        if not audio_bytes:
            raise ValueError("Audio file is empty.")

        size_mb = len(audio_bytes) / (1024 * 1024)
        if size_mb > self.MAX_FILE_SIZE_MB:
            raise ValueError(
                f"Audio file is {size_mb:.1f}MB, which exceeds the "
                f"{self.MAX_FILE_SIZE_MB}MB limit. Please use a shorter clip."
            )

        filename = getattr(audio_source, "name", None) or "recording.wav"

        try:
            transcription = self.client.audio.transcriptions.create(
                file=(filename, audio_bytes),
                model=self.model,
                response_format="verbose_json",
                temperature=0,
            )
        except Exception as e:
            raise RuntimeError(f"Groq transcription request failed: {e}") from e

        text = getattr(transcription, "text", None)
        if text is None and isinstance(transcription, dict):
            text = transcription.get("text")
        if text is None and isinstance(transcription, str):
            text = transcription

        if not text or not str(text).strip():
            raise RuntimeError(
                "Transcription returned no text. Please speak clearly and try again."
            )

        return str(text).strip()
