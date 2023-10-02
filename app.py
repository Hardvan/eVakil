from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os


app = Flask(__name__)

# GLOBAL VARIABLES
user_preference = {         # ? User's preferences
    "language": "English"
}
REGEN_AUDIO = False         # ? Flag to regenerate audio file when string changes

LANG_MAP = {"English": "en",  # Language mapping
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

HELLO = "Hi! Welcome to \"eVakil\", your digital lawyer and assistant."


def get_hello_message(lang):

    translator = Translator()
    tranlation = translator.translate(
        HELLO, src="en", dest=LANG_MAP[lang])

    return tranlation.text


def make_audio(text, lang, audio_path=None):

    if audio_path is None:
        raise ValueError("Audio path not provided.")

    # Audio file not present or REGEN_AUDIO flag is True
    if not os.path.exists(audio_path) or REGEN_AUDIO:

        tts = gTTS(text=text, lang=LANG_MAP[lang], slow=False)
        tts.save(audio_path)

    return audio_path


@app.route('/', methods=['GET', 'POST'])
def index():

    result = None

    if request.method == 'POST':
        result = {}

        # Get user's choice
        global user_preference
        user_preference["language"] = request.form.get('language')

        # Get hello message in selected language
        result["hello_message"] = get_hello_message(
            user_preference["language"])

        # Make audio file
        result["hello_audio"] = make_audio(
            result["hello_message"],
            user_preference["language"],
            audio_path=f"./static/audio/hello_{user_preference['language']}.mp3")

    return render_template("index.html",
                           options=LANG_MAP.keys(),
                           user_preference=user_preference,
                           result=result)


if __name__ == "__main__":
    app.run(debug=True)
