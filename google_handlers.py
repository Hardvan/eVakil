from googletrans import Translator
from gtts import gTTS
import os


# ? Language mapping
LANG_MAP = {"English": "en",
            "Hindi": "hi",
            "Marathi": "mr",
            "Gujarati": "gu",
            "Kannada": "kn",
            "Tamil": "ta",
            "Telugu": "te",
            "Malayalam": "ml",
            "Bengali": "bn",
            "Japanese": "ja",
            }


def translate_message(text, lang):

    translator = Translator()
    tranlation = translator.translate(
        text, src="en", dest=LANG_MAP[lang])

    return tranlation.text


def make_audio(text, lang, audio_path=None, regen=False):

    if audio_path is None:
        raise ValueError("Audio path not provided.")

    # Audio file not present or REGEN_AUDIO flag is True
    if (not os.path.exists(audio_path)) or (regen):

        tts = gTTS(text=text, lang=LANG_MAP[lang], slow=False)
        tts.save(audio_path)

    return audio_path
