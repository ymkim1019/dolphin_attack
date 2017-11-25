import wave
import wavio
import numpy as np
import argparse
from scipy.signal import resample
import sounddevice as sd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=str)
    parser.add_argument("fs", type=int, default=88200)
    parser.add_argument("fc", type=int, default=25000)

    args = parser.parse_args()

    # audio load
    voice = wave.open(args.file_path, 'rb')
    Fs = voice.getframerate()
    target_fs = args.fs
    Fc = args.fc # modulation frequency
    n_channels = voice.getnchannels()
    n_samples = voice.getnframes()
    sampwidth = voice.getsampwidth()
    sample_max_range = (pow(2, 8*sampwidth))/2
    data = voice.readframes(n_samples)
    array = wavio._wav2array(n_channels, sampwidth, data)
    array = array / sample_max_range # normalization

    # resampling
    if Fs != target_fs:
        n_samples = int(n_samples * (target_fs / Fs))
        array = resample(array, n_samples)
    Fs = target_fs
    t = np.arange(n_samples)

    # modulation
    carrier = np.array([np.cos(2 * np.pi * Fc * (1 / Fs) * t)] * n_channels).transpose()
    mod = np.multiply(array, carrier) - np.min(array) * 1.1 * carrier
    sd.play(mod[:, 0]*1.3, Fs)
