import wave
import numpy as np

def read_data(file_path):
    # Открыть файл wav
    wav = wave.open(file_path, mode="r")
    # Считать параметры wav файла
    # nchannels - Количество каналов (1 или 2)
    # sampwidth - Сколько байт уходит на кодирование одного сэмпла (1, 2, или 4)
    # framerate - Частота
    # nframes - Количество кадров
    # comptype - Тип сжатия
    # compname - Название сжатия
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav.getparams()
    # Считать все кадры
    content = wav.readframes(nframes)
    types = {
        1: np.int8,
        2: np.int16,
        4: np.int32
    }
    samples = np.fromstring(content, dtype=types[sampwidth])
    # Проредить данные если несколько каналов
    channel = samples[0::nchannels]
    # Закрыть файл wav
    wav.close()
    return (nchannels, sampwidth, framerate, nframes, comptype, compname, types[sampwidth], channel)