from transformers import pipeline


# Initialize the Whisper model
pipe = pipeline(model="openai/whisper-large-v3")


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
    result = pipe(audio_path)
    return result["text"]

