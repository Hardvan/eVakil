from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# User's choice
LANGUAGE = None
OPTIONS_LANG = ["English", "Hindi", "Marathi", "Gujarati", "Kannada", "Tamil"]

HELLO = {
    "English": "Hi! Welcome to eVakil, your digital lawyer.",
    "Hindi": "नमस्ते! ईवकील में आपका स्वागत है, आपका डिजिटल वकील।",
    "Marathi": "नमस्कार! ईवकीलवर आपले स्वागत आहे, आपले डिजिटल वकील.",
    "Gujarati": "નમસ્તે! ઈવકીલ પર આપનું સ્વાગત છે, આપનો ડિજિટલ વકીલ.",
    "Kannada": "ಹಲೋ! ಈವಕಿಲ್‌ಗೆ ಸುಸ್ವಾಗತ, ನಿಮ್ಮ ಡಿಜಿಟಲ್ ವಕೀಲ್.",
    "Tamil": "வணக்கம்! ஈவகில் க்கு வருக, உங்கள் டிஜிட்டல் வக்கீல்."
}


@app.route('/', methods=['GET', 'POST'])
def index():
    global LANGUAGE
    if request.method == 'POST':
        LANGUAGE = request.form.get('language')
    hello_message = HELLO.get(LANGUAGE, HELLO['English'])
    return render_template("index.html", options=OPTIONS_LANG, selected_language=LANGUAGE, hello_message=hello_message)


if __name__ == "__main__":
    app.run(debug=True)
