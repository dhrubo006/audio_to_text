import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
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


@app.route("/uploader", methods=["POST", "GET"])
def handle_upload():
    """
    Handle the file upload process from the client side.
    This function is triggered when a file is uploaded through the Flask app's front-end.
    It checks for the file's presence, validates it, saves it, and then processes it for transcription.
    """

    # Check if the 'file' key is part of the form data in the incoming request
    if "file" not in request.files:
        # If the 'file' key is missing, it means no file was uploaded
        flash("No file part")  # Display a message to the user
        return redirect(request.url)  # Redirect the user back to the upload page

    # Retrieve the file object from the form data
    file = request.files["file"]

    # Check if a file was actually selected and has a non-empty filename
    if file.filename == "":
        flash("No selected file")  # Inform the user that no file was selected
        return redirect(request.url)  # Redirect back to the upload page

    # Check if the file is of an allowed type using the 'allowed_file' function
    if file and allowed_file(file.filename):
        # Create a secure filename for the file
        filename = secure_filename(file.filename)
        # Ensure that the upload directory exists, create it if not
        if not os.path.exists(app.config["UPLOAD_FOLDER"]):
            os.makedirs(app.config["UPLOAD_FOLDER"])
        # Construct the full path where the file will be saved
        audio_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(audio_path)  # Save the file to the server

        # Process the audio file to transcribe its content
        try:
            print("trying to transcribe")  # Log the start of the transcription process
            transcription = process_audio(audio_path)  # Transcribe the audio content
            print("transcription Done")  # Log the completion of the transcription
            return jsonify(
                {"transcription": transcription}
            )  # Send the transcription as a JSON response
        except Exception as e:
            flash(
                "Error processing audio file"
            )  # Display an error message if transcription fails
            return redirect(url_for("upload_file"))  # Redirect back to the upload page
    else:
        flash(
            "File type not allowed"
        )  # Inform the user if the file type is not permitted
        return redirect(request.url)  # Redirect back to the upload page


if __name__ == "__main__":
    app.run(debug=True)
