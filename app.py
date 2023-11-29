from flask import Flask, render_template
from src.upload_audio import upload_audio

app = Flask(__name__)

# Configuration
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max file size
ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg"}


@app.route("/")
def upload_file():
    """Render the file upload form."""
    return render_template("upload.html")


@app.route("/uploader", methods=["GET", "POST"])
def handle_upload():
    return upload_audio(app, ALLOWED_EXTENSIONS, app.config["UPLOAD_FOLDER"])


if __name__ == "__main__":
    app.run(debug=True)
