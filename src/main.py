import os
import argparse
from transcribe import transcribe_audio

def main():
    """
    Main function that serves as the entry point of the program.
    Handles audio file transcription using Whisper.
    """
    parser = argparse.ArgumentParser(description="Transcribe audio files using Whisper")
    parser.add_argument("audio_path", help="Path to the audio file or directory containing audio files")
    parser.add_argument("--model", default="base", choices=["tiny", "base", "small", "medium", "large"],
                      help="Whisper model size (default: base)")
    
    args = parser.parse_args()
    
    # Check if path exists
    if not os.path.exists(args.audio_path):
        print(f"Error: Path '{args.audio_path}' not found.")
        return
    
    # Handle single file
    if os.path.isfile(args.audio_path):
        print(f"Transcribing file: {args.audio_path}")
        transcription = transcribe_audio(args.audio_path, args.model)
        print("\nTranscription completed!")
    
    # Handle directory
    else:
        audio_extensions = ('.mp3', '.wav', '.m4a', '.ogg', '.flac')
        audio_files = [f for f in os.listdir(args.audio_path) 
                      if os.path.isfile(os.path.join(args.audio_path, f)) 
                      and f.lower().endswith(audio_extensions)]
        
        if not audio_files:
            print(f"No audio files found in {args.audio_path}")
            return
        
        print(f"Found {len(audio_files)} audio files to transcribe")
        for audio_file in audio_files:
            full_path = os.path.join(args.audio_path, audio_file)
            print(f"\nTranscribing: {audio_file}")
            transcription = transcribe_audio(full_path, args.model)
            print(f"Completed transcription of {audio_file}")

if __name__ == "__main__":
    main() 