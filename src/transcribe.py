import whisper
import torch
import os

def ensure_transcriptions_dir():
    """Ensure the transcriptions directory exists."""
    transcriptions_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "transcriptions")
    os.makedirs(transcriptions_dir, exist_ok=True)
    return transcriptions_dir

def transcribe_audio(audio_path, model_name="base"):
    """
    Transcribe audio file using Whisper model.
    
    Args:
        audio_path (str): Path to the audio file
        model_name (str): Whisper model size (tiny, base, small, medium, large)
    
    Returns:
        str: Transcribed text
    """
    # Check if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    # Load the Whisper model
    print(f"Loading {model_name} model...")
    model = whisper.load_model(model_name, device=device)
    
    # Transcribe the audio
    print("Transcribing audio...")
    result = model.transcribe(audio_path)
    
    return result["text"] 