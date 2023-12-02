import os
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from src.process_audio import process_audio

app = Flask(__name__)
app.secret_key = "unique"

# Configuration
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max file size
ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg"}


def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_file():
    """Render the file upload form."""
    return render_template("upload.html")


@app.route("/uploader", methods=["POST", 'GET'])
def handle_upload():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(audio_path)

        
        try:
            print("trying to trnscribe")
            transcription = process_audio(audio_path)
            print("transcription Done")
            return transcription
        except Exception as e:
            flash("Error processing audio file")
            return redirect(url_for("upload_file"))
    else:
        flash("File type not allowed")
        return redirect(request.url)


if __name__ == "__main__":
    app.run(debug=True)
