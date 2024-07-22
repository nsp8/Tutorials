from dataclasses import dataclass, field
from time import sleep

import librosa
import matplotlib.pyplot as plt
import numpy as np
import pyaudio
import soundfile as sf
from scipy import fftpack as fft
from scipy.signal import medfilt
import wave


@dataclass
class AudioProcessor:
    
    chunk: int = field(default=1024)  # Record in chunks of 1024 samples
    sample_format: int = field(default=pyaudio.paInt16)  # 16 bits per sample
    channels: int = field(default=2)
    frequency_seconds: int = field(default=44100)  # Record at 44100 samples per second
    time_to_store_seconds: int = field(default=3)
    frames: list = field(default_factory=list)

    port_audio = pyaudio.PyAudio()  # Create an interface to PortAudio
    stream = None

    def __enter__(self):
        self.stream = self.port_audio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.frequency_seconds,
            frames_per_buffer=self.chunk,
            input=True
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        
        # Stop and close the stream
        self.stream.stop_stream()
        self.stream.close()
        # Terminate the PortAudio interface
        self.port_audio.terminate()
        self.frames = []
        print("Finished recording")

    def record(self):
        print("Recording...")
        # Store data in chunks for 3 seconds
        chunks = int(self.frequency_seconds / self.chunk * self.time_to_store_seconds)
        for i in range(0, chunks):
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def save(self, output_file="output.wav"):
        # Save the recorded data as a WAV file
        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.port_audio.get_sample_size(self.sample_format))
            wf.setframerate(self.frequency_seconds)
            wf.writeframes(b"".join(self.frames))

    @staticmethod
    def denoise(input_file_path, output_file_path):
        data, sampling_rate = librosa.load(input_file_path, sr=None)
        # executing STFT
        audio_magnitude, audio_phase = librosa.magphase(librosa.stft(data))
        # to take frames from the first few seconds
        noise_power = np.mean(audio_magnitude[:, :int(sampling_rate * 0.1)], axis=1)
        mask = audio_magnitude > noise_power[:, None]
        mask = medfilt(mask.astype(float), kernel_size=(1, 5))
        clean_magnitude = audio_magnitude * mask
        clean_data = librosa.istft(clean_magnitude * audio_phase)
        sf.write(output_file_path, clean_data, sampling_rate)


def record_audio(output_file="out.mp3"):
    with AudioProcessor() as audio_processor:
        audio_processor.record()
    audio_processor.save(output_file)


if __name__ == "__main__":
    # TODO: resolve issues with pyaudio and numpy processing STFT
    _output_file = "out.mp3"
    record_audio(_output_file)
    AudioProcessor.denoise(_output_file, "denoise.wav")
