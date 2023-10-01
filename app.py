from flask import Flask, render_template, request

app = Flask(__name__)


# User's choice
LANGUAGE = None
OPTIONS_LANG = ["English",
                "Hindi",
                "Marathi",
                "Gujarati",
                "Kannada",
                "Tamil",
                ]

HELLO = "Hi! Welcome to eVakil, your digital lawyer."


@app.route('/')
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
