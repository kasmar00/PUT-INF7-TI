import math
from typing import List
from bitarray import bitarray


def count_freq(letters: List[str]):
    freq = {}
    for letter in letters:
        freq[letter] = freq.get(letter, 0) + 1
    return freq


class Compress:
    code = {}
    code_length = None

    def create(self, corpus: str):
        # letters = corpus.split()
        freq = count_freq(corpus)
        possible_chars = freq.keys()

        self.code_length = math.ceil(math.log2(len(possible_chars)))

        sorted_freq = sorted(freq.items(), key=lambda item: -item[1])

        for index, (key, _) in enumerate(sorted_freq):
            self.code[key] = bitarray(format(index, f"0{self.code_length}b"))

    def encode(self, text: str):
        encoded = bitarray()

        for letter in text:
            encoded += self.code[letter]

        return encoded

    def decode(self, text: bitarray):
        decoded = []

        code = {key: val for val, key in self.code_as_string().items()}

        for x in range(math.floor(len(text)/self.code_length)):
            encoded_char = text[x*self.code_length:(x+1)*self.code_length]
            decoded.append(code[encoded_char.to01()])

        return "".join(decoded)

    def code_as_string(self):
        code = {}
        for key, val in self.code.items():
            code[key] = val.to01()
        return code

    def load_code(self, code: dict):
        self.code = {key: bitarray(val) for key, val in code.items()}
        self.code_length = len(list(code.items())[1][1])
