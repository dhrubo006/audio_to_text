from transformers import pipeline, GPTNeoForCausalLM, GPT2Tokenizer

# Initialize the Whisper model for audio transcription
transcribe_pipe = pipeline(model="openai/whisper-large-v3")

# Initialize the GPT-Neo model for response generation
tokenizer = GPT2Tokenizer.from_pretrained("EleutherAI/gpt-neo-125M")
gpt_neo_model = GPTNeoForCausalLM.from_pretrained("EleutherAI/gpt-neo-125M")


def process_audio(audio_path):
    """
    Process the audio file for transcription and generate a response.

    Args:
        audio_path (str): Path to the audio file to be processed.

    Returns:
        tuple: Transcription of the audio and the generated response.
    """
    # Transcribe the audio
    result = transcribe_pipe(audio_path)
    transcription = result["text"]

    # Generate a response using GPT-Neo-125M
    inputs = tokenizer.encode(transcription, return_tensors="pt")
    outputs = gpt_neo_model.generate(inputs)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return transcription, response
