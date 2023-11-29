import os
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from transformers import pipeline

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file size
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}

# Initialize the Whisper model
pipe = pipeline(model="openai/whisper-large-v3")

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_audio(audio_path):
    """
    Process the given audio file for speech-to-text transcription using Whisper Large v3.

    This function takes the path of an audio file as input and utilizes the Whisper Large v3
    model to transcribe the speech in the audio file to text. It handles any exceptions during
    the transcription process and logs an error if one occurs. 

    Args:
    audio_path (str): The file path of the audio file to be transcribed.

    Returns:
    str: The transcribed text from the audio file if successful, otherwise raises an exception.
    """
    try:
        result = pipe(audio_path)
        return result["text"]
    except Exception as e:
        app.logger.error(f'Error processing audio file: {e}')
        raise

@app.route('/')
def upload_file():
    """Render the file upload form."""
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_audio():
    """
    Handle the uploading and processing of audio files for speech-to-text conversion.

    This function is triggered when a user submits an audio file via the '/uploader' route.
    It performs several checks to validate the presence and type of the file. If the file
    is valid, it is saved to the specified upload folder. The function then calls another
    function to process this audio file using the Whisper Large v3 model for transcription.
    In case of any processing errors, it logs the error and notifies the user.

    Args:
    None

    Returns:
    The transcribed text if successful, or redirects to the upload page with an error message.
    """

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
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

if __name__ == '__main__':
    app.run(debug=True)
