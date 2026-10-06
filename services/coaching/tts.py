from io import BytesIO
from gtts import gTTS

class TextToSpeech:
    def speak(self, text, lang = "en"):
        cleaned = (text or "").strip()

        if not cleaned:
            return

        buffer = BytesIO()
        gTTS(text=cleaned, lang=lang).write_to_fp(buffer)
        # gTTS cleaned text ko speech mein convert karta hai.
        # write_to_fp(buffer) ka matlab:
        # Generated audio ko directly buffer ke andar likh do.
        #
        # Example:
        # "Keep your back straight."
        #          ↓
        #       gTTS
        #          ↓
        #      MP3 audio
        #          ↓
        #       buffer
        buffer.seek(0)
        # Buffer ke cursor ko beginning (position 0) par le ja rahe hain.
        # Kyunki audio likhne ke baad cursor end par hota hai.

        return buffer.read()