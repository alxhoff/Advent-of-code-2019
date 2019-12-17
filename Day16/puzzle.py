#!/bin/python

import numpy as np
import math
import sys


class FFT:

    base_repeating_pattern = np.array([0, 1, 0, -1])

    def __init__(self, signal=None):

        if signal:
            char_arr = np.array([int(val) for val in signal])
            self.signal = np.concatenate(np.repeat([char_arr], 10000, axis=0))
        else:
            char_arr = np.array([int(val) for val in input("$>")])
            self.signal = np.concatenate(np.repeat([char_arr], 10000, axis=0))

        self.test_signal = np.copy(self.signal)
        self.offset = self.intArray(self.signal[:7])

        print("Offset: {}".format(self.offset))

    def _arrayInt(self, res):
        ret = []
        str_arr = str(res)
        for char in str_arr:
            ret.append(int(char))
        return np.array(ret)

    def _getRepeatingPattern(self, index, len):
        len += 1  #as we discard first element
        ret = []

        for i in range(self.base_repeating_pattern.size):
            add = np.full(index + 1, self.base_repeating_pattern[i])
            ret.append(add)
        ret = np.concatenate(ret)

        if ((index + 1) * 4 - 1) >= len:
            ret = ret[1:len]
            return ret
        else:
            repeats = math.ceil(len / ((index + 1) * 4)) - 1
            apnd = [ret]
            for i in range(repeats):
                apnd.append(np.copy(ret))
            ret = np.concatenate(apnd)[1:len]
            return ret

    def _getReturnArray(self, inp):

        ret = []
        for digit in inp:
            ret.append(abs(digit) % 10)
        return np.array(ret)

    def _multiply(self, index, array):

        rep = self._getRepeatingPattern(index, array.size)
        return abs(np.sum(rep * array)) % 10

    def intArray(self, array=None):

        ret = 0

        if not any(array):
            for i in range(self.test_signal.size):
                ret += self.test_signal[self.test_signal.size - i - 1] * 10**i
        else:
            for i in range(array.size):
                ret += array[array.size - i - 1] * 10**i

        return ret

    def performFFT(self, times=1):

        for i in range(times):
            ret = []
            for i in range(len(self.test_signal)):
                ret.append(self._multiply(i, self.test_signal))

            self.test_signal = np.array(ret)
            print(self.test_signal)

    def sumBottomHalf(self, times=10):
        half = int(self.signal.size / 2)

        for i in range(times):
            new_signal = np.copy(self.signal)
            sum = 0
            for n in reversed(range(half, self.signal.size)):
                sum += self.signal[n]
                sum = sum % 10
                new_signal[n] = sum

            self.signal = new_signal

            print("{} : {}".format(i, self.signal))

    def getOffsetValue(self):
        val = self.signal[self.offset:self.offset + 8]
        return self.intArray(val)


fft = FFT(
    '59754835304279095723667830764559994207668723615273907123832849523285892960990393495763064170399328763959561728553125232713663009161639789035331160605704223863754174835946381029543455581717775283582638013183215312822018348826709095340993876483418084566769957325454646682224309983510781204738662326823284208246064957584474684120465225052336374823382738788573365821572559301715471129142028462682986045997614184200503304763967364026464055684787169501819241361777789595715281841253470186857857671012867285957360755646446993278909888646724963166642032217322712337954157163771552371824741783496515778370667935574438315692768492954716331430001072240959235708'
)

# fft.performFFT(100)
#
# print("Recursion")

fft.sumBottomHalf(100)
print(fft.getOffsetValue())
