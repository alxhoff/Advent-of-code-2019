#!/bin/python

import numpy as np
import math
import hashlib

class FFT:

    base_repeating_pattern = np.array([0,1,0,-1])

    def __init__(self, signal=None):

        if signal:
            self.signal = self._arrayInt(int(signal))
        else:
            self.signal = self._arrayInt(int(input("$>")))
        self.base_patterns = dict()

    def _getKey(self, val):
        return hashlib.sha1(str(val).encode()).hexdigest()

    def _arrayInt(self, res):
        ret = []
        str_arr = str(res)
        for char in str_arr:
            ret.append(int(char))
        return np.array(ret)

    def _getRepeatingPattern(self, index, len):
        len+=1 #as we discard first element
        ret = []

        key = self._getKey([index, len])

        if key in self.base_patterns:
            return self.base_patterns[key]

        for i in range(self.base_repeating_pattern.size):
            add = np.full(index + 1, self.base_repeating_pattern[i])
            ret.append(add)
        ret = np.concatenate(ret)

        if ((index + 1) * 4 - 1) >= len:
            ret = ret[1:len]
            self.base_patterns[key] = ret
            return ret
        else:
            repeats = math.ceil(len/((index + 1) * 4)) - 1
            apnd = [ret]
            for i in range(repeats):
                apnd.append(np.copy(ret))
            ret = np.concatenate(apnd)[1:len]
            self.base_patterns[key] = ret
            return ret


    def _getReturnArray(self, inp):

        ret = []
        for digit in inp:
            ret.append(abs(digit) % 10)
        return np.array(ret)

    def _multiply(self, index, array):

        rep = self._getRepeatingPattern(index, array.size)
        return  abs(np.sum(rep * array)) % 10

    def intArray(self):

        ret = 0
        for i in range(self.signal.size):
            ret += self.signal[self.signal.size - i - 1] * 10**i

        return ret

    def performFFT(self, times=1):

        for i in range(times):
            ret = []
            for i in range(len(self.signal)):
                ret.append(self._multiply(i, self.signal))

            self.signal = np.array(ret)


fft = FFT(59754835304279095723667830764559994207668723615273907123832849523285892960990393495763064170399328763959561728553125232713663009161639789035331160605704223863754174835946381029543455581717775283582638013183215312822018348826709095340993876483418084566769957325454646682224309983510781204738662326823284208246064957584474684120465225052336374823382738788573365821572559301715471129142028462682986045997614184200503304763967364026464055684787169501819241361777789595715281841253470186857857671012867285957360755646446993278909888646724963166642032217322712337954157163771552371824741783496515778370667935574438315692768492954716331430001072240959235708)
fft.performFFT(100)
print(fft.signal)
print(fft.intArray())

