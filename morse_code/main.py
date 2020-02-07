""" Morse Code """
""" You cannot use (_) and (/) in your morse code. """

import os
import time
import re
import numpy as np
import scipy
from scipy.io import wavfile
import wave
import matplotlib.pyplot as plt
import configparser


from morse_table import encode_morse, decode_morse


# Parse config files
config_file = configparser.ConfigParser()
config_file.read('./config.ini')
FREQUENCY = config_file.getfloat("MORSE_SIGNAL", "frequency")
PERIOD = config_file.getfloat("MORSE_SIGNAL", "period")
RATE = config_file.getint("MORSE_SIGNAL", "rate")
AMP = config_file.getfloat("MORSE_SIGNAL", "amp")



######functions######


# Create morse pattern wave
def create_morse(s, filename="morse.wav"):
    if "_" in s or "/" in s:
        raise SyntaxError("Cannot use (/) and (_)")

    s = "/".join(["_".join(word) for word in s.split()]) + "/"
    """
    e.g) I am Mike.  ==> I a_m  M_i_k_e_. 
    """
    
    signal_table = dict()
    signals = list()
    for c in s:
        if c in signal_table.keys():
            signal = signal_table[c]
        else:
            morse = encode_morse(c.upper())
            signal = make_morsesignal(morse)
            signal_table[c] = signal
        signals.append(signal)
        
    wave = np.concatenate([signal for signal in signals])
    wavfile.write(filename, RATE, wave)
    
    return wave


# Make morse signal pattern
def make_morsesignal(morse):
    amp = AMP
    time = PERIOD

    signal = np.array([], dtype=np.int16)
    for c in morse:

        if c == ".": # 短符 1
            time = PERIOD
            amp = AMP
        elif c == "-": # 長符 3
            time = 3 * PERIOD
            amp = AMP
        elif c == " ": # 符号の間 1
            time = PERIOD
            amp = 0
        elif c == "_": # 文字の間 3
            time = 3 * PERIOD
            amp = 0
        elif c == "/": # 語の間 7
            time = 7 * PERIOD
            amp = 0
        else:
            return

        phases = np.cumsum(2.0 * np.pi * FREQUENCY / RATE * np.ones(int(RATE * time)))

        sin = amp * np.sin(phases)
        sin = (sin * float(2 ** 15-1)).astype(np.int16)
        
        signal = np.concatenate((signal, sin))
    
    return signal


# Plot wave
def plot_wave(wave):
    t = np.linspace(0, len(wave) / FREQUENCY, len(wave))

    plt.plot(t, wave, label="morse")
    plt.show()

# Return the wave given file name
def get_wav(dirpath, filename):
    try:
        filepath = os.path.join(dirpath, filename)
    except:
        raise FileNotFoundError("{} is not found".format(filename))
    wr = wave.open(filepath)
    data = wr.readframes(wr.getnframes())
    wr.close()
    data = np.frombuffer(data, dtype=np.int16) / float(2**15)

    return data


#  Analyse morse pattern wave and return the decode result
def analysis_wave(data):
    waves = np.array(np.split(data, len(data) / int(RATE*PERIOD)))
    means = np.mean(waves * waves, axis=1)


    threshold = AMP**2 /2 /2 # Avarage of sin**2 / 2  (2 = √2 * √2)

    s = str()
    for mean in means:
        if mean > threshold:
            s += "s"
        else:
            s += "n"

    s = s.replace("sss", "-")
    s = s.replace("s", ".")
    s = s.replace("nnnnnnn", "/")
    s = s.replace("nnn", "_")
    s = s.replace("n", " ")

    words = s.split("/")
 
    result = str()
    for word in words:
        sigs = word.split("_")
        for sig in sigs:
            result += decode_morse(sig)
        result += " "
    
    return result


def channel(wave):
    pass



# Main thread
if __name__ == "__main__":
    start = time.time()
    s = "".join([chr(ord("a")+i) for i in range(26)])
    create_morse(s)
    wave = get_wav(os.path.curdir, "morse.wav")


    result = analysis_wave(wave)
    print(result)
    
    end = time.time()
    print("Time:", end-start)

