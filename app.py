from flask import Flask, render_template, request, jsonify

# Custom modules
from google_handlers import LANG_MAP, translate_message, make_audio


app = Flask(__name__)

# GLOBAL VARIABLES
user_preference = {         # ? User's preferences
    "language": "English"   # Default
}

REGEN_AUDIO = False  # ? Set to True when string changes (regenerate audio)

HELLO = "Hi! Welcome to \"eVakil\", your digital lawyer and assistant."


@app.route('/', methods=['GET', 'POST'])
def index():

    result = None

    if request.method == 'POST':

        # Get user's language preference
        lang = request.form.get('language')
        global user_preference
        user_preference["language"] = lang

        # Get hello message in selected language
        translated_text = translate_message(HELLO, lang)

        # Make audio file in selected language
        audio_path = make_audio(
            translated_text, lang,
            audio_path=f"./static/audio/hello_{lang}.mp3",
            regen=REGEN_AUDIO)

        result = {}
        result["hello_message"] = translated_text
        result["hello_audio"] = audio_path

    return render_template("index.html",
                           options=LANG_MAP.keys(),
                           user_preference=user_preference,
                           result=result)


if __name__ == "__main__":
    app.run(debug=True)
