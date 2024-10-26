import wave 
import numpy as np

def write_data(file_path, data, d_type):
    with wave.open(file_path, mode="wb") as wav_file:   
        data_repeated = np.repeat(data, 500)  
        wav_file.setnchannels(1)
        wav_file.setsampwidth(np.iinfo(d_type).bits // 8)
        wav_file.setframerate(44100)
        wav_file.writeframes(data_repeated.tobytes())


