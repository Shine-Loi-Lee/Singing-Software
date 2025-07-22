import pyttsx3
import os
import random
from pydub import AudioSegment
from pydub.playback import play
import uuid
import time

# Basic settings
output_dir = "tmp_syllables"

# Syllable splitter (Korean only, ignores whitespace)
def split_syllables(text):
    return [char for char in text if char.strip() != ""] # List of syllables without spaces

# Save TTS audio for a single syllable
def save_syllable_tts(syllable, filename):
    engine=pyttsx3.init()
    engine.setProperty('rate', 1000) # Speech rate
    engine.save_to_file(syllable, filename)
    engine.runAndWait()
    engine.stop()
    
# Pitch shifting function
def pitch_shift(sound, semitones):
    new_sample_rate = int(sound.frame_rate*(2.0**(semitones/12.0)))
    shifted=sound._spawn(sound.raw_data, overrides={'frame_rate':new_sample_rate})
    return shifted.set_frame_rate(sound.frame_rate)

# Main function
def sing_text(text, output_path="singing_output.wav"):
    # 
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    syllables=split_syllables(text)
    final_audio=AudioSegment.silent(duration=0)
    
    for i, syllable in enumerate(syllables):
        print(f"Processing syllable: '{syllable}' ({i+1}/{len(syllables)})")
        
        temp_filename=os.path.join(output_dir, f"{uuid.uuid4().hex}.wav")
        save_syllable_tts(syllable, temp_filename)
        
        while not os.path.exists(temp_filename) or os.path.getsize(temp_filename)==0:
            time.sleep(0.1)
        
        sound=AudioSegment.from_file(temp_filename, format="wav")
        
        semitone_shift=random.randint(-5, 7) # Random pitch shift between -5 and +7 semitones
        shifted = pitch_shift(sound, semitone_shift)
        
        final_audio += shifted+AudioSegment.silent(duration=100) # Short pause between syllables
        
        os.remove(temp_filename)
        
    # Export final audio
    final_audio.export(output_path, format="wav")
    print(f"Singing voice saved to: {output_path}")
    # play(final_audio) # Playback
    
# Example execution
if __name__ == "__main__":
    input_text=input("Enter lyrics: ")
    sing_text(input_text)