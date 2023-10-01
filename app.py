from flask import Flask, render_template, request, jsonify
from googletrans import Translator
from gtts import gTTS
import os


app = Flask(__name__)

# User's choice
LANGUAGE = None
OPTIONS_LANG = ["English", "Hindi", "Marathi", "Gujarati", "Kannada", "Tamil"]

HELLO = {
    "English": "Hi! Welcome to \"eVakil\", your digital lawyer and assistant.",
}


def get_hello_message(lang):

    lang_map = {"English": "en",
                "Hindi": "hi",
                "Marathi": "mr",
                "Gujarati": "gu",
                "Kannada": "kn",
                }

    translator = Translator()
    tranlation = translator.translate(
        HELLO['English'], src="en", dest=lang_map[lang])

    return tranlation.text


def make_audio(text, lang):

    lang_map = {"English": "en",
                "Hindi": "hi",
                "Marathi": "mr",
                "Gujarati": "gu",
                "Kannada": "kn",
                }

    tts = gTTS(text=text, lang=lang_map[lang], slow=False)
    # If file exists, delete it
    if os.path.exists("./static/audio/hello.mp3"):
        os.remove("./static/audio/hello.mp3")
    tts.save("./static/audio/hello.mp3")


@app.route('/', methods=['GET', 'POST'])
def index():

    result = None

    if request.method == 'POST':
        result = {}

        # Get user's choice
        global LANGUAGE
        LANGUAGE = request.form.get('language')

        # Get hello message in selected language
        result["hello_message"] = get_hello_message(LANGUAGE)

        # Make audio file
        make_audio(result["hello_message"], LANGUAGE)

    return render_template("index.html",
                           options=OPTIONS_LANG,
                           selected_language=LANGUAGE,
                           result=result)


if __name__ == "__main__":
    app.run(debug=True)
