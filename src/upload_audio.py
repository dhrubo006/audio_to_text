import os
from flask import request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from .process_audio import process_audio


def allowed_file(filename, ALLOWED_EXTENSIONS):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



def upload_audio(app, ALLOWED_EXTENSIONS, UPLOAD_FOLDER):
    """
    Handle the uploading and processing of audio files for speech-to-text conversion.
    """
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            audio_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(audio_path)

            try:
                transcription = process_audio(audio_path)
                return transcription
            except Exception:
                flash('Error processing audio file')
                return redirect(url_for('upload_file'))
        else:
            flash('File type not allowed')
            return redirect(request.url)