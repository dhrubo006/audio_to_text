import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.utils import secure_filename
from src.process_audio import process_audio

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Configuration
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max file size
ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg"}

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def upload_file():
    """Render the file upload form."""
    return render_template("upload.html")

@app.route("/uploader", methods=["POST"])
def handle_upload():
    """
    Handle the file upload process and process the uploaded audio file.
    """
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
            transcription, response = process_audio(audio_path)
            return jsonify({"transcription": transcription, "response": response})
        except Exception as e:
            flash("Error processing audio file")
            return redirect(url_for("upload_file"))

if __name__ == "__main__":
    app.run(debug=True)
