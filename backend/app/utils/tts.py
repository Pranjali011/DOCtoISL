import os
import uuid
from gtts import gTTS

# Directory for saving speech files
AUDIO_OUTPUT_DIR = "generated_audio"
os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)


def safe_filename(text: str, length=20):
    """
    Create a safe, clean filename from text.
    """
    cleaned = "".join(c for c in text if c.isalnum() or c == " ").strip()
    cleaned = cleaned.replace(" ", "_").lower()
    return cleaned[:length] if cleaned else "audio"


def generate_speech_audio(text: str) -> str:
    """
    Convert text to speech using gTTS.
    Handles large text and network errors.
    Returns the path of the generated MP3 file.
    """

    text = text.strip()
    if not text:
        return ""

    # Unique filename
    filename = f"{safe_filename(text)}_{uuid.uuid4().hex[:8]}.mp3"
    file_path = os.path.join(AUDIO_OUTPUT_DIR, filename)

    try:
        # gTTS cannot handle extremely long text in one call
        if len(text) > 200:
            # Break into chunks
            chunks = [text[i:i+200] for i in range(0, len(text), 200)]
            combined = ""

            for chunk in chunks:
                tts = gTTS(text=chunk, lang="en")
                temp_path = os.path.join(AUDIO_OUTPUT_DIR, f"temp_{uuid.uuid4().hex[:8]}.mp3")
                tts.save(temp_path)
                combined += temp_path + "|"

            # Merge audio chunks
            from pydub import AudioSegment
            final_audio = AudioSegment.empty()

            for temp_file in combined.split("|"):
                if temp_file and os.path.exists(temp_file):
                    final_audio += AudioSegment.from_mp3(temp_file)
                    os.remove(temp_file)

            final_audio.export(file_path, format="mp3")

        else:
            tts = gTTS(text=text, lang="en")
            tts.save(file_path)

    except Exception as e:
        print(f"[TTS ERROR] {e}")
        return ""

    return file_path
