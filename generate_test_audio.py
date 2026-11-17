import wave
import struct
import os

# Generates a quick 3-second test WAV/MP3 asset for pipeline verification
def generate_test_audio(filename="test_voiceover.wav"):
    sample_rate = 44100
    duration = 3.0  # seconds
    frequency = 440.0  # A4 note tone
    
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1) # Mono
        wav_file.setsampwidth(2) # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        for i in range(int(sample_rate * duration)):
            value = int(32767.0 * 0.5 * struct.math.sin(2.0 * struct.math.pi * frequency * i / sample_rate))
            data = struct.pack('<h', value)
            wav_file.writeframes(data)
            
    print(f"Test audio asset generated successfully: {filename}")

if __name__ == "__main__":
    generate_test_audio()